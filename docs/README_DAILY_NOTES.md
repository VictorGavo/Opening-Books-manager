# Daily Notes Integration

This extension to the Second Brain Mobile Integration project adds functionality to create and update daily notes in markdown format from Google Form submissions. It integrates with your existing Google Forms (SOD and EOD) to create daily notes in your Obsidian vault that's synced with Google Drive.

## Overview

The system works as follows:

1. When you submit your Start of Day (SOD) Google Form, the data is sent to your server via webhook
2. The server processes the form data and:
   - Creates a Google Keep note (existing functionality)
   - Creates a new markdown file in your Google Drive folder using your daily note template
3. When you submit your End of Day (EOD) Google Form, the data is sent to your server via webhook
4. The server processes the form data and:
   - Finds the existing daily note for the current day
   - Updates it with the EOD form data

## Setup Instructions

### 1. Install Dependencies

Make sure you have all the required dependencies installed:

```bash
pip install -r requirements.txt
```

### 2. Google Drive API Setup

1. Make sure your Google Cloud project has the Google Drive API enabled
2. Ensure your service account has access to the Google Drive folder where you want to store your daily notes
3. Make sure the service account credentials file is properly set up in your environment

### 3. Update Google Apps Script

1. Open your Google Forms in edit mode
2. Click the three dots (⋮) in the top right corner
3. Select "Script editor"
4. Copy and paste the code from `google_apps_script.js` into the editor
5. Replace the `WEBHOOK_URL` with your server's webhook URL
6. Save the script
7. Set up a trigger for the `onSubmit` function to run when a form is submitted:
   - Click on the clock icon (Triggers) in the left sidebar
   - Click "Add Trigger"
   - Set "Choose which function to run" to `onSubmit`
   - Set "Select event source" to "From form"
   - Set "Select event type" to "On form submit"
   - Click "Save"

### 4. Configure Your Server

Make sure your server is properly configured:

1. Check that the `DAILY_NOTES_FOLDER` in `config.py` points to the correct Google Drive folder path
2. Verify that `DAILY_TEMPLATE_PATH` in `config.py` points to your daily note template
3. Ensure that `GOOGLE_APPLICATION_CREDENTIALS` environment variable is set to the path of your service account credentials file

## How It Works

### Components

1. **markdown_handler.py**: Handles the generation and updating of markdown content based on the template and form data
2. **drive_handler.py**: Handles Google Drive operations (finding, creating, and updating files)
3. **daily_notes_handler.py**: Orchestrates the process of creating and updating daily notes
4. **app.py**: Contains the webhook endpoint that receives form submissions and routes them to the appropriate handler

### Data Flow

```
Google Form Submission → Webhook → Form Type Detection → Process Form Data → Create/Update Daily Note
```

### Form Type Detection

The system determines whether a form submission is from the SOD or EOD form by:

1. Checking the `form_id` field in the data (if provided by the Google Apps Script)
2. Analyzing the form fields (e.g., SOD forms have "Today's Big 3", EOD forms have "Rating")

## Troubleshooting

### Common Issues

1. **Webhook Connection Issues**:
   - Verify your server is accessible from the internet
   - Check port forwarding if behind a router
   - Ensure your firewall allows incoming connections on the configured port

2. **Google Drive API Issues**:
   - Check that your service account has the necessary permissions
   - Verify the folder path is correct
   - Check the credentials file is valid and accessible

3. **Template Processing Issues**:
   - Ensure the template file exists and is readable
   - Check that the template variables are correctly formatted

### Logging

The system uses Python's logging module to log information and errors. Check the logs for detailed information about what's happening and any errors that occur.

## Extending the System

This system is designed to be modular and extensible. Here are some ways you could extend it:

1. **Discord Integration**: Send your Big 3 items to a Discord channel for accountability
2. **Google Keep Import**: Import notes created in Google Keep into your Obsidian vault
3. **Goal Linking**: Link goals from your Obsidian vault to Google Keep notes

## File Structure

```
second-brain-integration/
├── app.py                  # Main Flask app with webhook endpoints
├── auth.py                 # Authentication utilities
├── config.py               # Configuration settings
├── daily_notes_handler.py  # Handles daily notes creation and updates
├── drive_handler.py        # Google Drive integration
├── forms_handler.py        # Google Forms interaction
├── google_apps_script.js   # Google Apps Script for form submission
├── keep_handler.py         # Google Keep integration
├── main.py                 # Main script for orchestration
├── markdown_handler.py     # Markdown generation and processing
├── utils.py                # Utility functions
├── requirements.txt        # Python dependencies
└── README.md               # Documentation
