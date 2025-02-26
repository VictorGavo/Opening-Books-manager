# Second Brain Mobile Integration

This project integrates with Google Keep to automatically create notes from external sources.

## Overview

This project consists of a Flask application that receives webhooks from external services and creates Google Keep notes using the `gkeepapi` library.

## Prerequisites

*   Python 3.9+
*   `pyenv` (recommended for managing Python versions)
*   A Google account with Google Keep enabled
*   A master token for authenticating with the Google Keep API (obtained using `gpsoauth`)

## Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd second-brain-mobile-integration
    ```

2.  Install dependencies:

    ```bash
    python -m venv venv
    source venv/bin/activate  # Linux/macOS
    .\venv\Scripts\activate   # Windows
    pip install -r requirements.txt  # If you have a requirements.txt file
    # OR
    pip install Flask gkeepapi  # If you don't have a requirements.txt file
    ```

3.  Configure environment variables:

    *   Set the following environment variables:
        *   `GMAIL_ADDRESS`: Your Gmail address
        *   `MASTER_TOKEN`: Your Google Keep master token

    *   You can set these variables in your shell's configuration file (e.g., `.bashrc`, `.zshrc`) or directly in the environment where your application is running.

## Usage

1.  Run the Flask application (development):

    ```bash
    python app.py
    ```

2.  Run the Flask application (production):

    ```bash
    gunicorn --bind 0.0.0.0:8000 app:app
    ```

3.  Configure a reverse proxy (Nginx, Apache) to expose the application to the internet.

4.  Configure the external service to send webhooks to your application's endpoint.

## Deployment

See the deployment documentation for detailed instructions on how to deploy this application to a production server.

## License

[Your License]


# Developer Notes:
Here's a possible project structure:

second-brain-integration/
├── app.py          # Main Flask app
├── google_keep/   # Module for Google Keep integration
│   ├── __init__.py
│   ├── keep_handler.py   # Function to create Google Keep notes
│   └── ...
├── obsidian/       # Module for Obsidian integration
│   ├── __init__.py
│   ├── obsidian_writer.py  # Function to write data to Markdown files
│   └── ...
├── utils/          # Shared utility functions (e.g., authentication)
│   ├── __init__.py
│   ├── google_auth.py
│   └── ...
├── requirements.txt
└── README.md
Plain text
In this structure:

app.py would handle the webhook from Google Forms and dispatch the data to the appropriate module (either google_keep or obsidian).
The google_keep module would contain the logic for creating Google Keep notes.
The obsidian module would contain the logic for writing data to Markdown files in your Obsidian vault.
The utils module would contain any shared utility functions, such as functions for authenticating with Google APIs.
If the obsidian module becomes too complex, you can always move it to a separate project later.

Integrating Additional Data Sources (Health, Food, Habits):

Your vision of centralizing all your personal data in Obsidian is excellent. To integrate additional data sources, you can follow a similar approach:
Identify Data Sources: Determine the APIs or data formats for each data source (e.g., Fitbit API for health data, a CSV file for food tracking data).
Create Modules: Create separate modules for each data source (e.g., fitbit, food_tracker).
Implement Data Extraction and Transformation: In each module, implement the logic to extract the data from the data source and transform it into a format suitable for writing to Markdown files.
Integrate with Obsidian: Use the obsidian_writer.py module to write the data to Markdown files in your Obsidian vault.
Schedule Data Updates: Use a scheduler (e.g., cron on Linux, Task Scheduler on Windows) to automatically update the data in your Obsidian vault on a regular basis.
Remember to handle authentication and data privacy carefully, especially when dealing with sensitive personal data.