# Main script to orchestrate the process
from config.config import SOD_ID, EOD_ID
from src.handlers.forms_handler import get_form_responses
from src.handlers.keep_handler import create_keep_note
from src.handlers.daily_notes_handler import DailyNotesHandler
from src.utils.utils import setup_logging
import logging
import datetime

logger = setup_logging()

def main():
    logger.info("Starting the process...")
    
    # Initialize the daily notes handler
    daily_notes_handler = DailyNotesHandler()
    
    try:
        # 1. Fetch data from the SOD G.Form
        sod_responses = get_form_responses(SOD_ID)
        
        if sod_responses and len(sod_responses) > 0:
            # Get the most recent response
            sod_data = sod_responses[0]
            
            # 2. Process the form data and create a Keep note (keeping existing functionality)
            create_keep_note(sod_data)
            
            # 3. Create a daily note from SOD data and upload it to Google Drive
            success, result = daily_notes_handler.process_sod_form(sod_data)
            
            if success:
                logger.info(f"Successfully created a daily note in Google Drive: {result}")
            else:
                logger.error(f"Failed to create daily note in Google Drive: {result}")
        else:
            logger.warning("No responses found in the SOD form.")
        
        # 4. Fetch data from the EOD G.Form
        eod_responses = get_form_responses(EOD_ID)
        
        if eod_responses and len(eod_responses) > 0:
            # Get the most recent response
            eod_data = eod_responses[0]
            
            # 5. Update the daily note with EOD data
            success, result = daily_notes_handler.process_eod_form(eod_data)
            
            if success:
                logger.info(f"Successfully updated the daily note with EOD data: {result}")
            else:
                logger.error(f"Failed to update daily note with EOD data: {result}")
        else:
            logger.warning("No responses found in the EOD form.")
            
    except Exception as e:
        logger.exception(f"An error occurred: {e}")
    
    logger.info("Process completed.")

if __name__ == "__main__":
    main()
