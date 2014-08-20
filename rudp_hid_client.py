from struct import pack
from rudp.client import client


FOILS_HID_DEVICE_NEW = 0
FOILS_HID_DEVICE_DROPPED = 1
FOILS_HID_DEVICE_CREATED = 2
FOILS_HID_DEVICE_CLOSE = 3
FOILS_HID_FEATURE = 4
FOILS_HID_DATA = 5
FOILS_HID_GRAB = 6
FOILS_HID_RELEASE = 7
FOILS_HID_FEATURE_SOLLICIT = 8


def round_up(x):
    return (x + 3) & ~3


class foils_hid_header(object):
    def __init__(self, device_id=0, report_id=0):
        self.device_id = device_id
        self.report_id = report_id


class foils_hid_device_new(object):
    def __init__(self, name, serial, descriptor_offset, descriptor_size,
                 physical_offset, physical_size, strings_offset, strings_size):
        self.name = name
        self.serial = serial
        self.zero = 0
        self.version = 1
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
    def __init__(self, rudp, handler):
        self.rudp = rudp
        self.handler = handler
        self.base = client(rudp, handler)

    def device_new(self, desc, device_id):
        header = foils_hid_header(device_id)

        descriptor_size = round_up(desc.descriptor_size)
        physical_size = round_up(desc.physical_size)

        dev = foils_hid_device_new(
            desc.name, desc.serial, 112,
            desc.descriptor_size, 112 + descriptor_size, desc.physical_size, 112 +
            descriptor_size + physical_size, desc.strings_size)

        data = pack('!{}s{}s{}s'.format(descriptor_size, physical_size,
                                        desc.strings_size + 8),
                    desc.descriptor, desc.physical, desc.strings)

        packet = header.raw() + dev.raw() + data

        self.base.send(1, FOILS_HID_DEVICE_NEW, packet, len(packet))

    def device_drop(self, device_id):
        header = foils_hid_header(device_id)
        self.base.send(1, FOILS_HID_DEVICE_DROPPED, header)
