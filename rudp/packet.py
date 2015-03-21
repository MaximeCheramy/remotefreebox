from struct import pack, unpack


RUDP_CMD_NOOP = 0
RUDP_CMD_CLOSE = 1
RUDP_CMD_CONN_REQ = 2
RUDP_CMD_CONN_RSP = 3
RUDP_CMD_PING = 4
RUDP_CMD_PONG = 5
RUDP_CMD_APP = 0x10

RUDP_OPT_RELIABLE = 1
RUDP_OPT_ACK = 2
RUDP_OPT_RETRANSMITTED = 4


class packet_header(object):
    def __init__(self, cmd=RUDP_CMD_NOOP, opt=0, reliable_ack=0, reliable=0,
                 unreliable=0):
        self.command = cmd
        self.opt = opt
        self.reliable_ack = reliable_ack
        self.reliable = reliable
        self.unreliable = unreliable

    def get_header(self):
        return pack('!BBHHH', self.command, self.opt, self.reliable_ack,
                    self.reliable, self.unreliable)


class packet_conn_req(object):
    def __init__(self, header=None):
        if header is None:
            self.header = packet_header(cmd=RUDP_CMD_CONN_REQ)
        else:
            self.header = header
        self.data = 0

    def raw(self):
        return self.header.get_header() + pack('!I', self.data)


class packet_conn_rsp(object):
    def __init__(self, header=None):
        if header is None:
            self.header = packet_header(cmd=RUDP_CMD_CONN_RSP)
        else:
            self.header = header
        self.data = 0

    def raw(self):
        return self.header.get_header() + pack('!I', self.data)


class packet_data(object):
    def __init__(self, header=None, data=bytes()):
        if header is None:
            self.header = packet_header()
        else:
            self.header = header
        self.data = data

    def raw(self):
        return self.header.get_header() + self.data


def data_to_packet(data):
    cmd, opt, reliable_ack, reliable, unreliable = unpack('!BBHHH', data[:8])
    header = packet_header(cmd, opt, reliable_ack, reliable, unreliable)
    if header.command == RUDP_CMD_CONN_RSP:
        return packet_conn_rsp(header)
    if header.command == RUDP_CMD_CONN_REQ:
        return packet_conn_req(header)
    else:
        return packet_data(header, data[8:])

def command_to_string(command):
    d = { "RUDP_CMD_NOOP": 0, "RUDP_CMD_CLOSE": 1, "RUDP_CMD_CONN_REQ": 2,
          "RUDP_CMD_CONN_RSP": 3, "RUDP_CMD_PING": 4, "RUDP_CMD_PONG": 5,
          "RUDP_CMD_APP": 0x10 }
    for cmd, v in d.items():
        if v == command:
            return cmd
    return "<unknown>"