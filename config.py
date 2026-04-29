"""
Configuration Settings for SecureWipe Pro
"""
import os

# Flask Settings
DEBUG = True  # Set to False in production
SECRET_KEY = "your-secret-key-change-this"
PORT = 5000
HOST = "127.0.0.1"

# File Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CERTS_DIR = os.path.join(BASE_DIR, "certs")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
WIPE_TARGETS_DIR = os.path.join(BASE_DIR, "wipe_targets")

# Create directories if they don't exist
os.makedirs(CERTS_DIR, exist_ok=True)
os.makedirs(LOGS_DIR, exist_ok=True)
os.makedirs(WIPE_TARGETS_DIR, exist_ok=True)

# Logging Settings
LOG_LEVEL = "INFO"
LOG_FILE = os.path.join(LOGS_DIR, "securewipe.log")

# Security Settings
MAX_FILE_SIZE = 5 * 1024 * 1024  # 5MB
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'doc', 'docx'}

# API Settings
API_TIMEOUT = 30  # seconds
MAX_REQUESTS_PER_MINUTE = 60

# Host ID Settings
HOST_ID_FILE = os.path.join(CERTS_DIR, "host_id.json")

# Wipe Algorithm Settings
WIPE_PASSES = 3  # Number of overwrite passes
WIPE_ALGORITHM = "VAJRA"  # Algorithm to use