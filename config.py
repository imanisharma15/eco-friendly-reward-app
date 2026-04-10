# Configuration file for Eco-Friendly Reward App

# Flask Configuration
DEBUG = True
TESTING = False
SECRET_KEY = 'eco_app_secret_key_2026'  # Change this in production!

# Database Configuration
DATABASE = {
    'type': 'sqlite',
    'database': 'eco_app.db'
}

# File Upload Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'webm'}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Session Configuration
SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
PERMANENT_SESSION_LIFETIME = 86400  # 24 hours

# Application Settings
APP_NAME = 'Eco-Friendly Reward App'
APP_VERSION = '1.0.0'
APP_PORT = 5000
APP_HOST = 'localhost'
