from zeroconf import ServiceBrowser, Zeroconf
import socket
import time

# Author: 1337Woflpack.

servers = []


class Server(object):
    def __init__(self, address, port, name):
        self.address = address
        self.port = port
        self.name = name


class MyListener(object):
    # def addService(self, zeroconf, type, name):
    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        if info:
            servers.append(Server(socket.inet_ntoa(info.address),
                                  info.port, info.server))


def detect():
    zeroconf = Zeroconf()
    print("Browsing services...")
    listener = MyListener()
    ServiceBrowser(zeroconf, "_hid._udp.local.", listener=listener)
    freebox = None
    while not freebox:
        for server in servers:
            if 'Freebox' in server.name:
                freebox = server
        time.sleep(0.1)
    zeroconf.close()
    return freebox
