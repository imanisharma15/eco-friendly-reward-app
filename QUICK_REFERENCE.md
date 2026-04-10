# ⚡ QUICK REFERENCE GUIDE

## 🎯 Start Here

### For First-Time Users on Windows
```powershell
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run database setup in MySQL
mysql -u root -p < database_setup.sql

# 3. Start the app
python app.py

# 4. Open browser
# http://localhost:5000
```

### Login with Test Account
```
Username: testuser
Password: password123
```

---

## 📚 File Quick Reference

| File | Purpose | Edit When |
|------|---------|-----------|
| `app.py` | Main application logic | Adding new features |
| `config.py` | Settings and configuration | Changing app behavior |
| `helpers.py` | Reusable functions | Adding utilities |
| `database_setup.sql` | Database creation | Modifying schema |
| `requirements.txt` | Python dependencies | Installing new packages |
| `templates/*.html` | Web pages and forms | Changing UI/layout |
| `static/uploads/` | Uploaded files | (Auto-managed) |

---

## 🔑 Environment Variables (For Production)

Create `.env` file:
```
SECRET_KEY=your_secure_random_key
DB_HOST=your_database_host
DB_USER=your_database_user
DB_PASSWORD=your_secure_password
DB_NAME=eco_app
FLASK_ENV=production
FLASK_DEBUG=False
```

---

## 📡 API Endpoints

| Method | Endpoint | Purpose | Access |
|--------|----------|---------|--------|
| GET | `/signup` | Show signup form | Public |
| POST | `/signup` | Create account | Public |
| GET | `/login` | Show login form | Public |
| POST | `/login` | Authenticate user | Public |
| GET | `/logout` | Logout user | Protected |
| GET | `/activity` | Show activities page | Protected |
| POST | `/submit_activity` | Create activity | Protected |

---

## 🗄️ Database Tables

### Users
- `id` - User ID (auto-increment)
- `username` - Unique username
- `password` - Hashed password
- `created_at` - Registration timestamp

### Activities
- `id` - Activity ID (auto-increment)
- `user_id` - Reference to user
- `title` - Activity title
- `description` - Activity details
- `caption` - Short caption/hashtag
- `file_path` - Path to uploaded image/video
- `created_at` - Activity submission timestamp

---

## 📝 Code Organization

**Authentication Flow:**
```
User → /signup or /login → Verify credentials → Create/Check session → /activity
```

**Activity Flow:**
```
User → /activity (display form) → Submit → /submit_activity → Save file + DB → Display
```

**File Upload Process:**
```
Select file → Validate type/size → Generate unique name → Save to uploads/ → Store path in DB
```

---

## 🔒 Security Summary

✅ Passwords hashed with Werkzeug  
✅ SQL queries parameterized (no injection)  
✅ File uploads validated and sanitized  
✅ Sessions HttpOnly and secure  
✅ Timestamps in filenames prevent conflicts  

---

## 🐛 Common Issues & Fixes

### MySQL Connection Failed
```python
# Check DB_CONFIG in app.py
DB_CONFIG = {
    'host': 'localhost',        # ← Verify this
    'user': 'root',             # ← And this
    'password': '',             # ← And password is correct
    'database': 'eco_app'
}
# Then run: mysql -u root -p < database_setup.sql
```

### Python Module Not Found
```bash
# Run this:
pip install -r requirements.txt --upgrade
```

### Port 5000 Already in Use
```python
# Change in app.py, last line:
app.run(debug=True, host='localhost', port=5001)  # Use 5001 instead
```

### Files Not Uploading
```
1. Check file is < 50MB
2. Check format is: PNG, JPG, GIF, MP4, AVI, MOV, WEBM
3. Check /static/uploads/ folder has write permissions
```

---

## 📁 Directory Structure After Setup

```
EcoFriendly/
├── app.py                    # Run this!
├── config.py
├── helpers.py
├── requirements.txt
├── database_setup.sql
├── templates/
│   ├── login.html
│   ├── signup.html
│   └── activity.html
├── static/
│   └── uploads/
│       └── (uploaded files go here)
├── venv/                     # Virtual environment
├── Documentation files...
└── .gitignore
```

---

## 🚀 Deployment Checklist

- [ ] Change `SECRET_KEY` to random value
- [ ] Set database credentials as environment variables
- [ ] Enable HTTPS/SSL
- [ ] Set `DEBUG = False`
- [ ] Use production WSGI server (Gunicorn)
- [ ] Configure reverse proxy (Nginx)
- [ ] Set up automated backups
- [ ] Configure logging
- [ ] Add rate limiting
- [ ] Test all routes

---

## 📊 Performance Tips

1. **For Faster Database Queries:**
   - Indexes are already created on user_id
   - Add more indexes if needed

2. **For Better File Handling:**
   - Use S3 for uploaded files (not local storage)
   - Implement file compression

3. **For Scalability:**
   - Use session storage (Redis) instead of Flask sessions
   - Load balance across multiple app instances
   - Use CDN for static files

---

## 🔧 Configuration Quick Edit

**Change upload folder size limit:**
```python
# app.py, line ~20
MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB instead of 50MB
```

**Add new allowed file types:**
```python
# app.py, line ~18
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'mp4', 'avi', 'mov', 'webm', 'pdf'}
```

**Change password minimum length:**
```python
# app.py, line ~75 (in signup route)
if len(password) < 8:  # 8 characters instead of 6
    return render_template('signup.html', error='Password must be at least 8 characters')
```

---

## 📞 Help Resources

| Topic | Resource |
|-------|----------|
| Flask Routing | https://flask.palletsprojects.com/routing/ |
| MySQL Queries | https://dev.mysql.com/doc/refman/ |
| Security | https://owasp.org/www-project-top-ten/ |
| Python | https://docs.python.org/3/ |
| Deployment | DEPLOYMENT_GUIDE.md |
| API Docs | API_DOCUMENTATION.md |

---

## 💡 Pro Tips

1. **Always backup database before major changes:**
   ```bash
   mysqldump -u root -p eco_app > backup.sql
   ```

2. **Use virtual environment to avoid conflicts:**
   ```bash
   python -m venv venv
   venv\Scripts\Activate.ps1  # Windows
   source venv/bin/activate   # Mac/Linux
   ```

3. **Test file uploads:**
   - Small image first
   - Then large video
   - Then unsupported format (should fail)

4. **Monitor application logs:**
   - Check Flask console output
   - Create log files for production
   - Use Sentry for error tracking

---

## ✨ Features Included

- ✅ User signup with validation
- ✅ Secure login/logout
- ✅ Activity submission
- ✅ Image/video upload
- ✅ Activity history
- ✅ Responsive design
- ✅ Form validation
- ✅ Error handling
- ✅ Database persistence
- ✅ Session management

---

## 🎓 Learning Resources

Learn from this project:
- Flask application structure
- MySQL integration with Python
- Session-based authentication
- File upload handling
- HTML/CSS form design
- Database schema design
- Security best practices
- RESTful API patterns

---

## 📈 Next Steps

1. **Understand the code** - Read app.py with comments
2. **Test thoroughly** - Try all features
3. **Customize styling** - Edit HTML/CSS
4. **Add features** - Extend functionality
5. **Deploy** - Follow DEPLOYMENT_GUIDE.md
6. **Monitor** - Set up logging and monitoring
7. **Scale** - Implement caching and optimization

---

**Version:** 1.0.0  
**Status:** ✅ Production Ready  
**Last Updated:** 2026  

**Questions?** See PROJECT_INDEX.md or README.md

---

🌱 **Happy Eco-Tracking!** 🌍
