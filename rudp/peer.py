from . import address
from . import packet
import time
from struct import pack
from random import randint


ACTION_TIMEOUT = 5000
DROP_TIMEOUT = ACTION_TIMEOUT * 2


def rudp_timestamp():
    return int(round(time.time() * 1000))


class peer_handler(object):
    def __init__(self, handle_packet, link_info, dropped):
        self.handle_packet = handle_packet
        self.link_info = link_info
        self.dropped = dropped


class peer(object):
    def __init__(self, rudp, addr, handler, endpoint):
        self.rudp = rudp
        self.sendq = []
        self.handler = handler
        self.endpoint = endpoint
        self.address = address.address()
        self.address.set(addr)
        self.scheduled = False
        self.reset()
        self.service_schedule()

    def reset(self):
        print("reset peer")
        if self.scheduled:
            self.rudp.evtloop.remove(self.service)
        self.sendq = []
        self.scheduled = False
        self.abs_timeout_deadline = rudp_timestamp() + DROP_TIMEOUT
        self.in_seq_reliable = 0xffff
        self.in_seq_unreliable = 0
        self.out_seq_reliable = randint(0, 2 ** 16 - 1)
        self.out_seq_unreliable = 0
        self.out_seq_acked = self.out_seq_reliable - 1
        self.state = 'new'
        self.must_ack = 0
        self.sendto_err = 0
        self.last_out_time = rudp_timestamp()

    def analyse_reliable(self, reliable_seq):
        print("analyse reliable")
        if self.in_seq_reliable == reliable_seq:
            return 'retransmitted'

        if (self.in_seq_reliable + 1) % (2 ** 16) != reliable_seq:
            print("unsequenced!", self.in_seq_reliable + 1, reliable_seq)
            return 'unsequenced'

        self.in_seq_reliable = reliable_seq
        self.in_seq_unreliable = 0

        print("sequenced")
        return 'sequenced'

    def analyse_unreliable(self, reliable_seq, unreliable_seq):
        if self.in_seq_reliable != reliable_seq:
            return 'unsequenced'

        unreliable_delta = unreliable_seq - self.in_seq_unreliable

        if unreliable_delta <= 0:
            return 'unsequenced'

        self.in_seq_unreliable = unreliable_seq

        return 'sequenced'

    def handle_ack(self, reliable_ack):
        pass

    def handle_packet(self):
        pass

    def handle_ping(self, pc):
        if pc.header.opt & packet.RUDP_OPT_RETRANSMITTED:
            return

        out = packet.packet_data(data=pc.data)
        header = out.header
        header.command = packet.RUDP_CMD_PONG
        header.opt = 0

        self.send_unreliable(out)

    def handle_pong(self):
        pass

    def incoming_packet(self, pc):
        print("peer incoming packet", self.state)
        header = pc.header
        if header.opt & packet.RUDP_OPT_ACK:
            self.handle_ack(header.reliable_ack)

        if header.opt & packet.RUDP_OPT_RELIABLE:
            state = self.analyse_reliable(header.reliable)
        else:
            state = self.analyse_unreliable(header.reliable, header.unreliable)

        if state == 'unsequenced':
            if (self.state == 'connecting' and
                    header.command == packet.RUDP_CMD_CONN_RSP):
                print("run.")
                self.in_seq_reliable = header.reliable
                self.handle_ack(header.reliable_ack)
                self.state = 'run'
        elif state == 'retransmitted':
            self.abs_timeout_deadline = rudp_timestamp() + DROP_TIMEOUT
        elif state == 'sequenced':
            self.abs_timeout_deadline = rudp_timestamp() + DROP_TIMEOUT
            if header.command == packet.RUDP_CMD_CLOSE:
                print("peer dead (CMD CLOSE)")
                self.state = 'dead'
                self.handler.dropped(self)
            elif header.command == packet.RUDP_CMD_PING:
                if self.state == 'run':
                    self.handle_ping(pc)
                else:
                    print("ping while not running")
            elif header.command == packet.RUDP_CMD_PONG:
                if self.state == 'run':
                    self.handle_pong(pc)
                else:
                    print("pong while not running")
            elif header.command >= packet.RUDP_CMD_APP:
                self.handler.handle_packet(pc)

        if header.opt & packet.RUDP_OPT_RELIABLE:
            self.post_ack()
        self.service_schedule()

    def send_connect(self):
        pc = packet.packet_conn_req()
        self.state = 'connecting'
        return self.send_reliable(pc)

    def send_reliable(self, pc):
        pc.header.opt = packet.RUDP_OPT_RELIABLE
        self.out_seq_reliable += 1
        pc.header.reliable = self.out_seq_reliable
        pc.header.unreliable = 0
        self.out_seq_unreliable = 0
        self.sendq.append(pc)
        self.service_schedule()
        return self.sendto_err

    def send_unreliable(self, pc):
        pc.header.opt = 0
        self.out_seq_unreliable += 1
        pc.header.reliable = self.out_seq_reliable
        pc.header.unreliable = self.out_seq_unreliable
        self.sendq.append(pc)
        self.service_schedule()
        return self.sendto_err

    def post_ack(self):
        pass

    def service_schedule(self):
        delta = ACTION_TIMEOUT

        if self.sendq:
            head = self.sendq[0]
            header = head.header
            if header.opt & packet.RUDP_OPT_RETRANSMITTED:
                print("already transmitted head, wait for rto")
                # already transmitted head, wait for rto
                delta = rudp_timestamp() - self.last_out_time + self.rto
            else:
                # transmit asap
                delta = 0

        to_delta = self.abs_timeout_deadline - rudp_timestamp()

        if to_delta < delta:
            delta = to_delta
        if delta <= 0:
            delta = 1

        self.rudp.evtloop.add(rudp_timestamp() + delta, self.service)
        self.scheduled = True
        print("end service schedule")

    def ping(self):
        print("ping")
        pc = packet.packet_data()
        pc.header.command = packet.RUDP_CMD_PING
        pc.data = pack('!Q', rudp_timestamp())
        self.send_reliable(pc)

    def send_queue(self):
        while self.sendq:
            packet = self.sendq.pop()
            header = packet.header
            if self.must_ack:
                header.opt |= packet.RUDP_OPT_ACK
                header.reliable_ack = self.in_seq_reliable

            self.send_raw(packet)

    def send_raw(self, packet):
        print("send raw")
        self.last_out_time = rudp_timestamp()
        self.endpoint.send(self.address.get(), packet.raw())

    def service(self):
        print("service")
        self.scheduled = False

        if self.abs_timeout_deadline < rudp_timestamp():
            print("Dropped because abs timeout deadline < now")
            self.handler.dropped(self)
            return

        if not self.sendq:
            out_delta = rudp_timestamp() - self.last_out_time
            if out_delta > ACTION_TIMEOUT:
                self.ping()

        self.send_queue()
        self.service_schedule()
