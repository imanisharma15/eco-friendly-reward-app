# Eco-Friendly Reward App - Deployment & Best Practices

## Development vs Production

### Current Development Setup
- Debug mode: ON
- Secret key: Hardcoded
- Database: Local MySQL
- HTTPS: Not enabled
- Suitable for: Local testing only

### Production Considerations

#### 1. Security

**Secret Key**
```python
# ❌ NEVER use in production:
app.secret_key = 'eco_app_secret_key_2026'

# ✅ Instead, use:
import os
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(16))
```

**HTTPS/SSL**
```python
# Production app should enforce HTTPS
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['PREFERRED_URL_SCHEME'] = 'https'
```

**Password Hashing**
The app already uses werkzeug.security for password hashing - this is good.

#### 2. Database Security

**Store credentials as environment variables:**
```python
import os
from dotenv import load_dotenv

load_dotenv()

DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'localhost'),
    'user': os.environ.get('DB_USER', 'root'),
    'password': os.environ.get('DB_PASSWORD', ''),
    'database': os.environ.get('DB_NAME', 'eco_app')
}
```

**Create .env file (DO NOT commit):**
```
DB_HOST=your_db_host
DB_USER=your_db_user
DB_PASSWORD=your_secure_password
DB_NAME=eco_app
SECRET_KEY=your_random_secret_key
```

#### 3. File Upload Security

Current implementation is secure with:
- ✅ File type whitelist validation
- ✅ Filename sanitization
- ✅ Unique filename generation
- ✅ File size limit

However, add these for production:
```python
# Scan uploaded files for viruses (requires 3rd party service)
# Consider implementing antivirus scanning
# Example: python-magic for file type detection

# Store uploads outside web root
UPLOAD_FOLDER = '/var/data/eco_app/uploads'  # Outside /static/
```

#### 4. Debugging

```python
# ❌ Never in production:
if __name__ == '__main__':
    app.run(debug=True)

# ✅ Use production WSGI server instead:
# gunicorn app:app --workers 4 --bind 0.0.0.0:5000
```

---

## Deployment Options

### Option 1: Heroku

**Steps:**
1. Install Heroku CLI
2. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```
3. Create `runtime.txt`:
   ```
   python-3.9.16
   ```
4. Push to Heroku:
   ```bash
   heroku create your-app-name
   heroku config:set SECRET_KEY=$(python -c 'import secrets; print(secrets.token_hex(16))')
   git push heroku main
   ```

**Environment Variables:**
```bash
heroku config:set DB_HOST=your_db_host
heroku config:set DB_USER=your_db_user
heroku config:set DB_PASSWORD=your_password
```

### Option 2: AWS (EC2 + RDS)

**Flask Setup:**
1. Use Gunicorn as WSGI server:
   ```bash
   pip install gunicorn
   gunicorn --bind 0.0.0.0:5000 app:app
   ```

2. Use Nginx as reverse proxy
3. Configure with supervisor or systemd

**Database:**
- Use AWS RDS for managed MySQL
- Update DB_CONFIG with RDS endpoint

**File Storage:**
- Use AWS S3 for uploaded files instead of local storage
- Install boto3: `pip install boto3`

### Option 3: DigitalOcean

**App Platform (Easiest):**
1. Connect GitHub repository
2. Set environment variables in dashboard
3. Deploy with one click

**Droplet (More Control):**
1. SSH into droplet
2. Install Python, MySQL, Nginx
3. Deploy using Git
4. Use Gunicorn + Supervisor

### Option 4: Docker

**Dockerfile:**
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
```

**Docker Compose:**
```yaml
version: '3.8'
services:
  web:
    build: .
    ports:
      - "5000:5000"
    environment:
      - DB_HOST=db
      - DB_USER=root
      - DB_PASSWORD=root_password
  db:
    image: mysql:8.0
    environment:
      - MYSQL_ROOT_PASSWORD=root_password
      - MYSQL_DATABASE=eco_app
    volumes:
      - mysql_data:/var/lib/mysql

volumes:
  mysql_data:
```

---

## Performance Optimization

### 1. Database Optimization

**Add indexes:**
```sql
-- Already in schema, but verify:
CREATE INDEX idx_user_id ON activities(user_id);
CREATE INDEX idx_username ON users(username);
```

**Connection pooling:**
```python
from mysql.connector import pooling

db_pool = pooling.MySQLConnectionPool(
    pool_name="eco_app_pool",
    pool_size=5,
    **DB_CONFIG
)

def get_connection():
    return db_pool.get_connection()
```

### 2. Caching

**Flask-Caching:**
```bash
pip install Flask-Caching
```

```python
from flask_caching import Cache

cache = Cache(app, config={'CACHE_TYPE': 'simple'})

@app.route('/activity')
@cache.cached(timeout=60)
def activity():
    # This will be cached for 60 seconds
    ...
```

### 3. File Optimization

- Compress images: `PIL/Pillow`
- Generate thumbnails for previews
- Use CDN for file delivery

```bash
pip install Pillow
```

### 4. Frontend Optimization

- Minify CSS and JavaScript
- Use lazy loading for images
- Enable gzip compression in Nginx

---

## Monitoring & Logging

### Logging Configuration

```python
import logging
from logging.handlers import RotatingFileHandler

# Create logs directory
if not os.path.exists('logs'):
    os.mkdir('logs')

file_handler = RotatingFileHandler('logs/eco_app.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
```

### Monitoring Tools

- **Sentry**: Error tracking
- **New Relic**: Performance monitoring
- **DataDog**: Infrastructure monitoring
- **Prometheus**: Metrics collection

---

## Backup Strategy

### Database Backups

**Automated daily backup:**
```bash
#!/bin/bash
mysqldump -u root -p'password' eco_app > /backups/eco_app_$(date +%Y%m%d).sql
```

**Store backups:**
- AWS S3
- Google Cloud Storage
- GitHub (for important versions)

### File Backups

```bash
# Backup uploads folder
tar -czf /backups/uploads_$(date +%Y%m%d).tar.gz /path/to/uploads/
```

---

## Scaling Considerations

### Horizontal Scaling

1. **Load Balancer**
   - Distribute traffic across multiple app instances
   - Use AWS ELB, Nginx, or HAProxy

2. **Shared Session Storage**
   - Replace Flask sessions with Redis
   - `pip install flask-session redis`

3. **Shared File Storage**
   - Use AWS S3 instead of local storage
   - Or NFS mount for distributed file system

### Vertical Scaling

- Increase server RAM and CPU
- Optimize database queries
- Use caching aggressively

---

## Testing Checklist

### Pre-Deployment
- [ ] All routes tested
- [ ] Database backup created
- [ ] Environment variables set
- [ ] HTTPS certificate configured
- [ ] Error pages customized
- [ ] Logging configured
- [ ] Security headers enabled
- [ ] CSRF protection enabled
- [ ] Rate limiting configured
- [ ] Backup strategy tested

### Post-Deployment
- [ ] Test login/signup
- [ ] Test activity creation
- [ ] Test file upload
- [ ] Monitor error logs
- [ ] Monitor performance
- [ ] Test email notifications (if added)
- [ ] Verify backups working
- [ ] SSL certificate valid

---

## Security Checklist

- [ ] Secret key is random and strong
- [ ] Database password is secure
- [ ] HTTPS enforced
- [ ] CSRF tokens implemented
- [ ] SQL injection prevention verified
- [ ] XSS protection enabled
- [ ] Rate limiting configured
- [ ] File upload validated
- [ ] Session timeouts configured
- [ ] Error messages don't leak info
- [ ] Logs don't contain sensitive data
- [ ] Dependencies updated
- [ ] No hardcoded secrets
- [ ] Security headers set

---

## Production Environment Variables

Required for production:
```
SECRET_KEY=random_secure_key_here
DB_HOST=production_database_host
DB_USER=database_user
DB_PASSWORD=secure_password
DB_NAME=eco_app
FLASK_ENV=production
FLASK_DEBUG=False
SERVER_NAME=yourdomain.com
MAX_CONTENT_LENGTH=52428800
```

---

## Troubleshooting Production Issues

### 500 Error
1. Check application logs
2. Verify database connection
3. Check file permissions
4. Review recent code changes

### Slow Performance
1. Check database queries (use EXPLAIN ANALYZE)
2. Review application logs for errors
3. Check server resources (CPU, RAM, Disk)
4. Monitor network connectivity

### Database Connection Issues
1. Verify MySQL is running
2. Check connection credentials
3. Verify firewall rules
4. Check database size

### File Upload Issues
1. Check disk space
2. Verify folder permissions
3. Check file size limits
4. Review logs for upload errors

---

## Support & Resources

- Flask Documentation: https://flask.palletsprojects.com/
- MySQL Documentation: https://dev.mysql.com/doc/
- Werkzeug Documentation: https://werkzeug.palletsprojects.com/
- Python Security: https://python.readthedocs.io/en/stable/library/security_warnings.html

---

**Happy Deploying! 🚀**
