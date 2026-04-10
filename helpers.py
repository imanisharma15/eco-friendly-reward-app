# Helper functions for Eco-Friendly Reward App

import sqlite3
import os
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from datetime import datetime

# File handling helpers

def allowed_file(filename, allowed_extensions):
    """
    Check if the file extension is allowed.
    
    Args:
        filename: The name of the file
        allowed_extensions: Set of allowed file extensions
        
    Returns:
        Boolean indicating if file is allowed
    """
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def get_unique_filename(filename):
    """
    Generate a unique filename with timestamp to prevent conflicts.
    
    Args:
        filename: Original filename
        
    Returns:
        Unique filename with timestamp
    """
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
    secure_name = secure_filename(filename)
    return timestamp + secure_name


def get_exif_data(image_path):
    """
    Extract EXIF metadata from an image file.
    """
    try:
        from PIL import Image
        from PIL.ExifTags import TAGS, GPSTAGS

        image = Image.open(image_path)
        exif_info = image._getexif() or {}
        exif_data = {}

        for tag, value in exif_info.items():
            decoded = TAGS.get(tag, tag)
            if decoded == 'GPSInfo':
                gps_data = {}
                for t in value:
                    sub_decoded = GPSTAGS.get(t, t)
                    gps_data[sub_decoded] = value[t]
                exif_data['GPSInfo'] = gps_data
            else:
                exif_data[decoded] = value

        return exif_data
    except Exception as e:
        print(f"EXIF extraction error: {e}")
        return {}


def _convert_to_degrees(value):
    """Convert GPS coordinates stored in EXIF to decimal degrees."""
    d = value[0]
    m = value[1]
    s = value[2]
    return float(d[0]) / float(d[1]) + (float(m[0]) / float(m[1]) / 60.0) + (float(s[0]) / float(s[1]) / 3600.0)


def get_gps_lat_lon(exif_data):
    """Extract latitude and longitude from EXIF GPS data."""
    gps_info = exif_data.get('GPSInfo')
    if not gps_info:
        return None, None

    lat = gps_info.get('GPSLatitude')
    lat_ref = gps_info.get('GPSLatitudeRef')
    lon = gps_info.get('GPSLongitude')
    lon_ref = gps_info.get('GPSLongitudeRef')

    if not lat or not lat_ref or not lon or not lon_ref:
        return None, None

    lat_value = _convert_to_degrees(lat)
    lon_value = _convert_to_degrees(lon)

    if lat_ref != 'N':
        lat_value = -lat_value
    if lon_ref != 'E':
        lon_value = -lon_value

    return lat_value, lon_value


def get_exif_timestamp(exif_data):
    """Extract the photo capture timestamp from EXIF metadata."""
    dt = exif_data.get('DateTimeOriginal') or exif_data.get('DateTime')
    if not dt or not isinstance(dt, str):
        return None

    try:
        return datetime.strptime(dt, '%Y:%m:%d %H:%M:%S')
    except ValueError:
        return None


def extract_image_metadata(image_path):
    """Extract useful metadata from an uploaded image."""
    exif = get_exif_data(image_path)
    lat, lon = get_gps_lat_lon(exif)
    timestamp = get_exif_timestamp(exif)
    return {
        'gps_lat': lat,
        'gps_lon': lon,
        'photo_timestamp': timestamp,
        'camera_make': exif.get('Make'),
        'camera_model': exif.get('Model'),
    }


def get_file_type(filename):
    """
    Determine if file is image or video based on extension.
    
    Args:
        filename: Name of the file
        
    Returns:
        'image', 'video', or 'unknown'
    """
    extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
    
    image_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    video_extensions = {'mp4', 'avi', 'mov', 'webm'}
    
    if extension in image_extensions:
        return 'image'
    elif extension in video_extensions:
        return 'video'
    return 'unknown'


# Database helpers

def create_database_connection(db_config):
    """
    Create a connection to the configured database.
    
    Args:
        db_config: Dictionary with database configuration
        
    Returns:
        Connection object or None if failed
    """
    try:
        if db_config.get('type') == 'sqlite':
            db_path = db_config.get('database')
            connection = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)
            connection.row_factory = sqlite3.Row
            return connection
        raise ValueError('Unsupported database type')
    except Exception as e:
        print(f"Database connection error: {e}")
    return None


def initialize_database(db_config):
    """
    Initialize the SQLite database schema if it does not exist.
    """
    connection = create_database_connection(db_config)
    if not connection:
        return

    def ensure_column(cursor, table, column, definition):
        cursor.execute(f"PRAGMA table_info({table})")
        columns = [row[1] for row in cursor.fetchall()]
        if column not in columns:
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                reward_points INTEGER DEFAULT 0,
                is_admin INTEGER DEFAULT 0
            )
            """
        )
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                caption TEXT,
                file_path TEXT,
                proof_file_path TEXT,
                gps_lat REAL,
                gps_lon REAL,
                photo_timestamp TEXT,
                upload_source TEXT,
                device_info TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                points_awarded INTEGER DEFAULT 0,
                review_status TEXT DEFAULT 'pending_admin_review',
                admin_points INTEGER,
                review_notes TEXT,
                reviewed_by INTEGER,
                reviewed_at TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
                FOREIGN KEY (reviewed_by) REFERENCES users(id)
            )
            """
        )
        cursor.execute(
            """
            CREATE INDEX IF NOT EXISTS idx_user_id ON activities(user_id)
            """
        )

        ensure_column(cursor, 'users', 'reward_points', 'INTEGER DEFAULT 0')
        ensure_column(cursor, 'users', 'is_admin', 'INTEGER DEFAULT 0')
        ensure_column(cursor, 'activities', 'proof_file_path', 'TEXT')
        ensure_column(cursor, 'activities', 'gps_lat', 'REAL')
        ensure_column(cursor, 'activities', 'gps_lon', 'REAL')
        ensure_column(cursor, 'activities', 'photo_timestamp', 'TEXT')
        ensure_column(cursor, 'activities', 'upload_source', 'TEXT')
        ensure_column(cursor, 'activities', 'device_info', 'TEXT')
        ensure_column(cursor, 'activities', 'points_awarded', 'INTEGER DEFAULT 0')
        ensure_column(cursor, 'activities', 'review_status', "TEXT DEFAULT 'pending_admin_review'")
        ensure_column(cursor, 'activities', 'admin_points', 'INTEGER')
        ensure_column(cursor, 'activities', 'review_notes', 'TEXT')
        ensure_column(cursor, 'activities', 'reviewed_by', 'INTEGER')
        ensure_column(cursor, 'activities', 'reviewed_at', 'TEXT')

        cursor.close()
        connection.commit()
    except Exception as e:
        print(f"Database initialization error: {e}")
    finally:
        close_database_connection(connection)


def create_admin_user(username, password, db_config=None):
    """
    Create an admin user in the database.
    
    Args:
        username: Admin username
        password: Admin password (will be hashed)
        db_config: Database configuration (optional, defaults to sqlite eco_app.db)
        
    Returns:
        Boolean indicating success
    """
    if db_config is None:
        db_config = {'type': 'sqlite', 'database': 'eco_app.db'}
    
    connection = create_database_connection(db_config)
    if not connection:
        return False

    try:
        cursor = connection.cursor()
        
        # Check if admin already exists
        cursor.execute("SELECT id FROM users WHERE username = ? AND is_admin = 1", (username,))
        if cursor.fetchone():
            print(f"Admin user '{username}' already exists.")
            cursor.close()
            return True
            
        # Create admin user
        hashed_password = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (username, password, is_admin, reward_points) VALUES (?, ?, 1, 0)",
            (username, hashed_password)
        )
        connection.commit()
        cursor.close()
        print(f"Admin user '{username}' created successfully.")
        return True
    except Exception as e:
        print(f"Error creating admin user: {e}")
        return False
    finally:
        close_database_connection(connection)


def close_database_connection(connection):
    """
    Close database connection safely.
    
    Args:
        connection: Database connection object
    """
    if connection:
        try:
            connection.close()
        except Exception as e:
            print(f"Error closing database connection: {e}")


# Format helpers

def format_date(date_obj):
    """
    Format datetime object to readable string.
    
    Args:
        date_obj: datetime object
        
    Returns:
        Formatted date string
    """
    if date_obj:
        return date_obj.strftime('%B %d, %Y at %I:%M %p')
    return 'Recently'


def format_file_size(size_bytes):
    """
    Convert bytes to human-readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted size string
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


# Validation helpers

def validate_username(username):
    """
    Validate username format.
    
    Args:
        username: Username to validate
        
    Returns:
        Tuple (is_valid, error_message)
    """
    if not username or len(username.strip()) == 0:
        return False, "Username cannot be empty"
    
    if len(username) < 3:
        return False, "Username must be at least 3 characters"
    
    if len(username) > 50:
        return False, "Username cannot exceed 50 characters"
    
    if not username.replace('_', '').isalnum():
        return False, "Username can only contain letters, numbers, and underscores"
    
    return True, ""


def validate_password(password):
    """
    Validate password strength.
    
    Args:
        password: Password to validate
        
    Returns:
        Tuple (is_valid, error_message)
    """
    if not password or len(password.strip()) == 0:
        return False, "Password cannot be empty"
    
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    
    if len(password) > 255:
        return False, "Password is too long"
    
    return True, ""


def validate_activity_data(title, description, caption):
    """
    Validate activity form data.
    
    Args:
        title: Activity title
        description: Activity description
        caption: Activity caption
        
    Returns:
        Tuple (is_valid, error_message)
    """
    if not title or len(title.strip()) == 0:
        return False, "Activity title is required"
    
    if not description or len(description.strip()) == 0:
        return False, "Activity description is required"
    
    if not caption or len(caption.strip()) == 0:
        return False, "Activity caption is required"
    
    if len(title) > 200:
        return False, "Title cannot exceed 200 characters"
    
    if len(caption) > 500:
        return False, "Caption cannot exceed 500 characters"
    
    return True, ""
