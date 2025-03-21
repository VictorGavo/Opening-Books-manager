# Handles daily notes creation and updates
import os
import logging
import datetime
from src.handlers.markdown_handler import (
    create_daily_note_from_sod,
    update_daily_note_with_eod,
    read_file_content,
    format_date
)
from src.handlers.drive_handler import DriveHandler
from config.config import DAILY_NOTES_FOLDER, DAILY_TEMPLATE_PATH, GOOGLE_DRIVE_CREDENTIALS

# Set up logging
logger = logging.getLogger(__name__)

class DailyNotesHandler:
    """
    Handles the creation and updating of daily notes.
    """
    
    def __init__(self):
        """
        Initializes the DailyNotesHandler.
        """
        self.drive_handler = DriveHandler(GOOGLE_DRIVE_CREDENTIALS)
        self.template_path = DAILY_TEMPLATE_PATH
        self.folder_path = DAILY_NOTES_FOLDER
    
    def process_sod_form(self, form_data, date_str=None):
        """
        Processes SOD form data and creates a daily note.
        
        Args:
            form_data: Dictionary containing SOD form data
            date_str: Date string for the note (defaults to today)
            
        Returns:
            tuple: (bool, str) - (Success status, File ID or error message)
        """
        try:
            if date_str is None:
                date_str = format_date()
            
            logger.info(f"Processing SOD form data for {date_str}")
            
            # Generate markdown content from SOD form data
            content = create_daily_note_from_sod(form_data, self.template_path, date_str)
            if not content:
                return False, "Failed to generate markdown content"
            
            # Create or update the daily note in Google Drive
            success, result = self.drive_handler.create_or_update_daily_note(
                date_str, content, self.folder_path
            )
            
            if success:
                logger.info(f"Successfully created daily note for {date_str}")
                return True, result
            else:
                logger.error(f"Failed to create daily note for {date_str}: {result}")
                return False, result
        except Exception as e:
            logger.error(f"Error processing SOD form data: {e}")
            return False, str(e)
    
    def process_eod_form(self, form_data, date_str=None):
        """
        Processes EOD form data and updates a daily note.
        
        Args:
            form_data: Dictionary containing EOD form data
            date_str: Date string for the note (defaults to today)
            
        Returns:
            tuple: (bool, str) - (Success status, File ID or error message)
        """
        try:
            if date_str is None:
                date_str = format_date()
            
            logger.info(f"Processing EOD form data for {date_str}")
            
            # Find the daily note in Google Drive
            folder_id = self.drive_handler.find_folder(self.folder_path)
            if not folder_id:
                return False, "Failed to find daily notes folder"
            
            file_name = f"{date_str}.md"
            existing_file = self.drive_handler.find_file(file_name, folder_id)
            
            if not existing_file:
                logger.warning(f"Daily note for {date_str} not found, creating new note")
                # If the note doesn't exist, create a new one with empty SOD data
                return self.process_sod_form({}, date_str)
            
            # Read the existing content
            existing_content = self.drive_handler.read_file(existing_file['id'])
            if not existing_content:
                return False, "Failed to read existing daily note"
            
            # Update the content with EOD form data
            updated_content = update_daily_note_with_eod(form_data, existing_content, date_str)
            if not updated_content:
                return False, "Failed to update markdown content"
            
            # Update the daily note in Google Drive
            success = self.drive_handler.update_file(existing_file['id'], updated_content)
            
            if success:
                logger.info(f"Successfully updated daily note for {date_str}")
                return True, existing_file['id']
            else:
                logger.error(f"Failed to update daily note for {date_str}")
                return False, "Failed to update daily note"
        except Exception as e:
            logger.error(f"Error processing EOD form data: {e}")
            return False, str(e)
