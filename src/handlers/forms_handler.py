# Handles Google Forms Interactions
import logging
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import datetime

def get_form_responses(form_id):
    """
    Retrieves the latest responses from a Google Form
    
    Args:
        form_id: The ID of the Google Form
        
    Returns:
        list: A list of dictionaries, where each dictionary represents a form response
            Returns None if there's an error.
    """
    try:
        # Authenticate and build the Forms API service
        creds, _ = google.auth.default()
        service = build('forms','v1', credentials=creds)

        # Retreive the form responses
        results = service.forms().responses().list(formId=form_id).execute()
        responses = results.get('responses', [])

        # Process the responses into a more usable format
        processed_responses = []
        for response in responses:
            item_responses = response.get('answers', {})
            processed_response = {}
            for key, value in item_responses.items():
                processed_response[key] = value['textAnswers']['answers'][0]['value']
            processed_responses.append(processed_response)

        return processed_responses
    
    except HttpError as e:
        print(f"An error occurred: {e}")
        return None
    

if __name__ == '__main__':
    FORM_ID='1blTpEVqj9xASpwgPJLATF65uiPImf3EME8AEHg2AWhE'

    responses = get_form_responses(FORM_ID)

    if responses:
        for response in responses:
            print(response)
    else:
        print("No responses found or an error occurred.")
