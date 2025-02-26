import keyring
import os
from dotenv import load_dotenv

load_dotenv()


def get_master_token(email):
    """
    Retrieves the Google Keep master token from the keyring.
    """
    try:
        master_token = keyring.get_password("google-keep-token", email)
        if not master_token:
            print("Error: Master token not found in keyring. Please store it using keyring.set_password().")
            return None
        return master_token
    except Exception as e:
        print(f"Error retrieving master token from keyring: {e}")
        return None
    
def store_master_token(email, master_token):
    """
    Stores the Google Keep master token in the keyring.
    """
    try:
        keyring.set_password("google-keep-token", email, master_token)
        print("Master token stored successfully in keyring.")
    except Exception as e:
        print(f"Error storing master token in keyring: {e}")

if __name__ == "__main__":
    # Example usage:
    email = os.environ.get('GMAIL_ADDRESS')
    store_master_token(email, os.environ.get('MASTER_TOKEN'))
    token = get_master_token(email)
    if token:
        print("Master token retrieved successfully.")
    else:
        print("Failed to retrieve master token.")