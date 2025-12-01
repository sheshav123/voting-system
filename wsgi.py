#!/usr/bin/env python3
"""
WSGI configuration for PythonAnywhere deployment
"""
import sys
import os

# Add your project directory to the sys.path
project_home = '/home/YOUR_USERNAME/YOUR_PROJECT_FOLDER'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv(os.path.join(project_home, '.env'))

# Import Flask app
from decentralised_voting_app import app as application
