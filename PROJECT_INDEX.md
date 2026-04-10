# 🌱 Eco-Friendly Reward App - Project Index

## Project Overview

A complete, production-ready full-stack web application for tracking and sharing eco-friendly activities. Built with Flask (Python), MySQL, HTML, CSS, and JavaScript.

**Status:** ✅ Ready to Deploy  
**Version:** 1.0.0  
**Last Updated:** 2026

---

## 📁 Project Structure

```
eco_app/
├── 📄 app.py                    ← Main Flask application (start here!)
├── 📄 config.py                 ← Configuration settings
├── 📄 helpers.py                ← Utility functions and helpers
├── 📄 requirements.txt           ← Python dependencies
│
├── 🗄️ database_setup.sql        ← Database creation script
│
├── 📚 Documentation/
│   ├── 📖 README.md             ← Full project documentation
│   ├── 🚀 QUICKSTART_WINDOWS.md ← Windows setup guide
│   ├── 🌐 API_DOCUMENTATION.md  ← API endpoints reference
│   ├── 🔧 DEPLOYMENT_GUIDE.md   ← Production deployment
│   └── 📋 PROJECT_INDEX.md      ← This file
│
├── 📁 templates/                ← HTML templates
│   ├── login.html               ← Login page (form + styling)
│   ├── signup.html              ← Registration page (form + styling)
│   └── activity.html            ← Main app page (form + activity display)
│
├── 📁 static/
│   └── 📁 uploads/              ← User-uploaded files (auto-created)
│       └── .gitkeep             ← Maintains folder in git
│
├── 📄 .gitignore                ← Git ignore configuration
└── ⚙️ .env (not included)        ← Environment variables (create this!)
```

---

## 🚀 Quick Start

### For Windows Users (Recommended)
1. Read: **QUICKSTART_WINDOWS.md**
2. Run: `pip install -r requirements.txt`
3. Setup: Execute `database_setup.sql` in MySQL
4. Start: `python app.py`
5. Visit: `http://localhost:5000`

### For Mac/Linux Users
Follow the same steps but adjust paths for your OS.

### Test Credentials
- **Username:** `testuser`
- **Password:** `password123`

---

## 📖 Documentation Guide

### Getting Started
| Document | Purpose | Audience |
|----------|---------|----------|
| **README.md** | Complete feature overview and usage guide | Everyone |
| **QUICKSTART_WINDOWS.md** | Step-by-step Windows setup | Windows users |

### For Developers
| Document | Purpose | Audience |
|----------|---------|----------|
| **API_DOCUMENTATION.md** | All API endpoints, request/response formats | API developers |
| **code comments in app.py** | Line-by-line code explanation | Code reviewers |
| **helpers.py** | Reusable utility functions | Code maintainers |
| **config.py** | Configuration and settings | DevOps engineers |

### For Deployment
| Document | Purpose | Audience |
|----------|---------|----------|
| **DEPLOYMENT_GUIDE.md** | Production setup and best practices | DevOps/System admins |

---

## 🔧 File Descriptions

### Core Application Files

#### `app.py` (Main Application - 250+ lines)
**What it does:**
- Initializes Flask application
- Handles all HTTP routes
- Manages user authentication (signup, login, logout)
- Processes activity submissions
- Manages file uploads
- Interacts with MySQL database

**Key Functions:**
- `get_db_connection()` - MySQL connection management
- `signup()` - User registration route
- `login()` - User authentication route
- `logout()` - Session termination route
- `activity()` - Activity page display route
- `submit_activity()` - Activity creation route

**Dependencies:**
- Flask
- mysql-connector-python
- Werkzeug (for security)

#### `config.py` (Configuration)
**What it does:**
- Centralized configuration management
- Database settings
- File upload settings
- Security settings
- Session management settings

**Use:** Modify before production deployment

#### `helpers.py` (Utility Functions)
**What it does:**
- File validation functions
- Database helper functions
- Date formatting functions
- Input validation functions
- Filename generation

**Use:** Imported and reusable in app.py

### HTML Templates

#### `login.html` (Login Form)
- User authentication form
- Styled with gradient background
- Error message display
- Link to signup page
- Test account hint

#### `signup.html` (Registration Form)
- User registration form
- Password confirmation validation
- Username availability check
- Password strength requirements
- Link back to login

#### `activity.html` (Main Application)
- User welcome bar with logout
- Activity submission form
- Activity display feed
- Image/video preview
- Responsive design for mobile

### Configuration Files

#### `database_setup.sql`
SQL commands to:
- Create `eco_app` database
- Create `users` table
- Create `activities` table
- Add database indexes
- Insert test user

#### `requirements.txt`
Python package dependencies:
- Flask==2.3.3 - Web framework
- mysql-connector-python==8.2.0 - Database driver
- Werkzeug==2.3.7 - Security utilities

#### `.gitignore`
Prevents committing:
- Python cache files (`__pycache__/`)
- Virtual environment (`venv/`)
- Uploaded files (`static/uploads/*`)
- Environment variables (`.env`)
- IDE files (`.vscode/`, `.idea/`)

---

## 🔐 Security Features

✅ **Authentication**
- Password hashing with Werkzeug
- Session-based authentication
- Protected routes require login

✅ **Database**
- Parameterized SQL queries (SQL injection prevention)
- Foreign key constraints
- Cascade delete for data integrity

✅ **File Upload**
- Whitelist file type validation
- Filename sanitization
- File size limits (50MB max)
- Unique filename generation with timestamps
- Malicious file prevention

✅ **Session Security**
- HttpOnly cookies
- SameSite cookie policy
- 24-hour session timeout
- Secure logout functionality

⚠️ **Future Improvements**
- CSRF token implementation
- Rate limiting
- File virus scanning
- Two-factor authentication

---

## 📊 Database Schema

### Users Table
```sql
id (INT, Primary Key, Auto Increment)
username (VARCHAR 50, Unique)
password (VARCHAR 255, Hashed)
created_at (TIMESTAMP, Auto set)
```

### Activities Table
```sql
id (INT, Primary Key, Auto Increment)
user_id (INT, Foreign Key → users.id)
title (VARCHAR 200)
description (TEXT)
caption (VARCHAR 500)
file_path (VARCHAR 500)
created_at (TIMESTAMP, Auto set)
```

---

## 🌐 API Endpoints

3 User Authentication Routes:
- `POST /signup` - Create new account
- `POST /login` - Authenticate user
- `GET /logout` - End session

2 Activity Routes (Protected):
- `GET /activity` - View activities page
- `POST /submit_activity` - Create new activity

See **API_DOCUMENTATION.md** for detailed specifications.

---

## 💻 System Requirements

### Minimum
- Python 3.8+
- MySQL 5.7+ or MariaDB 10.3+
- 2GB RAM
- 100MB disk space

### Recommended
- Python 3.10+
- MySQL 8.0+
- 4GB RAM
- 1GB disk space

### Development
- VS Code or PyCharm IDE
- Postman for API testing (optional)
- MySQL Workbench (optional)

---

## 📋 Installation Checklist

- [ ] Python installed and added to PATH
- [ ] MySQL server installed and running
- [ ] Project folder created
- [ ] Python virtual environment created
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Database setup (`database_setup.sql` executed)
- [ ] Flask app started (`python app.py`)
- [ ] Can access `http://localhost:5000`
- [ ] Can login with test account
- [ ] Can create activities
- [ ] Can upload files

---

## 🚀 Next Steps After Installation

1. **Test the Application**
   - Try logging in with test account
   - Create a new account
   - Submit activities with and without files
   - Verify activities display correctly

2. **Customize for Your Needs**
   - Modify styling in HTML templates
   - Add new fields to activities
   - Implement additional features
   - Add more validation rules

3. **Deploy to Production**
   - Follow DEPLOYMENT_GUIDE.md
   - Set up HTTPS/SSL
   - Configure environment variables
   - Set up automatic backups
   - Monitor application performance

4. **Maintain the Application**
   - Set up error logging
   - Configure automated backups
   - Monitor server resources
   - Keep dependencies updated
   - Review security best practices

---

## 🔍 Common Tasks

### View Database Contents
```bash
mysql -u root -p
USE eco_app;
SELECT * FROM users;
SELECT * FROM activities;
```

### Debug Database Connection
Check `app.py` line ~28 for connection settings and ensure:
- MySQL is running
- Credentials are correct
- Port 3306 is accessible

### Add More Users
```sql
INSERT INTO users (username, password) 
VALUES ('newuser', 'hashed_password_here');
```

### Reset Database
```bash
DROP DATABASE eco_app;
# Then re-run database_setup.sql
```

### Change Upload Folder
Edit `app.py` line ~15:
```python
UPLOAD_FOLDER = '/your/custom/path'
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| MySQL Connection Error | Check MySQL is running, verify credentials in app.py |
| Module Not Found | Run `pip install -r requirements.txt` |
| Port 5000 Already in Use | Change port in app.py last line |
| Upload Fails | Check image/video is < 50MB and correct format |
| Template Not Found | Verify templates/ folder exists and files are there |
| Static Files Not Loading | Check static/ folder exists with uploads/ subfolder |

---

## 📞 Support Resources

- **Flask Docs:** https://flask.palletsprojects.com/
- **MySQL Docs:** https://dev.mysql.com/doc/
- **Werkzeug Docs:** https://werkzeug.palletsprojects.com/
- **Python Security:** https://python.readthedocs.io/

---

## 📝 License

This project is provided as-is for educational and personal use.

---

## ✨ Features Summary

✅ User authentication (signup/login/logout)  
✅ Activity submission with form validation  
✅ File upload (images and videos)  
✅ Activity history display  
✅ Responsive design  
✅ Session management  
✅ Database persistence  
✅ Secure password storage  
✅ Input validation and sanitization  
✅ Error handling  

---

## 🎯 Project Goals Met

✅ Complete working application  
✅ Proper database structure  
✅ Secure authentication system  
✅ File upload functionality  
✅ User-friendly interface  
✅ Production-ready code  
✅ Comprehensive documentation  
✅ Easy deployment  

---

**Application created with ❤️ for environmental sustainability and eco-friendly action tracking.**

**Happy tracking! 🌍🌱**
