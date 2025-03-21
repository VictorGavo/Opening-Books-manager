from flask import Flask, request, jsonify
import logging
import json
import os

from src.handlers.keep_handler import create_keep_note
from src.handlers.daily_notes_handler import DailyNotesHandler
from config.config import SOD_ID, EOD_ID

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize the daily notes handler
daily_notes_handler = DailyNotesHandler()

@app.route('/test-webhook', methods=['GET', 'POST'])
def test_webhook():
    logging.info(f"Test webhook called - Method: {request.method}")
    logging.info(f"Headers: {dict(request.headers)}")

    # Log raw request data
    raw_data = request.get_data(as_text=True)
    logging.info(f"Raw Request Data: {raw_data}")

    try:
        # Try parsing as JSON
        data = request.get_json(force=True)
        logging.info(f"Parsed JSON Data: {data}")
        return jsonify({'status': 'success', 'received_data': data}), 200
    except Exception as e:
        logging.error(f"JSON Parsing Error: {e}")
        # Return success even if JSON parsing fails
        return jsonify({'status': 'success', 'received_raw_data': raw_data}), 200

@app.route('/webhook', methods=['GET', 'POST'])
def webhook_handler():
    logging.info(f"Webhook called - Method: {request.method}")
    logging.info(f"Headers: {dict(request.headers)}")
    
    # Log raw request data
    raw_data = request.get_data(as_text=True)
    logging.info(f"Raw Request Data: {raw_data}")
    
    try:
        # Try parsing as JSON
        data = request.get_json(force=True)
        logging.info(f"Parsed JSON Data: {data}")
    except Exception as e:
        logging.error(f"JSON Parsing Error: {e}")
        data = raw_data
        
    if request.method == 'POST':
        data = request.get_json()
        
        # Extract form_id if present
        form_id = None
        if isinstance(data, dict) and 'form_id' in data:
            form_id = data.get('form_id')
            logger.info(f"Form ID: {form_id}")

        # Process Form Data here
        process_form_data(data, form_id)

        return jsonify({'status': 'success'}), 200
    elif request.method == 'GET':
        return "Webhook endpoint is active", 200
    else:
        return jsonify({'error': 'Method Not Allowed'}), 405
    

def process_form_data(data, form_id=None):
    """
    Processes the data received from the Google Form submission.
    
    Args:
        data (dict): The JSON data received from the webhook.
        form_id (str, optional): The ID of the form that was submitted.
    """
    logger.info("Received form submission:")
    logger.info(json.dumps(data, indent=4))  # Pretty print the JSON for inspection

    # Determine if this is a SOD or EOD form
    is_sod = False
    is_eod = False
    
    # Check if form_id is provided
    if form_id:
        is_sod = form_id == SOD_ID
        is_eod = form_id == EOD_ID
    else:
        # Try to determine form type from the data
        # SOD form typically has "Today's Big 3" field
        is_sod = "Today's Big 3" in data or "What am I looking forward to the most today?" in data
        # EOD form typically has "Rating" field
        is_eod = "Rating" in data or "Summary" in data or "What can I do tomorrow to be 1% better?" in data
    
    # Process based on form type
    if is_sod:
        logger.info("Processing SOD form data")
        # Create Google Keep note
        create_keep_note(data)
        
        # Create daily note in markdown
        success, result = daily_notes_handler.process_sod_form(data)
        if success:
            logger.info(f"Successfully created daily note: {result}")
        else:
            logger.error(f"Failed to create daily note: {result}")
    
    elif is_eod:
        logger.info("Processing EOD form data")
        # Update daily note in markdown
        success, result = daily_notes_handler.process_eod_form(data)
        if success:
            logger.info(f"Successfully updated daily note: {result}")
        else:
            logger.error(f"Failed to update daily note: {result}")
    
    else:
        logger.warning("Unknown form type, defaulting to Google Keep note")
        # Default to creating a Google Keep note
        create_keep_note(data)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
