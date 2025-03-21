# Google Drive API Setup Instructions

You can use your existing service account credentials (`credentials/credentials.json`) for Google Drive access. Here's how to set it up:

## 1. Enable Google Drive API for Your Project

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project "gform-to-gkeep"
3. Navigate to "APIs & Services" > "Library"
4. Search for "Google Drive API"
5. Click on "Google Drive API" in the results
6. Click "Enable" if it's not already enabled

## 2. Grant Your Service Account Access to Your Google Drive Folder

Your service account email is: `daily-books-monitor@gform-to-gkeep.iam.gserviceaccount.com`

To grant this service account access to your Google Drive folder:

1. Go to your Google Drive
2. Navigate to the folder where you want to store your daily notes (Projects/Systems/Daily Notes/Output)
3. Right-click on the folder and select "Share"
4. In the "Add people or groups" field, enter your service account email: `daily-books-monitor@gform-to-gkeep.iam.gserviceaccount.com`
5. Set the permission to "Editor"
6. Uncheck "Notify people" (optional)
7. Click "Share"

## 3. Update Your Configuration

Your existing configuration in `config.py` should already be set up to use the credentials file. Make sure the following settings are correct:

```python
# Google Drive API settings
GOOGLE_DRIVE_CREDENTIALS=os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
DAILY_NOTES_FOLDER="Projects/Systems/Daily Notes/Output"
DAILY_TEMPLATE_PATH="references/Daily Template.md"
```

And ensure your environment variable is set:

```bash
# For Linux/macOS
export GOOGLE_APPLICATION_CREDENTIALS="credentials/credentials.json"

# For Windows PowerShell
$env:GOOGLE_APPLICATION_CREDENTIALS="credentials/credentials.json"

# For Windows Command Prompt
set GOOGLE_APPLICATION_CREDENTIALS=credentials/credentials.json
```

## 4. Test Your Setup

Run the test script to verify everything is working:

```bash
python test_daily_notes.py
```

This will attempt to create a daily note in your Google Drive folder using your service account credentials.

## Troubleshooting

If you encounter any issues:

1. **Permission Denied**: Make sure you've shared the folder with your service account email and given it Editor permissions.

2. **API Not Enabled**: Verify that the Google Drive API is enabled for your project in the Google Cloud Console.

3. **Credentials Path**: Ensure the `GOOGLE_APPLICATION_CREDENTIALS` environment variable is set correctly to the path of your credentials file.

4. **Folder Path**: Double-check that the folder path in `config.py` matches exactly the path in your Google Drive.

5. **Character Encoding Issues**: If you see errors about character encoding (especially with emoji characters), the system now automatically replaces emoji characters with text equivalents to avoid these issues.

6. **Testing**: You can use the provided `test_setup.bat` file (on Windows) to set the environment variable and run the test script in one step.
