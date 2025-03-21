# Main scirpt to orchestrate the process
from config.config import SOD_ID
from src.handlers.forms_handler import get_form_responses
from src.handlers.keep_handler import create_keep_note
from src.utils.utils import setup_logging
import logging

logger = setup_logging()

def main():
    logger.info("Starting the process...")

    try:
        # 1. Fetch data from the SOD G.Form
        sod_responses = get_form_responses(SOD_ID)

        if sod_responses:
            # 2. Process the form data and create a Keep note
            note_title = "[YYYY.MM.dd]"
            note_body = str("[PLACEHOLDER NOTE BODY CONTENT]")
            create_keep_note(note_title, note_body)

            logger.info("Successfully created a daily note.")
        else:
            logger.warning("No responses found in the morning form.")

    except Exception as e:
        logger.exception(f"An error occured: {e}")
    
    logger.info("Process completed.")

if __name__ == "__main__":
    main()
