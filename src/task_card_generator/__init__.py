"""Task Card Generator - AI-powered task card creation for thermal printers."""

__version__ = "1.0.0"
__author__ = "Your Name"

from .ai_client import get_task_from_ai, parse_ai_response, analyze_emails_for_tasks, parse_task_analysis
from .arcade_client import get_task_from_arcade_tool, authorize_arcade_tool, ArcadeTaskGenerator
from .image_generator import create_task_image
from .pdf_generator import create_task_pdf
from .printer import print_to_thermal_printer

__all__ = [
    "get_task_from_ai",
    "parse_ai_response",
    "analyze_emails_for_tasks",
    "parse_task_analysis", 
    "get_task_from_arcade_tool",
    "authorize_arcade_tool",
    "ArcadeTaskGenerator",
    "create_task_pdf",
    "create_task_image",
    "print_to_thermal_printer",
]
