from struct import pack, unpack
from rudp.client import client, client_handler
from log import warning, info
from time import sleep


FOILS_HID_DEVICE_NEW = 0
FOILS_HID_DEVICE_DROPPED = 1
FOILS_HID_DEVICE_OPEN = 2
FOILS_HID_DEVICE_CLOSE = 3
FOILS_HID_FEATURE = 4
FOILS_HID_DATA = 5
FOILS_HID_GRAB = 6
FOILS_HID_RELEASE = 7
FOILS_HID_FEATURE_SOLLICIT = 8


def round_up(x):
    return (x + 3) & ~3


class foils_hid_device_descriptor(object):
    def __init__(self, name, version, descriptor, physical, strings):
        self.name = name
        self.version = version
        self.descriptor = descriptor
        self.descriptor_size = len(descriptor)
        self.physical = physical
        self.physical_size = len(physical)
        self.strings = strings
        self.strings_size = len(strings)


class foils_hid_header(object):
    def __init__(self, device_id=0, report_id=0):
        self.device_id = device_id
        self.report_id = report_id

    def raw(self):
        return pack('!II', self.device_id, self.report_id)


class foils_hid_device_new(object):
    def __init__(self, name, serial, version, descriptor_offset, descriptor_size,
                 physical_offset, physical_size, strings_offset, strings_size):
        self.name = name
        self.serial = serial
        self.zero = 0
        self.version = version
        self.descriptor_offset = descriptor_offset
        self.descriptor_size = descriptor_size
        self.physical_offset = physical_offset
        self.physical_size = physical_size
        self.strings_offset = strings_offset
        self.strings_size = strings_size

    def raw(self):
        return pack('!64s32sHHHHHHHH', self.name, self.serial, self.zero,
                    self.version, self.descriptor_offset, self.descriptor_size,
                    self.physical_offset, self.physical_size,
                    self.strings_offset, self.strings_size)


class rudp_hid_client(object):
    # create rudp client with proper address
    # set handlers
    def __init__(self, rudp, hid_handler, addr):
        self.state = "none"
        self.rudp = rudp
        self.handler = hid_handler
        base_handler = client_handler(self.handle_packet,
                                      self.handler.link_info,
                                      self.handler.connected,
                                      self.handler.server_lost)
        self.base = client(rudp, base_handler)
        self.base.set_addr(addr)
        self.reports_listening = set()

    def setup_device(self, desc):
        info("setup_device")
        self.base.connect()
        info("connect called")
        while not self.base.connected:
            sleep(0.1)
        info("connected, calling device_new")
        self.device_new(desc)
        info("device_new called")

    def device_new(self, desc, device_id=0):
        header = foils_hid_header(device_id)

        descriptor_size = round_up(desc.descriptor_size)
        physical_size = round_up(desc.physical_size)

        dev = foils_hid_device_new(
            desc.name, b'', desc.version, 112, desc.descriptor_size,
            112 + descriptor_size, desc.physical_size, 112 +
            descriptor_size + physical_size, desc.strings_size)

        data = pack('!{}s{}s{}s'.format(descriptor_size, physical_size,
                                        desc.strings_size + 8),
                    desc.descriptor, desc.physical, desc.strings)

        packet = header.raw() + dev.raw() + data
        self.base.send(1, FOILS_HID_DEVICE_NEW, packet)

    def handle_packet(self, cl, cmd, data):
        command = cmd - 0x10  # user packet, update command
        _, report_id = unpack("!II", data)
        if command == FOILS_HID_DEVICE_OPEN:
            self.state = "open"
        elif command == FOILS_HID_DEVICE_CLOSE:
            self.state = "closed"
        elif command == FOILS_HID_GRAB:
            self.reports_listening.add(report_id)
            info("(grab) list is now %s" % self.reports_listening)
        elif command == FOILS_HID_RELEASE:
            self.reports_listening.remove(report_id)
            info("(rel) list is now %s" % self.reports_listening)
        else:
            self.handler.handle_packet(cl, cmd, data)

    def device_drop(self, device_id):
        header = foils_hid_header(device_id)
        self.base.send(1, FOILS_HID_DEVICE_DROPPED, header)

    def feature_report_send(self, device_id, report_id, reliable, data):
        header = pack('!IB{}s'.format(len(data)), device_id, report_id, data)
        self.base.send(reliable, FOILS_HID_FEATURE, header)

    def input_report_send(self, device_id, report_id, reliable, data):
        header = pack('!IB{}s'.format(len(data)), device_id, report_id, data)
        self.base.send(reliable, FOILS_HID_FEATURE, header)

    # size of code is number of bits of the code (8, 16, 32)
    def send_command(self, report, code, size_of_code):
        self.header = foils_hid_header(0, report)
        pack_format = '!I'
        if size_of_code == 16:
            pack_format = '<H'
        elif size_of_code == 8:
            pack_format = '!B'

        data = self.header.raw() + pack(pack_format, code)
        self.base.send(1, FOILS_HID_DATA, data)

        # send empty command too
        data = self.header.raw() + pack(pack_format, 0)
        self.base.send(1, FOILS_HID_DATA, data)
