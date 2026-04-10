# Eco-Friendly Reward App - Full Stack Application

A complete web application built with Flask, SQLite, HTML, CSS, and JavaScript that allows users to track and share eco-friendly activities.

## Features

✅ **User Authentication System**
- Secure signup and login with password hashing
- Session-based user management
- Protected routes requiring authentication

✅ **Activity Management**
- Add eco-friendly activities with title, description, and caption
- Upload primary proof and secondary verification images/videos
- View all previous activities in chronological order
- Browser location capture and device metadata for proof
- Responsive and modern UI

✅ **Admin Review System**
- Manual point assignment by administrators
- Activity approval/rejection workflow
- Review dashboard with pending activities
- Admin authentication and secure access
- Detailed activity review with metadata inspection

✅ **Reward System**
- Points awarded based on activity type (photos/videos)
- Bonus points for verification features (GPS, proof files, camera source)
- User reward tracking and tier system
- Admin-controlled point assignment

✅ **Database**
- SQLite database with proper relationships
- User profiles with activity tracking
- Reward points added to user accounts
- Activity review status for uploaded media
- GPS and timestamp metadata stored for proof
- Timestamp tracking for all activities

✅ **Security**
- Password hashing using Werkzeug
- Secure file upload handling with validation
- SQL injection prevention using parameterized queries
- Session management for user authentication
- Admin-only access controls

## Project Structure

```
eco_app/
├── app.py                      # Main Flask application
├── helpers.py                  # Database and utility functions
├── setup_admin.py              # Admin user creation script
├── requirements.txt            # Python dependencies
├── database_setup.sql          # Database initialization script
├── static/
│   └── uploads/               # Upload directory for user files
└── templates/
    ├── login.html             # Login page
    ├── signup.html            # Account creation page
    ├── activity.html          # Main application page
    ├── admin_login.html       # Admin login page
    ├── admin_dashboard.html   # Admin review dashboard
    └── admin_review.html      # Individual activity review page
```

## Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Run the Application

```bash
python app.py
```

The app will automatically:
- Create the SQLite database (`eco_app.db`) if it doesn't exist
- Set up the required tables
- Create a default admin user (if not already created)

**Default Admin Credentials:**
- Username: `admin`
- Password: `admin123`

### Step 4: Access the Application

Open your browser and go to `http://localhost:5000`

**User Login:** `http://localhost:5000/`
- Login or create a new account
- Look for the "Go to Admin Login" link at the bottom

**Admin Login:** `http://localhost:5000/admin/login`
- Username: `admin`
- Password: `admin123`

## Usage

### First Time Users - Regular Account

1. **Create Account**
   - Click "Sign up here" on the login page
   - Enter a username and password (minimum 6 characters)
   - Click "Create Account"

2. **Login**
   - Enter your credentials
   - Click "Login"

### Using the App

1. **Add Activity**
   - Fill in Activity Title (e.g., "Planted 10 Trees")
   - Add Description with details about the activity
   - Add a Caption or hashtag (e.g., "#GoGreen")
   - Optionally upload an image or video
   - Click "Submit Activity"

2. **View Activities**
   - All your activities are displayed below the form
   - Activities are sorted by most recent first
   - Images and videos are displayed inline
   - Each activity shows the date it was created

3. **Logout**
   - Click the "Logout" button in the top-right corner
   - You'll be returned to the login page

### Admin Review System

1. **Admin Login**
   - Go to `/admin/login`
   - Enter your admin credentials (created with `setup_admin.py`)
   - Access the review dashboard

2. **Review Dashboard**
   - View all pending activities awaiting review
   - See statistics: pending, approved, rejected counts
   - Click "Review" on any activity to evaluate it

3. **Review Process**
   - View activity details, description, and uploaded media
   - Check verification metadata (GPS, timestamp, device info)
   - Assign points manually (suggested: 25 for photos, 35 for videos)
   - Add review notes explaining your decision
   - Choose: "Approve & Award Points" or "Reject Activity"

4. **Point Assignment Guidelines**
   - **Photos**: 25 base points
   - **Videos**: 35 base points (harder to fake)
   - **Bonuses**: +5 for GPS, +5 for proof files, +5 for camera source
   - **Total range**: 0-50+ points based on quality and verification

## Test Account

Username: `testuser`
Password: `password123`

This account is pre-populated with test data to explore the application.

## File Upload Guidelines

**Supported Image Formats:** PNG, JPG, JPEG, GIF
**Supported Video Formats:** MP4, AVI, MOV, WEBM
**Maximum File Size:** 50 MB

Files are automatically named with timestamps to prevent conflicts.

## Database Schema

### Users Table
```
- id (Primary Key)
- username (Unique)
- password (Hashed)
- created_at (Timestamp)
```

### Activities Table
```
- id (Primary Key)
- user_id (Foreign Key → users.id)
- title (String)
- description (Text)
- caption (String)
- file_path (String - path to uploaded file)
- created_at (Timestamp)
```

## API Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Redirect to activity or login |
| `/signup` | GET, POST | Handle user registration |
| `/login` | GET, POST | Handle user authentication |
| `/logout` | GET | Clear session and logout |
| `/activity` | GET | Display activity page (protected) |
| `/submit_activity` | POST | Submit new activity (protected) |

## Security Features

- **Password Hashing:** Uses Werkzeug's `generate_password_hash()` with scrypt
- **Session Management:** Secure session cookies with secret key
- **File Validation:** Only allowed file types can be uploaded
- **SQL Safety:** All queries use parameterized statements to prevent SQL injection
- **File Safety:** Uploaded files are renamed with timestamps using `secure_filename()`
- **Authentication:** Protected routes check for active session

## Troubleshooting

### "Database connection error"
- Ensure MySQL is running
- Check database credentials in `app.py`
- Verify `eco_app` database exists

### "File upload failed"
- Check if `static/uploads/` directory exists and is writable
- Verify file size is under 50MB
- Ensure file format is supported

### "Login failed"
- Verify username and password are correct
- Ensure user exists in database
- Check MySQL connection

### "Activities not loading"
- Clear browser cookies/cache
- Restart Flask application
- Check MySQL database connection

## Performance Notes

- Database queries use indexes on `user_id` for fast retrieval
- File uploads are optimized with secure filename handling
- Timestamps are stored in MySQL for efficient sorting

## Future Enhancements

- Social sharing features
- Leaderboard/ranking system
- Badge/achievement system
- Comments and likes on activities
- Email notifications
- Profile pictures
- Activity categories/tags
- Search and filtering
- Data export functionality

## License

This project is open source and available for educational purposes.

## Support

For issues or questions, please check the troubleshooting section or review the code comments for more details.

---

**Built with ❤️ for the environment**
