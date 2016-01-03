from .rudp_hid_client import foils_hid_device_descriptor


unicode_report_descriptor = bytes([
    0x05, 0x01,              # Usage Page (Desktop),
    0x09, 0x06,              # Usage (Keyboard),

    0xA1, 0x01,              # Collection (Application),
    0x85, 0x01,              # . Report ID (1),
    0x05, 0x10,              # . Usage Page (Unicode),
    0x08,                    # . Usage (00h),
    0x95, 0x01,              # . Report Count (1),
    0x75, 0x20,              # . Report Size (32),
    0x14,                    # . Logical Minimum (0),
    0x27, 0xFF, 0xFF, 0xFF,  # . Logical Maximum (2**24-1),
    0x81, 0x62,              # . Input (Variable, No pref state, No Null Pos),
    0xC0,                    # End Collection

    0xA1, 0x01,              # Collection (Application),
    0x85, 0x02,              # . Report ID (2),
    0x95, 0x01,              # . Report Count (1),
    0x75, 0x08,              # . Report Size (8),
    0x15, 0x00,              # . Logical Minimum (0),
    0x26, 0xFF, 0x00,        # . Logical Maximum (255),
    0x05, 0x07,              # . Usage Page (Keyboard),
    0x19, 0x00,              # . Usage Minimum (None),
    0x2A, 0xFF, 0x00,        # . Usage Maximum (FFh),
    0x80,                    # . Input,
    0xC0,                    # End Collection

    0x05, 0x0C,              # Usage Page (Consumer),
    0x09, 0x01,              # Usage (Consumer Control),
    0xA1, 0x01,              # Collection (Application),
    0x85, 0x03,              # . Report ID (3),
    0x95, 0x01,              # . Report Count (1),
    0x75, 0x10,              # . Report Size (16),
    0x19, 0x00,              # . Usage Minimum (Consumer Control),
    0x2A, 0x8C, 0x02,        # . Usage Maximum (AC Send),
    0x15, 0x00,              # . Logical Minimum (0),
    0x26, 0x8C, 0x02,        # . Logical Maximum (652),
    0x80,                    # . Input,
    0xC0,                    # End Collection,

    0x05, 0x01,              # Usage Page (Desktop),
    0x0a, 0x80, 0x00,        # Usage (System Control),
    0xA1, 0x01,              # Collection (Application),
    0x85, 0x04,              # . Report ID (4),
    0x75, 0x01,              # . Report Size (1),
    0x95, 0x04,              # . Report Count (4),
    0x1a, 0x81, 0x00,        # . Usage Minimum (System Power Down),
    0x2a, 0x84, 0x00,        # . Usage Maximum (System Context menu),
    0x81, 0x02,              # . Input (Variable),
    0x75, 0x01,              # . Report Size (1),
    0x95, 0x04,              # . Report Count (4),
    0x81, 0x01,              # . Input (Constant),
    0xC0,                    # End Collection,
])

fbx_foils_hid_device_descriptor = foils_hid_device_descriptor(
    b"Unicode", 0x100, unicode_report_descriptor, b"", b"")

TARGET_UNICODE = 1
TARGET_KEYBOARD = 2
TARGET_CONSUMER = 3
TARGET_DESKTOP = 4
fbx_targets_list = [TARGET_UNICODE, TARGET_KEYBOARD, TARGET_CONSUMER, TARGET_DESKTOP]

DC_SYSTEM_POWER_DOWN = 0x01
DC_SYSTEM_POWER_SLEEP = 0x02
DC_SYSTEM_POWER_WAKEUP = 0x04
DC_SYSTEM_CONTEXT_MENU = 0x08

HID_KEYBOARD_A = 0x04
HID_KEYBOARD_ENTER = 0x28
HID_KEYBOARD_BACKSPACE = 0x2A
HID_KEYBOARD_TAB = 0x2B
HID_KEYBOARD_RIGHTARROW = 0x4F
HID_KEYBOARD_LEFTARROW = 0x50
HID_KEYBOARD_DOWNARROW = 0x51
HID_KEYBOARD_UPARROW = 0x52
HID_KEYBOARD_HOME = 0x4A
HID_KEYBOARD_POWER = 0x66
HID_KEYBOARD_F1 = 0x3A
HID_KEYBOARD_KEYPAD_1 = 0x59
HID_KEYBOARD_KEYPAD_2 = 0x5A
HID_KEYBOARD_KEYPAD_3 = 0x5B
HID_KEYBOARD_KEYPAD_4 = 0x5C
HID_KEYBOARD_KEYPAD_5 = 0x5D
HID_KEYBOARD_KEYPAD_6 = 0x5E
HID_KEYBOARD_KEYPAD_7 = 0x5F
HID_KEYBOARD_KEYPAD_8 = 0x60
HID_KEYBOARD_KEYPAD_9 = 0x61
HID_KEYBOARD_KEYPAD_0 = 0x62

HID_CONSUMER_POWER = 0x30
HID_CONSUMER_MENU = 0x40
HID_CONSUMER_DATA_ON_SCREEN = 0x60
HID_CONSUMER_VCR_TV = 0x63
HID_CONSUMER_SUB_CHANNEL_INCREMENT = 0x171
HID_CONSUMER_ALTERNATE_AUDIO_INCREMENT = 0x173
HID_CONSUMER_ALTERNATE_SUBTITLE_INCREMENT = 0x175
HID_CONSUMER_CHANNEL_INCREMENT = 0x9c
HID_CONSUMER_CHANNEL_DECREMENT = 0x9d
HID_CONSUMER_PLAY_PAUSE = 0xcd
HID_CONSUMER_PLAY = 0xb0
HID_CONSUMER_PAUSE = 0xb1
HID_CONSUMER_RECORD = 0xb2
HID_CONSUMER_FAST_FORWARD = 0xb3
HID_CONSUMER_REWIND = 0xb4
HID_CONSUMER_SCAN_NEXT_TRACK = 0xb5
HID_CONSUMER_SCAN_PREVIOUS_TRACK = 0xb6
HID_CONSUMER_STOP = 0xb7
HID_CONSUMER_EJECT = 0xb8
HID_CONSUMER_MUTE = 0xe2
HID_CONSUMER_VOLUME_INCREMENT = 0xe9
HID_CONSUMER_VOLUME_DECREMENT = 0xea
HID_CONSUMER_RANDOM_PLAY = 0xb9

HID_CONSUMER_BROWSER_BACK = 0x224
HID_CONSUMER_BROWSER_FORWARD = 0x225
HID_CONSUMER_BROWSER_REFRESH = 0x227
HID_CONSUMER_BROWSER_STOP = 0x226

HID_CONSUMER_AC_ZOOM_IN = 0x22d
HID_CONSUMER_AC_ZOOM_OUT = 0x22e

HID_CONSUMER_AC_SEARCH = 0x221
HID_CONSUMER_AC_PROPERTIES = 0x209
HID_CONSUMER_AC_EXIT = 0x204

HID_CONSUMER_AL_TASK_MANAGER = 0x18f
HID_CONSUMER_AL_INTERNET_BROWSER = 0x196
HID_CONSUMER_AL_AUDIO_BROWSER = 0x1b7

HID_DESKTOP_MENU = 0x86

# Documentation available here:
# http://dev.freebox.fr/sdk/freebox_player_1.1.4_codes.html
fbx_target_command_codes = {
    # Remote control emulation
    "Power": (TARGET_CONSUMER, HID_CONSUMER_POWER),
    "AV": (TARGET_CONSUMER, HID_CONSUMER_VCR_TV),
    "0": (TARGET_KEYBOARD, HID_KEYBOARD_KEYPAD_0),
    "1": (TARGET_KEYBOARD, HID_KEYBOARD_KEYPAD_1),
    "2": (TARGET_KEYBOARD, HID_KEYBOARD_KEYPAD_2),
    "3": (TARGET_KEYBOARD, HID_KEYBOARD_KEYPAD_3),
    "4": (TARGET_KEYBOARD, HID_KEYBOARD_KEYPAD_4),
    "5": (TARGET_KEYBOARD, HID_KEYBOARD_KEYPAD_5),
    "6": (TARGET_KEYBOARD, HID_KEYBOARD_KEYPAD_6),
    "7": (TARGET_KEYBOARD, HID_KEYBOARD_KEYPAD_7),
    "8": (TARGET_KEYBOARD, HID_KEYBOARD_KEYPAD_8),
    "9": (TARGET_KEYBOARD, HID_KEYBOARD_KEYPAD_9),
    "Up": (TARGET_KEYBOARD, HID_KEYBOARD_UPARROW),
    "Down": (TARGET_KEYBOARD, HID_KEYBOARD_DOWNARROW),
    "Left": (TARGET_KEYBOARD, HID_KEYBOARD_LEFTARROW),
    "Right": (TARGET_KEYBOARD, HID_KEYBOARD_RIGHTARROW),
    "Enter": (TARGET_KEYBOARD, HID_KEYBOARD_ENTER),
    "Back": (TARGET_CONSUMER, HID_CONSUMER_AC_EXIT),
    "Search": (TARGET_CONSUMER, HID_CONSUMER_AC_SEARCH),
    "Menu": (TARGET_CONSUMER, HID_CONSUMER_MENU),
    "Info": (TARGET_CONSUMER, HID_CONSUMER_AC_PROPERTIES),
    "Free": (TARGET_CONSUMER, HID_CONSUMER_AL_TASK_MANAGER),
    "Vol-": (TARGET_CONSUMER, HID_CONSUMER_VOLUME_DECREMENT),
    "Vol+": (TARGET_CONSUMER, HID_CONSUMER_VOLUME_INCREMENT),
    "Mute": (TARGET_CONSUMER, HID_CONSUMER_MUTE),
    "Record": (TARGET_CONSUMER, HID_CONSUMER_RECORD),
    "Chan+": (TARGET_CONSUMER, HID_CONSUMER_CHANNEL_INCREMENT),
    "Chan-": (TARGET_CONSUMER, HID_CONSUMER_CHANNEL_DECREMENT),
    "Rewind": (TARGET_CONSUMER, HID_CONSUMER_REWIND),
    "Play/Pause": (TARGET_CONSUMER, HID_CONSUMER_PLAY_PAUSE),
    "Fast Forward": (TARGET_CONSUMER, HID_CONSUMER_FAST_FORWARD),

    # Additional keys
    "Backspace": (TARGET_KEYBOARD, HID_KEYBOARD_BACKSPACE),
    "Stream debug": (TARGET_CONSUMER, HID_CONSUMER_DATA_ON_SCREEN),
    "Stop": (TARGET_CONSUMER, HID_CONSUMER_STOP),
    "Play": (TARGET_CONSUMER, HID_CONSUMER_PLAY),
    "Random Play": (TARGET_CONSUMER, HID_CONSUMER_RANDOM_PLAY),
    "Previous track": (TARGET_CONSUMER, HID_CONSUMER_SCAN_PREVIOUS_TRACK),
    "Next track": (TARGET_CONSUMER, HID_CONSUMER_SCAN_NEXT_TRACK),
    "Zoom+": (TARGET_CONSUMER, HID_CONSUMER_AC_ZOOM_IN),
    "Zoom-": (TARGET_CONSUMER, HID_CONSUMER_AC_ZOOM_OUT),
    "Browser Back": (TARGET_CONSUMER, HID_CONSUMER_BROWSER_BACK),
    "Browser Forward": (TARGET_CONSUMER, HID_CONSUMER_BROWSER_FORWARD),
    "Browser Refresh": (TARGET_CONSUMER, HID_CONSUMER_BROWSER_REFRESH),
    "Browser Stop": (TARGET_CONSUMER, HID_CONSUMER_BROWSER_STOP),
    "Video Track": (TARGET_CONSUMER, HID_CONSUMER_SUB_CHANNEL_INCREMENT),
    "Audio Track": (TARGET_CONSUMER, HID_CONSUMER_ALTERNATE_AUDIO_INCREMENT),
    "Subtitle Track": (TARGET_CONSUMER, HID_CONSUMER_ALTERNATE_SUBTITLE_INCREMENT),
    "System Sleep": (TARGET_DESKTOP, DC_SYSTEM_POWER_SLEEP),
    "System Wakeup": (TARGET_DESKTOP, DC_SYSTEM_POWER_WAKEUP),
    "Eject": (TARGET_CONSUMER, HID_CONSUMER_EJECT),
    "Tab": (TARGET_KEYBOARD, HID_KEYBOARD_TAB),
    "Power/kbd": (TARGET_KEYBOARD, HID_KEYBOARD_POWER),
    "Context Menu": (TARGET_DESKTOP, DC_SYSTEM_CONTEXT_MENU),
    "AL Internet Browser": (TARGET_CONSUMER, HID_CONSUMER_AL_INTERNET_BROWSER)
}


def fbx_get_command(command_text):
    if command_text in fbx_target_command_codes:
        target, code = fbx_target_command_codes[command_text]
        size_of_code = 32
        if target == TARGET_CONSUMER:
            size_of_code = 16
        elif target == TARGET_KEYBOARD or target == TARGET_DESKTOP:
            size_of_code = 8
        return target, code, size_of_code
    else:
        raise Exception("Unknown command.")
