from detectserver import detect
from rudp.client import client, client_handler
from event_loop import event_loop
from rudp.rudp import rudp


def handle_packet(cl, cmd, data):
    print("handle packet")


def link_info(cl, info):
    pass


def connected(cl):
    print("connected")


def server_lost(cl):
    print("disconnected")


my_handler = client_handler(handle_packet, link_info, connected,
                            server_lost)

freebox = detect()
print(freebox.address, freebox.port)

evtloop = event_loop()
r = rudp(evtloop)

c = client(r, my_handler)
c.set_addr((freebox.address, freebox.port))
c.connect()

r.evtloop.loop()
