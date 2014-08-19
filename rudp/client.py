from . import address
from . import endpoint
from . import peer
from . import packet


class client_handler(object):
    def __init__(self, handle_packet, link_info, connected, server_lost):
        self.handle_packet = handle_packet
        self.link_info = link_info
        self.connected = connected
        self.server_lost = server_lost


class client(object):
    def __init__(self, rudp, handler):
        self.rudp = rudp
        self.handler = handler
        self.address = address.address()
        self.endpoint = endpoint.endpoint(
            rudp, endpoint.endpoint_handler(self.handle_endpoint_packet))
        self.connected = False
        self.peer = None
        self.peer_handler = peer.peer_handler(self.handle_data_packet,
                                              self.link_info, self.peer_dropped)

    def link_info(self, peer, info):
        pass

    def handle_endpoint_packet(self, addr, pc):
        print("Endpoint handling packet", addr, pc)
        try:
            self.peer.incoming_packet(pc)
            if not self.connected:
                self.connected = True
                self.handler.connected(self)
        except Exception as e:
            print(e)
            print("ignore packet.")

    def peer_dropped(self, peer):
        print("client peer dropped")

    def handle_data_packet(self, peer, pc):
        self.handler
        print("client handle data packet")

    def connect(self):
        addr = self.address.get()
        self.peer = peer.peer(self.rudp, addr, self.peer_handler, self.endpoint)
        self.endpoint.set_addr(('', 0))
        self.peer.send_connect()
        self.endpoint.bind()

    def close(self):
        self.endpoint.close()

    def deinit(self):
        pass

    def set_hostname(self, hostname, port, ip_flags):
        self.address.set_hostname(hostname, port, ip_flags)

    def set_addr(self, addr):
        self.address.set(addr)

    def send(self, reliable, command, data, size):
        print("client send", reliable, command, data, size)
        if command + packet.RUDP_CMD_APP > 255:
            return None
        if not self.connected:
            return None

        if reliable:
            return None
        else:
            return None
