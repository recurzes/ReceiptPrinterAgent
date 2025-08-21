"""Main entry point when running as module."""

from .ai_client import get_task_from_ai, parse_ai_response
from .image_generator import create_task_image
from .pdf_generator import create_task_pdf
from .printer import print_to_thermal_printer


def main():
    """Main application entry point."""
    print("*" * 50)
    print("AI TASK GENERATOR".center(50))
    print("Turn your tasks into beautiful cards!".center(50))
    print("*" * 50)

    # Get user task description
    # print("\nDescribe the task you need to complete:")
    # print("-" * 40)
    # task_description = input(">> Enter task description: ")

    # if not task_description.strip():
    #     print("ERROR: Please enter a valid task description!")
    #     return

    # # Get AI response
    # print("\nProcessing with AI...")
    # ai_response = get_task_from_ai(task_description)

    # if not ai_response or ai_response.startswith("Error"):
    #     print(f"ERROR: {ai_response or 'Failed to get response'}")
    #     return

    # Parse AI response
    # task_data = parse_ai_response(ai_response)

    # print(f"\nGenerated Task: {task_data['title']}")
    # print(f"Priority: {task_data['priority']}")

    # Create PDF for viewing
    # pdf_path = create_task_pdf(task_data)

    # Create image for printing
    # image_path = create_task_image(task_data, save_temp=False)
    image_path = "/tmp/tmpjvzufbm7.png"

    if image_path:
        # Print to thermal printer
        print("\nPrinting to thermal printer...")
        print_to_thermal_printer(image_path)
    else:
        print("ERROR: Could not create image for printing")

    print("\n" + "=" * 50)
    print("TASK CARD GENERATION COMPLETE!")
    # if pdf_path:
    #     print(f"PDF saved: {pdf_path}")
    print("=" * 50)


if __name__ == "__main__":
    main()
