#!/usr/bin/python3.10

"""
WSGI configuration for PythonAnywhere deployment
This file will be used by PythonAnywhere to serve your Flask app
"""

import sys
import os

# Add your project directory to the Python path
# Replace 'yourusername' with your actual PythonAnywhere username
project_home = '/home/yourusername/careerly_subscription'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Import your Flask application
from subscription_api import app as application

if __name__ == "__main__":
    application.run() 