#/usr/bin/python3

import sys
from threading import Thread

from .detectserver import detect
from .rudp.client import client_handler
from .event_loop import event_loop
from .rudp.rudp import rudp
from .rudp_hid_client import rudp_hid_client
from .fbx_descriptor import fbx_foils_hid_device_descriptor, fbx_get_command


def info(s):
    print(s, file=sys.stderr)

def success(s):
    print(s, file=sys.stderr)


class FreeboxController(object):
    def __init__(self):
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

        def handle_packet(cl, cmd, data):
            info("handle packet main.py (%s %s %s)" % (cl, cmd, data))

        def link_info(cl, info_):
            info("link_info %s %s" % (cl, info_))

        def connected(cl):
            info("connected %s" % cl)

        def server_lost(cl):
            info("server_lost %s" % cl)

        my_handler = client_handler(handle_packet, link_info, connected,
                                    server_lost)
        self.client = rudp_hid_client(r, my_handler, fb_addr)
        self.client.setup_device(fbx_foils_hid_device_descriptor)

    def press(self, key):
        info("pressing %s" % key)
        self.client.send_command(*fbx_get_command(key))
