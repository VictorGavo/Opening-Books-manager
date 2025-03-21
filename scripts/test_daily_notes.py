#!/usr/bin/env python3
"""
Test script for the daily notes functionality.

This script simulates form submissions to test the daily notes creation and updating
without having to submit actual Google Forms.
"""

import logging
import json
import datetime
from src.handlers.daily_notes_handler import DailyNotesHandler
from config.config import SOD_ID, EOD_ID

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def test_sod_form():
    """
    Test the SOD form processing.
    """
    logger.info("Testing SOD form processing...")
    
    # Create sample SOD form data
    sod_data = {
        "form_id": SOD_ID,
        "What am I looking forward to the most today?": "Testing the daily notes integration",
        "Today's Big 3": "1. Complete the daily notes integration\n2. Test the functionality\n3. Document the process",
        "3 things I'm grateful for in my life:": "Family, Health, Learning opportunities",
        "3 things I'm grateful about myself:": "Persistence, Creativity, Problem-solving skills",
        "I'm excited today for:": "Seeing the daily notes integration work",
        "One word to describe the person I want to be today would be __ because:": "Focused - because I want to complete this task efficiently",
        "Someone who needs me on my a-game today is:": "My future self who will use this system",
        "What's a potential obstacle/stressful situation for today and how would my best self deal with it?": "Technical issues - My best self would troubleshoot methodically and not get frustrated",
        "Someone I could surprise with a note, gift, or sign of appreciation is:": "A colleague who helped with a previous project",
        "One action I could take today to demonstrate excellence or real value is:": "Creating thorough documentation",
        "One bold action I could take today is:": "Sharing this project with others who might benefit",
        "An overseeing high performance coach would tell me today that:": "Focus on one step at a time and test thoroughly",
        "The big projects I should keep in mind, even if I don't work on them today, are:": "Future integrations with other systems",
        "I know today would be successful if I did or felt this by the end:": "A working daily notes system with good documentation"
    }
    
    # Initialize the daily notes handler
    handler = DailyNotesHandler()
    
    # Process the SOD form data
    success, result = handler.process_sod_form(sod_data)
    
    if success:
        logger.info(f"Successfully created daily note: {result}")
    else:
        logger.error(f"Failed to create daily note: {result}")
    
    return success

def test_eod_form():
    """
    Test the EOD form processing.
    """
    logger.info("Testing EOD form processing...")
    
    # Create sample EOD form data
    eod_data = {
        "form_id": EOD_ID,
        "Rating": "8",
        "Summary": "Today was productive. I completed the daily notes integration and tested it successfully.",
        "Story": "The most meaningful moment was when I saw the system working end-to-end for the first time.",
        "Accomplishments": "- Completed the daily notes integration\n- Tested the functionality\n- Wrote documentation",
        "Obstacles": "I encountered an issue with the Google Drive API authentication, but resolved it by checking the credentials file path.",
        "What did you do to re-energize? How did it go?": "Took a short walk outside. It helped clear my mind and come back refreshed.",
        "Physical": "7",
        "Mental": "8",
        "Emotional": "8",
        "Spiritual": "6",
        "What can I do tomorrow to be 1% better?": "Start with a clearer plan for the day and prioritize tasks better."
    }
    
    # Initialize the daily notes handler
    handler = DailyNotesHandler()
    
    # Process the EOD form data
    success, result = handler.process_eod_form(eod_data)
    
    if success:
        logger.info(f"Successfully updated daily note: {result}")
    else:
        logger.error(f"Failed to update daily note: {result}")
    
    return success

def main():
    """
    Main function to run the tests.
    """
    logger.info("Starting daily notes tests...")
    
    # Test SOD form
    sod_success = test_sod_form()
    
    # Test EOD form
    eod_success = test_eod_form()
    
    # Print summary
    logger.info("Test summary:")
    logger.info(f"SOD form test: {'SUCCESS' if sod_success else 'FAILED'}")
    logger.info(f"EOD form test: {'SUCCESS' if eod_success else 'FAILED'}")
    
    if sod_success and eod_success:
        logger.info("All tests passed!")
    else:
        logger.error("Some tests failed. Check the logs for details.")

if __name__ == "__main__":
    main()
