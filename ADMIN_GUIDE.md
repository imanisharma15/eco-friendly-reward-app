# 🛡️ Admin Access Guide

## Quick Start - Admin Login

### Access the Admin Dashboard:
1. **Go to Admin Login:** `http://localhost:5000/admin/login`
2. **Login Credentials:**
   - Username: `admin`
   - Password: `admin123`
3. **Start Reviewing:** Once logged in, you'll see all pending activities

### From Main Login Page:
You can also access from the regular login page by clicking the **"Go to Admin Login"** link at the bottom.

---

## Admin Dashboard Features

### 📋 Pending Activities Queue
- View all activities awaiting review
- See activity title, description, and submission date
- Click "Review" to examine each activity in detail

### ✅ Review & Approve
- View full activity details including:
  - Uploaded media (photos/videos)
  - GPS coordinates
  - Photo timestamps
  - Device information
- Manually assign points (suggested: 25 for photos, 35 for videos)
- Add review notes
- Click "Approve & Award Points" to award and approve

### ❌ Reject Activities
- If activity doesn't meet standards, click "Reject Activity"
- Add notes explaining rejection
- Activity gets rejected status, user receives no points

### 📊 Dashboard Statistics
- Total pending activities
- Approved count
- Rejected count

---

## Point Assignment Guidelines

| Type | Base Points | With Bonuses | Notes |
|------|----------|----------|-------|
| Photo | 25 | 25-35 | Add bonuses for GPS, proof files, camera source |
| Video | 35 | 35-45 | Higher than photos (harder to fake) |
| Bonus: GPS | +5 | - | Activity has verified coordinates |
| Bonus: Proof File | +5 | - | Additional verification file provided |
| Bonus: Camera Source | +5 | - | Captured from mobile camera/device |

### Example Scoring:
- **Photo + GPS = 30 points**
- **Video + GPS + Camera Source = 45 points**
- **Photo with all bonuses = 35 points**

---

## User Journey

1. **User submits activity** → Status: "Pending Admin Review" (0 points)
2. **You (admin) review** → Check metadata and media
3. **You assign points** → Select appropriate value
4. **User receives points** → Only after admin approval
5. **Activity completed** → Status: "Approved" with points awarded

---

## Logging Out
Click the **"Logout"** button in the top-right corner to exit the admin dashboard.

---

## Troubleshooting

**"Invalid admin credentials"?**
- Verify username: `admin`
- Verify password: `admin123`
- Check that Flask app is running at `http://localhost:5000`

**Can't find admin link?**
- Go directly to: `http://localhost:5000/admin/login`
- Or click "Go to Admin Login" on the login/signup pages

**Admin user doesn't exist?**
- Run: `python create_admin.py` in the project folder
- Or restart the app: `python app.py`

---

## More Information
See [README.md](README.md) for complete project documentation.
