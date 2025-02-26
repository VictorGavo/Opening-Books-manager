# Handles Google Keep interactions
import gkeepapi
import os
from auth import get_master_token

import sys
print(sys.executable)
print(f"gkeepapi version: {gkeepapi.__version__}") # Add this line


def create_keep_note(title, text):
    """
    Creates a new Google Keep note using a service account.
    """

    try:
        # Load credentials from the environment variable
        email = os.environ.get('GMAIL_ADDRESS')
        password = os.environ.get('GMAIL_PASSWORD')
        master_token = get_master_token(email)

        if not master_token:
            print("Error: Master token not found. Please store it using keyring.set_password().")
            return False

        # Authenticate with Keep
        keep = gkeepapi.Keep()
        # keep.login(email, password)
        # print(f"Keep class attributes: {dir(keep)}")  # Add this line
        keep.authenticate(email, master_token)

        # Create a new note
        note = keep.createNote(title, text)
        note.pinned = True
        keep.sync()

        print(f"Created Google Keep note: {title}")
        return True
    except Exception as e:
        print(f"Error creating Google Keep note: {e}")
        return False
    
if __name__ == "__main__":
    # Example usage
    note_title = "Test Note from Script"
    note_text = "This is a test note created using gkeepapi."
    create_keep_note(note_title, note_text)
