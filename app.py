from flask import Flask, request, jsonify
import datetime
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

    # Extract the content you want from GForm for GKeep
    big_3 = data.get("Today's Big 3", "No Big 3 Entered")
    success_criteria = data.get("I know today would be successful if I did or felt this by the end:",
                                 "No Success Criteria Entered")

    # Create the content fro the GKeep note
    note_content = f"Today's Big 3:\n{big_3}\n\nSuccess Criteria:\n{success_criteria}\n--------\n"

    # Format the title with the current date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    note_title = f"{current_date}"

    # Create Keep Note
    print(note_title, note_content)
    create_keep_note(note_title, note_content)

if __name__ == "__main__":
    app.run(debug=True)