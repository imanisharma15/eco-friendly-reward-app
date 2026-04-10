# Windows Quick Start Guide - Eco-Friendly Reward App

Follow these steps to get the application running on Windows.

## Prerequisites Installation

### 1. Install Python
- Download from https://www.python.org/downloads/
- **IMPORTANT:** Check "Add Python to PATH" during installation
- Verify installation by opening PowerShell and typing:
  ```powershell
  python --version
  ```

### 2. Database
This project now uses SQLite, which is built into Python. No separate database server installation is required.

## Application Setup

### Step 1: Navigate to Project Directory
```powershell
cd C:\Users\Asus\Desktop\EcoFriendly
```

### Step 2: Create Python Virtual Environment (Recommended)
```powershell
python -m venv venv
```

### Step 3: Activate Virtual Environment
```powershell
venv\Scripts\Activate.ps1
```

**Note:** If you get an execution policy error, run:
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Step 4: Install Dependencies
```powershell
pip install -r requirements.txt
```

### Step 5: Run the Application
```powershell
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

### Step 6: Access the Application
1. Open your web browser
2. Go to: `http://localhost:5000`
3. You'll be redirected to the login page

### Step 7: Test the App
```powershell
python app.py
```

You should see:
```
* Running on http://127.0.0.1:5000
* Debug mode: on
```

### Step 8: Access the Application
1. Open your web browser
2. Go to: `http://localhost:5000`
3. You'll be redirected to the login page

## Test the App

### Using Test Account
- **Username:** testuser
- **Password:** password123

### Create New Account
1. Click "Sign up here"
2. Enter a new username and password
3. Create your account
4. Login with your credentials

## Troubleshooting on Windows

### Issue: "Python not found"
**Solution:**
- Reinstall Python with "Add Python to PATH" checked
- Restart PowerShell after installation

### Issue: "Database connection error"
**Solution:**
- Ensure `eco_app.db` exists in the project folder after first app start
- Make sure the app has write permission to create the database file
- Restart the app if you updated `requirements.txt`

### Issue: "Module not found" or "pip install failed"
**Solution:**
- Ensure virtual environment is activated (you should see `(venv)` at start of prompt)
- Try upgrading pip:
  ```powershell
  python -m pip install --upgrade pip
  ```
- Then reinstall requirements:
  ```powershell
  pip install -r requirements.txt
  ```

### Issue: "Port 5000 already in use"
**Solution:**
- The application is trying to run on port 5000
- Either wait for the other process to finish, or
- Change the port in `app.py` (last line):
  ```python
  app.run(debug=True, host='localhost', port=5001)
  ```

### Issue: "Access Denied" for uploads
**Solution:**
- Run PowerShell as Administrator
- The `static/uploads/` folder needs write permissions

## File Locations

After setup, your project should look like:
```
C:\Users\Asus\Desktop\EcoFriendly\
├── app.py
├── requirements.txt
├── database_setup.sql
├── README.md
├── QUICKSTART_WINDOWS.md
├── .gitignore
├── static\
│   └── uploads\
├── templates\
│   ├── login.html
│   ├── signup.html
│   └── activity.html
└── venv\  (after running virtual environment)
```

## Stopping the Application

In PowerShell, press: `Ctrl + C`

## Deactivating Virtual Environment

```powershell
deactivate
```

## Next Steps

1. Explore the application features
2. Create activities and upload files
3. Review the code comments for implementation details
4. Check README.md for detailed documentation

## Tips

- Keep MySQL running in the background
- Always activate the virtual environment before running
- Browse `http://localhost:5000` while Flask is running
- Check the PowerShell console for any error messages

---

**Happy Eco-Tracking! 🌱**
