from . import address
from . import packet
import socket


class endpoint_handler(object):
    def __init__(self, handle_packet):
        self.handle_packet = handle_packet


class endpoint(object):
    def __init__(self, rudp, handler):
        self.rudp = rudp
        self.handler = handler
        self.socket = None
        self.address = address.address()

    def bind(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.rudp.evtloop.add_object(self.socket, self._handle_incoming)
        addr = self.address.get()
        print("bind sur ", addr)
        self.socket.bind(addr)

    def close(self):
        pass

    def set_addr(self, addr):
        self.address.set(addr)

    def send(self, addr, data):
        print("send", data, addr)
        self.socket.sendto(data, addr)

    def _handle_incoming(self):
        print("handle incoming")
        data, addr = self.socket.recvfrom(4096)
        pc = packet.data_to_packet(data)
        self.handler.handle_packet(addr, pc)
