# Second Brain Mobile Integration

This project integrates with Google Keep to automatically create notes from external sources like Google Forms.

## Overview

This project consists of a Flask application that receives webhooks from external services (primarily Google Forms via Google Apps Script) and creates Google Keep notes using the `gkeepapi` library. The application is designed to be part of a larger "Second Brain" system that centralizes personal data from various sources.

## Current Features

- Webhook endpoint that receives data from Google Forms
- Google Keep integration for creating formatted notes
- Support for environment variable and keyring-based authentication
- Configurable logging
- Test endpoint for verifying connectivity

## Prerequisites

* Python 3.9+
* `pyenv` (recommended for managing Python versions)
* A Google account with Google Keep enabled
* A master token for authenticating with the Google Keep API (obtained using `gpsoauth`)
* Nginx or another reverse proxy (for production deployment)

## Installation

1. Clone the repository:

   ```bash
   git clone <repository_url>
   cd second-brain-mobile-integration
   ```

2. Install dependencies:

   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   .\venv\Scripts\activate   # Windows
   pip install -r requirements.txt
   ```

3. Configure environment variables:

   Create a `.env` file in the project root:
   
   ```
   GMAIL_ADDRESS=your-gmail@gmail.com
   MASTER_TOKEN=your-master-token
   ```
   
   For security, set appropriate permissions:
   
   ```bash
   chmod 600 .env
   ```

4. Obtain a Google Keep master token (if you don't have one):

   ```python
   import gpsoauth
   
   email = "your-gmail@gmail.com"
   password = "your-app-password"  # Use an App Password if you have 2FA enabled
   master_token = gpsoauth.perform_master_login(email, password, 'androidId')
   print(master_token['Token'])
   ```

## Usage

### Development Mode

Run the Flask application locally:

```bash
python app.py
```

### Production Deployment

#### 1. Setting Up Nginx as a Reverse Proxy

Install and configure Nginx:

```bash
sudo apt install nginx
```

Create a configuration file:

```bash
sudo nano /etc/nginx/sites-available/gkeep-integration
```

Add the following configuration:

```nginx
server {
    listen 88;  # Or any port you prefer
    server_name _;  # Replace with your domain if available

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable the site and restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/gkeep-integration /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 2. Setting Up as a System Service

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/gkeep-integration.service
```

Add the following content (adjust paths as needed):

```ini
[Unit]
Description=Google Keep Integration Service
After=network.target

[Service]
User=your-username
Group=your-username
WorkingDirectory=/path/to/your/project
Environment="PATH=/path/to/your/project/venv/bin"
EnvironmentFile=/path/to/your/project/.env
ExecStart=/path/to/your/project/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable gkeep-integration
sudo systemctl start gkeep-integration
```

#### 3. Service Management

Check status:
```bash
sudo systemctl status gkeep-integration
```

View logs:
```bash
sudo journalctl -u gkeep-integration -f
```

Restart after code changes:
```bash
sudo systemctl restart gkeep-integration
```

### Google Apps Script Integration

To send data from Google Forms to your webhook:

1. Open your Google Form in edit mode
2. Click the three dots (⋮) in the top right corner
3. Select "Script editor"
4. Add the following code:

```javascript
function onSubmit(e) {
  try {
    var formResponse = e.response;
    var itemResponses = formResponse.getItemResponses();
    var data = {};

    for (var i = 0; i < itemResponses.length; i++) {
      var item = itemResponses[i].getItem();
      var question = item.getTitle();
      var answer = itemResponses[i].getResponse();
      data[question] = answer;
    }

    var payload = JSON.stringify(data);
    
    var options = {
      'method': 'post',
      'contentType': 'application/json',
      'payload': payload,
      'muteHttpExceptions': true
    };

    var response = UrlFetchApp.fetch('http://your-server-address:88/webhook', options);
    Logger.log('Webhook response: ' + response.getContentText());
  } catch (error) {
    Logger.log('Webhook error: ' + error.toString());
  }
}
```

5. Set up a trigger for the `onSubmit` function to run when a form is submitted

## Troubleshooting

### Connection Issues

If Google Apps Script cannot connect to your server:

1. Verify your server is accessible from the internet
2. Check port forwarding if behind a router
3. Ensure your firewall allows incoming connections on the configured port
4. Test connectivity with:
   ```bash
   curl -X POST -H "Content-Type: application/json" -d '{"test":"data"}' http://your-server-address:88/webhook
   ```

### Authentication Issues

If you're having trouble with Google Keep authentication:

1. Verify your environment variables are set correctly
2. Try regenerating your master token
3. Check the logs for specific error messages

## Planned Features and Integrations

### Obsidian Integration

Future development will include integration with Obsidian to write data to Markdown files:

- Create an `obsidian` module with an `obsidian_writer.py` component
- Implement functions to transform data into Markdown format
- Set up file management within an Obsidian vault

### Additional Data Sources

The project aims to centralize various personal data sources:

- Health data (e.g., Fitbit, Apple Health)
- Food tracking
- Habit tracking
- Journal entries
- Task management

### Architecture Improvements

Planned architectural improvements include:

- Modular design with separate packages for each integration
- Improved error handling and recovery
- Comprehensive logging and monitoring
- Configuration management system
- Unit and integration tests

## Project Structure

Current structure:
```
second-brain-integration/
├── app.py              # Main Flask app with webhook endpoints
├── auth.py             # Authentication utilities
├── config.py           # Configuration settings
├── forms_handler.py    # Google Forms interaction
├── keep_handler.py     # Google Keep integration
├── main.py             # Main script for orchestration
├── utils.py            # Utility functions
├── utils/              # JavaScript utilities (future use)
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
```

Planned structure:
```
second-brain-integration/
├── app.py              # Main Flask app
├── google_keep/        # Module for Google Keep integration
│   ├── __init__.py
│   ├── keep_handler.py # Function to create Google Keep notes
│   └── auth.py         # Authentication for Google services
├── obsidian/           # Module for Obsidian integration
│   ├── __init__.py
│   ├── obsidian_writer.py  # Function to write data to Markdown files
│   └── ...
├── integrations/       # Additional data source integrations
│   ├── __init__.py
│   ├── health/         # Health data integration
│   ├── food/           # Food tracking integration
│   └── ...
├── utils/              # Shared utility functions
│   ├── __init__.py
│   ├── config.py       # Configuration management
│   ├── logging.py      # Logging utilities
│   └── ...
├── tests/              # Test suite
├── requirements.txt    # Python dependencies
└── README.md           # Documentation
```

## License

[Your License]
