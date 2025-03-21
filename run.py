#!/usr/bin/env python3
"""
Main entry point for the Second Brain Mobile Integration application.
This script provides a convenient way to run the application.
"""

import sys
import os
from src.api.app import app

def main():
    """
    Main function to run the Flask application.
    """
    print("Starting Second Brain Mobile Integration...")
    app.run(host='127.0.0.1', port=5000, debug=True)

if __name__ == "__main__":
    main()
