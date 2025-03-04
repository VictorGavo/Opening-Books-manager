from flask import Flask, request, jsonify
import json

from keep_handler import create_keep_note

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    if request.method == 'POST':
        data = request.get_json()

        # Process Form Data here
        process_form_data(data)

        return jsonify({'status': 'success'}), 200
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
    app.run(debug=True)