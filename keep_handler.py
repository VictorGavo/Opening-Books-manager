# Handles Google Keep interactions
import gkeepapi
import os
from auth import get_master_token
import datetime

import sys
print(sys.executable)
print(f"gkeepapi version: {gkeepapi.__version__}") # Add this line


def create_keep_note(data):
    """
    Creates a new Google Keep note using a service account.
    """

    # Extract the content you want from GForm for GKeep
    big_3 = data.get("Today's Big 3", "No Big 3 Entered")
    success_criteria = data.get("I know today would be successful if I did or felt this by the end:",
                                 "No Success Criteria Entered")

    # Create the content for the GKeep note
    note_content = f"Today's Big 3:\n{big_3}\n\nSuccess Criteria:\n{success_criteria}\n--------\n"

    # Format the title with the current date
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    note_title = f"{current_date}"

    # Create Keep Note
    print(note_title, note_content)

    try:
        # Load credentials from the environment variable
        email = os.environ.get('GMAIL_ADDRESS')
        password = os.environ.get('GMAIL_PASSWORD')
        master_token = get_master_token(email)

        if not master_token:
            print("Keyring failed, trying environment variable...")
            master_token = os.environ.get('MASTER_TOKEN')

        if not master_token:
            print("Error: Master token not found. Please store it using keyring.set_password().")
            return False

        # Authenticate with Keep
        keep = gkeepapi.Keep()
        # keep.login(email, password)
        # print(f"Keep class attributes: {dir(keep)}")  # Add this line
        keep.authenticate(email, master_token)

        # Create a new note
        note = keep.createNote(note_title, note_content)
        note.pinned = True
        keep.sync()

        print(f"Created Google Keep note: {note_title}")
        return True
    except Exception as e:
        print(f"Error creating Google Keep note: {e}")
        return False
    
# if __name__ == "__main__":
    # TODO: UPDATE TESTING CODE
    # Example usage [DEPRECIATED]
    # note_title = "Test Note from Script"
    # note_text = "This is a test note created using gkeepapi."
    # create_keep_note(note_title, note_text)
