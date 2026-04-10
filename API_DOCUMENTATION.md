# Eco-Friendly Reward App - API Documentation

## Base URL
```
http://localhost:5000
```

## Authentication
The application uses Flask session-based authentication. Users must be logged in to access protected routes.

---

## Endpoints

### 1. Home Route
**GET** `/`

Redirects to the activity page if user is logged in, otherwise redirects to login page.

**Response:**
- Redirect to `/activity` (if authenticated)
- Redirect to `/login` (if not authenticated)

---

### 2. Sign Up
**GET/POST** `/signup`

#### GET Request
Returns the signup HTML form.

**Response:**
- Status: 200
- Content: signup.html template

#### POST Request
Creates a new user account.

**Request Body:**
```
- username (string, required): Unique username (3-50 characters)
- password (string, required): Password (minimum 6 characters)
- confirm_password (string, required): Password confirmation (must match password)
```

**Response - Success:**
- Status: 302 (Redirect)
- Redirects to: `/login`
- Creates new user record in database

**Response - Validation Errors:**
- Status: 200
- Content: signup.html with error message
- Error scenarios:
  - Username already exists
  - Passwords don't match
  - Password too short
  - Missing required fields

**Database Changes:**
- Inserts new record into `users` table
- Password is hashed using werkzeug.security.generate_password_hash()

---

### 3. Login
**GET/POST** `/login`

#### GET Request
Returns the login HTML form.

**Response:**
- Status: 200
- Content: login.html template

#### POST Request
Authenticates user and creates session.

**Request Body:**
```
- username (string, required): User's username
- password (string, required): User's password
```

**Response - Success:**
- Status: 302 (Redirect)
- Redirects to: `/activity`
- Creates session with:
  - session['user_id']: User's database ID
  - session['username']: User's username

**Response - Failure:**
- Status: 200
- Content: login.html with error message
- Error scenarios:
  - Invalid username or password
  - User not found
  - Database connection error

**Database Query:**
- Queries `users` table WHERE username = provided username
- Verifies password hash using werkzeug.security.check_password_hash()

---

### 4. Logout
**GET** `/logout`

Clears user session and logs out the user.

**Authentication:** Required (redirects to login if not authenticated)

**Response:**
- Status: 302 (Redirect)
- Redirects to: `/login`
- Clears all session data

---

### 5. Activity Page
**GET** `/activity`

Displays the activity management page with form and user's previous activities.

**Authentication:** Required

**Response - Success:**
- Status: 200
- Content: activity.html template
- Data passed to template:
  - `username`: Currently logged-in username
  - `activities`: List of user's activities (dict objects)
    - id: Activity ID
    - title: Activity title
    - description: Activity description
    - caption: Activity caption
    - file_path: Path to uploaded file (if exists)
    - created_at: DateTime object

**Response - Not Authenticated:**
- Status: 302 (Redirect)
- Redirects to: `/login`

**Database Query:**
```sql
SELECT id, title, description, caption, file_path, created_at 
FROM activities 
WHERE user_id = ? 
ORDER BY created_at DESC
```

---

### 6. Submit Activity
**POST** `/submit_activity`

Creates and saves a new activity.

**Authentication:** Required

**Request Format:** multipart/form-data

**Request Body:**
```
- title (string, required): Activity title (max 200 characters)
- description (string, required): Activity description
- caption (string, required): Activity caption (max 500 characters)
- file (file, optional): Image or video file
```

**File Upload Details:**
- Allowed image formats: PNG, JPG, JPEG, GIF
- Allowed video formats: MP4, AVI, MOV, WEBM
- Maximum file size: 50 MB
- Files are stored in: `static/uploads/`
- File naming: `YYYYMMDD_HHMMSS_originalname.ext`

**Response - Success:**
- Status: 302 (Redirect)
- Redirects to: `/activity`
- Creates new record in `activities` table
- If file uploaded, saves to `static/uploads/` directory

**Response - Not Authenticated:**
- Status: 302 (Redirect)
- Redirects to: `/login`

**Response - Validation Errors:**
- Status: 302 (Redirect to activity page)
- Activity not created if:
  - Required fields missing
  - Invalid file type
  - File upload fails

**Database Insert:**
```sql
INSERT INTO activities 
(user_id, title, description, caption, file_path, created_at) 
VALUES (?, ?, ?, ?, ?, NOW())
```

---

## Error Handling

### 404 - Page Not Found
**GET** any undefined route

**Response:**
- Status: 302 (Redirect)
- Redirects to: `/`

### 500 - Internal Server Error
Any unhandled exception in route handlers

**Response:**
- Status: 500
- Content: Error message

---

## Session Management

### Session Object
The Flask session stores:
```python
session = {
    'user_id': int,        # User's database ID
    'username': string     # User's username
}
```

### Session Security
- HttpOnly cookies enabled
- SameSite policy: Lax
- Expires after 24 hours of inactivity
- JWT not used (simple session-based auth)

---

## Database Schema

### Users Table
```sql
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Activities Table
```sql
CREATE TABLE activities (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    title VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    caption VARCHAR(500),
    file_path VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);
```

---

## Response Status Codes

| Status | Meaning |
|--------|---------|
| 200 | OK - Request successful, content returned |
| 302 | Found - Redirect response |
| 404 | Not Found - Route does not exist |
| 500 | Internal Server Error |

---

## Content Types

| Endpoint | Request | Response |
|----------|---------|----------|
| /signup | application/x-www-form-urlencoded | text/html |
| /login | application/x-www-form-urlencoded | text/html |
| /activity | (GET only) | text/html |
| /submit_activity | multipart/form-data | (redirect) |

---

## Rate Limiting
No rate limiting implemented. For production, consider adding:
- Login attempt limits
- File upload limits
- Request throttling

---

## Testing

### Test Account
- Username: `testuser`
- Password: `password123`

### cURL Examples

#### Sign Up
```bash
curl -X POST http://localhost:5000/signup \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=newuser&password=pass123&confirm_password=pass123"
```

#### Login
```bash
curl -X POST http://localhost:5000/login \
  -c cookies.txt \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=testuser&password=password123"
```

#### Get Activity Page
```bash
curl -X GET http://localhost:5000/activity \
  -b cookies.txt
```

#### Submit Activity
```bash
curl -X POST http://localhost:5000/submit_activity \
  -b cookies.txt \
  -F "title=New Activity" \
  -F "description=Activity description" \
  -F "caption=#GoGreen" \
  -F "file=@image.jpg"
```

---

## Security Considerations

1. **Password Security**
   - Passwords are hashed using scrypt
   - Plaintext passwords never stored
   - Password validation on client and server side

2. **SQL Injection Prevention**
   - All queries use parameterized statements
   - User input never directly in SQL

3. **File Upload Security**
   - File extension whitelist validation
   - Filename sanitization with secure_filename()
   - Timestamp in filename to prevent overwrite
   - File size limit (50MB)

4. **Session Security**
   - HttpOnly cookies (no JavaScript access)
   - SameSite cookie policy
   - Session data stored server-side (Flask sessions)

5. **CSRF Protection**
   - Implement CSRF tokens in production
   - Currently missing - should be added for production

---

## Future Enhancements

- Add JWT token-based authentication
- Implement CSRF protection
- Add API rate limiting
- Add comprehensive logging
- Add request validation middleware
- Add data encryption for sensitive fields
- Add activity deletion and editing
- Add user profile endpoints
- Add activity filtering/search endpoints
