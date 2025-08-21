import platform
from escpos.printer import Win32Raw, Usb
from .constants import *

def get_font_path_by_system():
    system = platform.system()
    if system == "Linux":
        return LINUX_FONT_PATHS
    elif system == "Windows":
        return WINDOWS_FONT_PATHS
    elif system == "Darwin":
        # Define ur own shit I use linux
        pass

def get_font_name_and_font_path():
    system = platform.system()
    if system == "Linux":
        return [
            ("NotoSans", LINUX_FONT_PATHS[0]),
            ("NotoSansEmoji", LINUX_FONT_PATHS[1]),
        ]
    elif system == "Windows":
        return [
            ("SegoeUIEmoji", WINDOWS_FONT_PATHS[0]),
            ("SegoeUIEmoji", WINDOWS_FONT_PATHS[1]),
            ("SegoeUISymbol", WINDOWS_FONT_PATHS[2]),
        ]

def get_wkhtml_path_by_system():
    system = platform.system()
    if system == "Linux":
        return LINUX_WKHTMLTOPDF_POSSIBLE_PATHS
    elif system == "Windows":
        return WINDOWS_WKHTMLTOPDF_POSSIBLE_PATHS
    elif system == "Darwin":
        # Define ur own shit I use linux
        pass

def get_printer_type():
    system = platform.system()
    if system == "Linux":
        return Usb(0x0483, 0x070b, 0)
    elif system == "Windows":
        return Win32Raw("Your printer fucking name here")
    else:
        raise OSError(f"Unsupported system: {system}")

    