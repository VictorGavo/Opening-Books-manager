from flask import Flask, request, jsonify
import logging
import json

from keep_handler import create_keep_note

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

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

        # Process Form Data here
        process_form_data(data)

        return jsonify({'status': 'success'}), 200
    elif request.method == 'GET':
        return "Webhook endpoint is active", 200
    else:
        return jsonify({'error': 'Method Not Allowed'}), 405
    

def process_form_data(data):
    """
    Processes the data received from the Google Form submission.
    
    Args:
        data (dict): The JSON data received from the webhook.
    """
    print("Received form submission:")
    print(json.dumps(data, indent=4)) # Pretty print the JSON for inspection

    # TODO: process_form_data should call g.keep, obsidian, discord, etc. functions and pass the data to them.
    create_keep_note(data)

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)