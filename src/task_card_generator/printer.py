"""Thermal printer functionality."""

from escpos.printer import Win32Raw, Usb
import platform

from src.util.common import get_printer_type


def print_to_thermal_printer(image_path):
    """Print image to thermal printer."""
    try:
        # Initialize printer
        printer = get_printer_type()

        # Print the image
        printer.image(image_path, impl="bitImageColumn", center=True)

        # Cut the paper
        printer.cut()

        print("Successfully printed to thermal printer!")

    except Exception as e:
        print(f"ERROR printing to thermal printer: {str(e)}")
