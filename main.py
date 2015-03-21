#/usr/bin/python3

import sys
from detectserver import detect
from rudp.client import client, client_handler
from event_loop import event_loop, event_source
from rudp.rudp import rudp
from rudp_hid_client import FOILS_HID_DATA
import socket
from threading import Lock, Thread
from getch import getch
from rudp_hid_client import foils_hid_header, rudp_hid_client
from fbx_descriptor import fbx_foils_hid_device_descriptor, fbx_get_command
from rudp.packet import RUDP_CMD_APP
from log import success, log, info

def handle_packet(cl, cmd, data):
    info("handle packet main.py (%s %s %s)" % (cl, cmd, data))


def link_info(cl, info):
    info("link_info %s %s" % (cl, info))


def connected(cl):
    info("connected %s" % cl)
    print("connected")


def server_lost(cl):
    info("server_lost %s" % cl)
    print("disconnected")


assert sys.version_info.major >= 3, "Needs at least Python 3"

# find freebox
freebox = detect()
success("%s found at %s:%s" % (freebox.name, freebox.address, freebox.port))
fb_addr = (freebox.address, freebox.port)

# rudp event loop
evtloop = event_loop()
r = rudp(evtloop)
loop_thread = Thread(target=r.evtloop.loop)
loop_thread.daemon = True
loop_thread.start()

# create client
my_handler = client_handler(handle_packet, link_info, connected,
                            server_lost)
c = rudp_hid_client(r, my_handler, fb_addr)
c.setup_device(fbx_foils_hid_device_descriptor)

#print("=== Press ESC to quit ===")
#print("Z: send key")
while True:
    ch = getch()
    if ord(ch) == 27:
        break
    elif ch == '-':
        info("Sending -")
        c.send_command(*fbx_get_command("Vol-"))
