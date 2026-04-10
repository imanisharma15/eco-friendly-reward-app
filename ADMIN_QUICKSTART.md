# 🚀 QUICK START - Admin Access

## ✅ FIXED! Admin System is Ready

### Admin Credentials (ALREADY CREATED)
```
Username: admin
Password: admin123
```

### 📍 Access Points

| Role | URL | Purpose |
|------|-----|---------|
| **Regular User** | http://localhost:5000 | Submit activities, view your posts |
| **Admin** | http://localhost:5000/admin/login | Review & approve activities |

### 🔗 Where to Find Admin Link

1. **On Login Page** → Scroll down, click "Go to Admin Login" 
2. **On Signup Page** → Scroll down, click "Go to Admin Login"
3. **Direct URL** → http://localhost:5000/admin/login

---

## 🎯 How to Use Admin Dashboard

### Step 1: Login as Admin
```
Go to: http://localhost:5000/admin/login
Username: admin
Password: admin123
```

### Step 2: Review Activities
- See all pending activities in the dashboard
- Click "Review" on any activity
- View full details, photos, videos, GPS data

### Step 3: Assign Points
- Suggest: **25 points** for photos
- Suggest: **35 points** for videos
- Add **+5** for each: GPS location, proof files, camera source
- Maximum points: 

### Step 4: Approve or Reject
- Click **"Approve & Award Points"** → Points added to user
- Click **"Reject Activity"** → Activity rejected, no points

---

## 📊 Point Scoring

```
Base Scores:
- Photo: 25 points
- Video: 35 points

Bonuses (+5 each):
- GPS coordinates captured ✓
- Proof/verification file ✓
- Camera/mobile device source ✓

Example: Video + GPS + Camera = 35 + 5 + 5 = 45 points
```

---

## 🐛 Troubleshooting

**Q: "Invalid admin credentials"**  
A: Check that:
- Username is exactly: `admin`
- Password is exactly: `admin123`
- Flask app is running (http://localhost:5000 loads)

**Q: I can't see the admin link on login page**  
A: Go directly to: `http://localhost:5000/admin/login`

**Q: Admin user doesn't exist**  
A: It should be created automatically. Restart the app:
```bash
python app.py
```

---

## 📚 Full Documentation

- **Complete Guide:** See [ADMIN_GUIDE.md](ADMIN_GUIDE.md)
- **README:** See [README.md](README.md)

---

## 🎬 Complete Workflow

```
1. User submits activity
   ↓
2. Status: "Pending Admin Review" (0 points)
   ↓
3. You review at /admin/login
   ↓
4. You assign points (25-50 range)
   ↓
5. Click "Approve"
   ↓
6. User gets points in their account
```

---

**Ready?** Open http://localhost:5000/admin/login and start reviewing! 🛡️
