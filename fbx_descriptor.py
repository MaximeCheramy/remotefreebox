from rudp_hid_client import foils_hid_device_descriptor


unicode_report_descriptor = bytes([
    0x05, 0x01,         #   Usage Page (Desktop),
    0x09, 0x06,         #   Usage (Keyboard),

    0xA1, 0x01,         #   Collection (Application),
    0x85, 0x01,         #       Report ID (1),
    0x05, 0x10,         #       Usage Page (Unicode),
    0x08,               #       Usage (00h),
    0x95, 0x01,         #       Report Count (1),
    0x75, 0x20,         #       Report Size (32),
    0x14,               #       Logical Minimum (0),
    0x27, 0xFF, 0xFF, 0xFF,  #       Logical Maximum (2**24-1),
    0x81, 0x62,         #       Input (Variable, No pref state, No Null Pos),
    0xC0,               #   End Collection

    0xA1, 0x01,         #   Collection (Application),
    0x85, 0x02,         #       Report ID (2),
    0x95, 0x01,         #       Report Count (1),
    0x75, 0x08,         #       Report Size (8),
    0x15, 0x00,         #       Logical Minimum (0),
    0x26, 0xFF, 0x00,   #       Logical Maximum (255),
    0x05, 0x07,         #       Usage Page (Keyboard),
    0x19, 0x00,         #       Usage Minimum (None),
    0x2A, 0xFF, 0x00,   #       Usage Maximum (FFh),
    0x80,               #       Input,
    0xC0,               #   End Collection

    0x05, 0x0C,         #  Usage Page (Consumer),
    0x09, 0x01,         #  Usage (Consumer Control),
    0xA1, 0x01,         #  Collection (Application),
    0x85, 0x03,         #   Report ID (3),
    0x95, 0x01,         #   Report Count (1),
    0x75, 0x10,         #   Report Size (16),
    0x19, 0x00,         #   Usage Minimum (Consumer Control),
    0x2A, 0x8C, 0x02,   #   Usage Maximum (AC Send),
    0x15, 0x00,         #   Logical Minimum (0),
    0x26, 0x8C, 0x02,   #   Logical Maximum (652),
    0x80,               #   Input,
    0xC0,               #  End Collection,

    0x05, 0x01,         #  Usage Page (Desktop),
    0x0a, 0x80, 0x00,   #  Usage (System Control),
    0xA1, 0x01,         #  Collection (Application),
    0x85, 0x04,         #   Report ID (4),
    0x75, 0x01,         #   Report Size (1),
    0x95, 0x04,         #   Report Count (4),
    0x1a, 0x81, 0x00,   #   Usage Minimum (System Power Down),
    0x2a, 0x84, 0x00,   #   Usage Maximum (System Context menu),
    0x81, 0x02,         #   Input (Variable),
    0x75, 0x01,         #   Report Size (1),
    0x95, 0x04,         #   Report Count (4),
    0x81, 0x01,         #   Input (Constant),
    0xC0,               #  End Collection,
])

fbx_foils_hid_device_descriptor = foils_hid_device_descriptor(
    b"Unicode", 0x100, unicode_report_descriptor, b"", b"")
