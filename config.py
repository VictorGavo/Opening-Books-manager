# To store configuration settings
import os
from dotenv import load_dotenv

load_dotenv()

# Google Keep API settings
KEEP_CLIENT_SECRET_FILE="credentials/gform-to-gkeep-gcloud-credentials.json"

# Google Sheets API settings
SHEETS_CLIENT_SECRET_FILE="credentials/gform-to-gkeep-gcloud-credentials.json"

# IDs of the Google Forms to monitor
SOD_ID=os.getenv("SOD_ID")
EOD_ID=os.getenv("EOD_ID")