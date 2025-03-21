# To store configuration settings
import os
from dotenv import load_dotenv

load_dotenv('config/.env')

# Google Keep API settings
KEEP_CLIENT_SECRET_FILE="credentials/gform-to-gkeep-gcloud-credentials.json"

# Google Sheets API settings
SHEETS_CLIENT_SECRET_FILE="credentials/gform-to-gkeep-gcloud-credentials.json"

# Google Drive API settings
GOOGLE_DRIVE_CREDENTIALS=os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
# Update this path to where the files are actually being created
DAILY_NOTES_FOLDER="Projects/Systems/Daily Notes/Output"
DAILY_TEMPLATE_PATH="templates/Daily Template.md"

# IDs of the Google Forms to monitor
SOD_ID=os.getenv("SOD_ID")
EOD_ID=os.getenv("EOD_ID")
