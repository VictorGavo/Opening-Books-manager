# Test script for daily notes functionality
import sys
import os
import logging
import datetime
import json

# Add the parent directory to the path so we can import the project modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.handlers.daily_notes_handler import DailyNotesHandler
from src.utils.utils import setup_logging

logger = setup_logging()

def test_sod_form():
    """
    Test creating a daily note from SOD form data.
    """
    logger.info("Testing SOD form processing...")
    
    # Create sample SOD form data
    sod_data = {
        "Today's Big 3": "1. Complete project report\n2. Prepare for client meeting\n3. Review team's code",
        "What am I looking forward to the most today?": "Meeting with the design team to finalize the UI",
        "3 things I'm grateful for in my life:": "Family, Health, Opportunities",
        "3 things I'm grateful about myself:": "Persistence, Creativity, Empathy",
        "I'm excited today for:": "Learning new technologies",
        "One word to describe the person I want to be today would be __ because:": "Focused - because I need to complete several important tasks",
        "Someone who needs me on my a-game today is:": "My team members who are waiting for my feedback",
        "What's a potential obstacle/stressful situation for today and how would my best self deal with it?": "Tight deadline - I'll break down the work into manageable chunks and prioritize",
        "Someone I could surprise with a note, gift, or sign of appreciation is:": "My colleague who helped me last week",
        "One action I could take today to demonstrate excellence or real value is:": "Deliver the project ahead of schedule",
        "One bold action I could take today is:": "Propose a new feature that could improve user experience",
        "An overseeing high performance coach would tell me today that:": "Focus on one task at a time and avoid multitasking",
        "The big projects I should keep in mind, even if I don't work on them today, are:": "Website redesign, API integration",
        "I know today would be successful if I did or felt this by the end:": "Completed all my Big 3 tasks and felt productive"
    }
    
    # Initialize the daily notes handler
    daily_notes_handler = DailyNotesHandler()
    
    # Process the SOD form data
    success, result = daily_notes_handler.process_sod_form(sod_data)
    
    if success:
        logger.info(f"Successfully created daily note: {result}")
    else:
        logger.error(f"Failed to create daily note: {result}")
    
    return success, result

def test_eod_form(file_id=None):
    """
    Test updating a daily note with EOD form data.
    
    Args:
        file_id: ID of the file to update (if None, will look for today's note)
    """
    logger.info("Testing EOD form processing...")
    
    # Create sample EOD form data
    eod_data = {
        "Rating": "8",
        "Summary": "Today was productive. I completed all my Big 3 tasks and made progress on the website redesign.",
        "Story": "The highlight of my day was the design team meeting where we finalized the UI for the new feature.",
        "Accomplishments": "- Completed project report\n- Prepared for client meeting\n- Reviewed team's code\n- Started working on the website redesign",
        "Obstacles": "I faced a tight deadline for the project report, but I managed to break it down into smaller tasks and completed it on time.",
        "What did you do to re-energize? How did it go?": "Took a 15-minute walk outside. It helped clear my mind and I came back refreshed.",
        "Physical": "7",
        "Mental": "8",
        "Emotional": "9",
        "Spiritual": "6",
        "What can I do tomorrow to be 1% better?": "Start the day with a short meditation session to improve focus."
    }
    
    # Initialize the daily notes handler
    daily_notes_handler = DailyNotesHandler()
    
    # Process the EOD form data
    success, result = daily_notes_handler.process_eod_form(eod_data)
    
    if success:
        logger.info(f"Successfully updated daily note: {result}")
    else:
        logger.error(f"Failed to update daily note: {result}")
    
    return success, result

def main():
    """
    Main function to run the tests.
    """
    logger.info("Starting daily notes tests...")
    
    # Test SOD form
    sod_success, sod_result = test_sod_form()
    
    # Test EOD form
    if sod_success:
        # If SOD test was successful, use the file ID for the EOD test
        eod_success, eod_result = test_eod_form(sod_result)
    else:
        # Otherwise, just run the EOD test without a specific file ID
        eod_success, eod_result = test_eod_form()
    
    logger.info("Daily notes tests completed.")

if __name__ == "__main__":
    main()
