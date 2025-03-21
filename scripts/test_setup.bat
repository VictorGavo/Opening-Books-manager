@echo off
echo Setting up environment variables...
set GOOGLE_APPLICATION_CREDENTIALS=credentials/credentials.json

echo Running test script...
python scripts\test_daily_notes.py

echo.
echo If the test was successful, you should see a new daily note in your Google Drive folder.
echo If there were any errors, please check the docs\SETUP_INSTRUCTIONS.md file for troubleshooting.
echo.
pause
