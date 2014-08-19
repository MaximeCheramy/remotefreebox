import socket


class address(object):
    def __init__(self):
        self.port = 0
        self.hostname = None
        self.resolver_state = None

    def set_hostname(self, hostname, port, ip_flags):
        if hostname is None:
            return None
        self.port = port
        self.hostname = hostname
        s = socket.getaddrinfo(hostname, None)
        self.resolver_state = 'done' if s else 'error'

    def set(self, addr):
        self.set_ipv4(addr[0], addr[1])

    def set_ipv4(self, in_addr, port):
        self.resolver_state = 'addr'
        self.port = port
        self.addr = in_addr

    def get(self):
        if self.resolver_state == 'addr' or self.resolver_state == 'done':
            return (self.addr, self.port)
        return None
