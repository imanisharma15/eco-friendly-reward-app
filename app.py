from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime

import config
from helpers import (
    allowed_file,
    get_unique_filename,
    create_database_connection,
    close_database_connection,
    initialize_database,
    extract_image_metadata,
    validate_username,
    validate_password,
    validate_activity_data,
    create_admin_user,
)

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), config.UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = config.ALLOWED_EXTENSIONS
MAX_FILE_SIZE = config.MAX_FILE_SIZE

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

DB_CONFIG = config.DATABASE.copy()
DB_CONFIG['database'] = os.environ.get('DB_NAME', DB_CONFIG.get('database', 'eco_app.db'))
DB_CONFIG['type'] = 'sqlite'

initialize_database(DB_CONFIG)

# Automatically create default admin user if it doesn't exist
create_admin_user('admin', 'admin123', DB_CONFIG)


@app.template_filter('format_datetime')
def format_datetime(value):
    if not value:
        return 'Recently'
    if hasattr(value, 'strftime'):
        return value.strftime('%b %d, %Y')
    if isinstance(value, str):
        for fmt in ('%Y-%m-%d %H:%M:%S', '%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S', '%Y-%m-%dT%H:%M:%S.%f'):
            try:
                return datetime.strptime(value, fmt).strftime('%b %d, %Y')
            except ValueError:
                continue
        try:
            return datetime.fromisoformat(value).strftime('%b %d, %Y')
        except ValueError:
            return str(value)
    return str(value)


def get_db_connection():
    """Get a database connection using configuration settings."""
    return create_database_connection(DB_CONFIG)


def get_reward_tier(points):
    if points >= 1000:
        return 'Platinum'
    if points >= 500:
        return 'Gold'
    if points >= 250:
        return 'Silver'
    if points >= 100:
        return 'Bronze'
    return 'Starter'


def get_user_summary(user_id):
    summary = {'reward_points': 0, 'reward_tier': 'Starter'}
    connection = get_db_connection()
    if not connection:
        return summary

    try:
        cursor = connection.cursor()
        cursor.execute(
            "SELECT reward_points FROM users WHERE id = ?",
            (user_id,),
        )
        row = cursor.fetchone()
        cursor.close()
        if row:
            points = row['reward_points'] if isinstance(row, dict) else row[0]
            summary['reward_points'] = points
            summary['reward_tier'] = get_reward_tier(points)
    except Exception as e:
        print(f"Error fetching user summary: {e}")
    finally:
        close_database_connection(connection)

    return summary


def fetch_user_activities(user_id):
    """Fetch all activities for a given user."""
    activities = []
    connection = get_db_connection()
    if connection:
        try:
            cursor = connection.cursor()
            cursor.execute(
                """SELECT id, title, description, caption, file_path, proof_file_path, 
                          gps_lat, gps_lon, photo_timestamp, upload_source, device_info,
                          created_at, points_awarded, review_status
                   FROM activities
                   WHERE user_id = ?
                   ORDER BY created_at DESC""",
                (user_id,)
            )
            raw_activities = cursor.fetchall()
            cursor.close()

            for activity in raw_activities:
                created_at = activity['created_at'] if isinstance(activity, dict) else activity[5]
                if isinstance(created_at, str):
                    try:
                        created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
                    except ValueError:
                        try:
                            created_at = datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S.%f')
                        except ValueError:
                            created_at = None

                if isinstance(activity, dict):
                    activity['created_at'] = created_at
                    activities.append(activity)
                else:
                    activity = dict(activity)
                    activity['created_at'] = created_at
                    activities.append(activity)
        except Exception as e:
            print(f"Error fetching activities: {e}")
        finally:
            close_database_connection(connection)
    return activities


@app.route('/')
def index():
    """Redirect to login if not authenticated, otherwise to activity page."""
    return redirect(url_for('activity')) if 'user_id' in session else redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user signup."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')

        if not username or not password or not confirm_password:
            return render_template('signup.html', error='All fields are required')

        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match')

        valid, message = validate_username(username)
        if not valid:
            return render_template('signup.html', error=message)

        valid, message = validate_password(password)
        if not valid:
            return render_template('signup.html', error=message)

        hashed_password = generate_password_hash(password)
        connection = get_db_connection()
        if not connection:
            return render_template('signup.html', error='Database connection failed')

        try:
            cursor = connection.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                cursor.close()
                return render_template('signup.html', error='Username already exists')

            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, hashed_password),
            )
            connection.commit()
            cursor.close()
            return redirect(url_for('login'))
        except Exception as e:
            print(f"Database error: {e}")
            return render_template('signup.html', error='Unable to create user account')
        finally:
            close_database_connection(connection)

    return render_template('signup.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle user login."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            return render_template('login.html', error='Username and password are required')

        connection = get_db_connection()
        if not connection:
            return render_template('login.html', error='Database connection failed')

        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, username, password FROM users WHERE username = ?",
                (username,),
            )
            user = cursor.fetchone()
            cursor.close()

            if user and check_password_hash(user['password'], password):
                session['user_id'] = user['id']
                session['username'] = user['username']
                return redirect(url_for('activity'))
            return render_template('login.html', error='Invalid username or password')
        except Exception as e:
            print(f"Database error: {e}")
            return render_template('login.html', error='Unable to authenticate user')
        finally:
            close_database_connection(connection)

    return render_template('login.html')


@app.route('/logout')
def logout():
    """Handle user logout."""
    session.clear()
    return redirect(url_for('login'))


@app.route('/activity', methods=['GET'])
def activity():
    """Display activity page with previous user submissions."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    username = session.get('username')
    user_id = session.get('user_id')
    activities = fetch_user_activities(user_id)
    summary = get_user_summary(user_id)
    return render_template(
        'activity.html',
        username=username,
        activities=activities,
        reward_points=summary['reward_points'],
        reward_tier=summary['reward_tier'],
    )


@app.route('/submit_activity', methods=['POST'])
def submit_activity():
    """Handle new activity submissions."""
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session.get('user_id')
    username = session.get('username')
    title = request.form.get('title', '').strip()
    description = request.form.get('description', '').strip()
    caption = request.form.get('caption', '').strip()
    main_file = request.files.get('file_main')
    proof_file = request.files.get('file_proof')
    gps_lat = request.form.get('gps_lat')
    gps_lon = request.form.get('gps_lon')
    location_accuracy = request.form.get('location_accuracy')
    upload_source = request.form.get('upload_source', 'unknown')
    device_info = request.form.get('device_info', '')
    photo_timestamp_field = request.form.get('photo_timestamp')

    valid, message = validate_activity_data(title, description, caption)
    if not valid:
        activities = fetch_user_activities(user_id)
        return render_template(
            'activity.html',
            username=username,
            activities=activities,
            error=message,
        )

    if not main_file or not main_file.filename:
        activities = fetch_user_activities(user_id)
        return render_template(
            'activity.html',
            username=username,
            activities=activities,
            error='Please upload a primary photo or video as proof of your eco-friendly activity.',
        )

    if main_file and not allowed_file(main_file.filename, ALLOWED_EXTENSIONS):
        activities = fetch_user_activities(user_id)
        return render_template(
            'activity.html',
            username=username,
            activities=activities,
            error='Unsupported file type for the main file. Please upload PNG, JPG, GIF, MP4, AVI, MOV, or WEBM.',
        )

    if proof_file and proof_file.filename and not allowed_file(proof_file.filename, ALLOWED_EXTENSIONS):
        activities = fetch_user_activities(user_id)
        return render_template(
            'activity.html',
            username=username,
            activities=activities,
            error='Unsupported file type for the proof file.',
        )

    main_file_path = None
    proof_file_path = None
    extracted_lat = None
    extracted_lon = None
    photo_timestamp = None

    try:
        main_filename = get_unique_filename(main_file.filename)
        main_saved_path = os.path.join(app.config['UPLOAD_FOLDER'], main_filename)
        main_file.save(main_saved_path)
        main_file_path = f"uploads/{main_filename}"

        if main_filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            metadata = extract_image_metadata(main_saved_path)
            extracted_lat = metadata['gps_lat']
            extracted_lon = metadata['gps_lon']
            photo_timestamp = metadata['photo_timestamp']

        if proof_file and proof_file.filename:
            proof_filename = get_unique_filename(proof_file.filename)
            proof_saved_path = os.path.join(app.config['UPLOAD_FOLDER'], proof_filename)
            proof_file.save(proof_saved_path)
            proof_file_path = f"uploads/{proof_filename}"
    except Exception as e:
        print(f"File upload error: {e}")
        activities = fetch_user_activities(user_id)
        return render_template(
            'activity.html',
            username=username,
            activities=activities,
            error='Unable to upload one or more files. Please try again.',
        )

    if gps_lat and gps_lon:
        try:
            gps_lat = float(gps_lat)
            gps_lon = float(gps_lon)
        except ValueError:
            gps_lat = None
            gps_lon = None

    if extracted_lat is None and extracted_lon is None:
        extracted_lat = gps_lat
        extracted_lon = gps_lon

    if not photo_timestamp and photo_timestamp_field:
        try:
            photo_timestamp = datetime.fromisoformat(photo_timestamp_field)
        except ValueError:
            photo_timestamp = None

    review_status = 'pending'
    suspicious = False
    if extracted_lat and extracted_lon and photo_timestamp:
        review_status = 'pending_review'

    if 'tree' not in title.lower() and 'plant' not in title.lower() and 'tree' not in description.lower():
        suspicious = True

    connection = get_db_connection()
    if not connection:
        activities = fetch_user_activities(user_id)
        return render_template(
            'activity.html',
            username=username,
            activities=activities,
            error='Database connection failed',
        )

    try:
        # Calculate proposed points (for admin reference only)
        proposed_points = 10
        
        # Determine file type and award media-specific bonuses
        main_filename = main_file.filename.lower()
        is_image = main_filename.endswith(('.png', '.jpg', '.jpeg', '.gif'))
        is_video = main_filename.endswith(('.mp4', '.avi', '.mov', '.webm'))
        
        if is_image:
            proposed_points += 15  # Bonus for photo uploads
        elif is_video:
            proposed_points += 25  # Higher bonus for video uploads (harder to fake)
        
        # Additional bonuses for verification features
        if proof_file_path:
            proposed_points += 5
        if extracted_lat and extracted_lon:
            proposed_points += 5
        if 'camera' in upload_source.lower() or 'mobile' in device_info.lower():
            proposed_points += 5

        review_status = 'pending_admin_review'

        cursor = connection.cursor()
        cursor.execute(
            """INSERT INTO activities
               (user_id, title, description, caption, file_path, proof_file_path, gps_lat, gps_lon, photo_timestamp, upload_source, device_info, points_awarded, review_status, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                user_id,
                title,
                description,
                caption,
                main_file_path,
                proof_file_path,
                extracted_lat,
                extracted_lon,
                photo_timestamp.isoformat() if photo_timestamp else None,
                upload_source,
                device_info,
                0,  # Start with 0 points until admin review
                review_status,
                datetime.now(),
            ),
        )
        # Don't update user reward_points here - wait for admin approval
        connection.commit()
        cursor.close()
        activities = fetch_user_activities(user_id)
        media_type = "photo" if is_image else "video" if is_video else "file"
        status_message = f'Activity submitted successfully! Your {media_type} upload is pending admin review. Proposed points: {proposed_points}.'
        return render_template(
            'activity.html',
            username=username,
            activities=activities,
            success=status_message,
        )
    except Exception as e:
        print(f"Database error: {e}")
        activities = fetch_user_activities(user_id)
        return render_template(
            'activity.html',
            username=username,
            activities=activities,
            error='Unable to save your activity. Please try again later.',
        )
    finally:
        close_database_connection(connection)


# Admin Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page."""
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        if not username or not password:
            return render_template('admin_login.html', error='Please provide both username and password.')

        connection = get_db_connection()
        if not connection:
            return render_template('admin_login.html', error='Database connection failed.')

        try:
            cursor = connection.cursor()
            cursor.execute(
                "SELECT id, password, is_admin FROM users WHERE username = ?",
                (username,)
            )
            user = cursor.fetchone()
            cursor.close()

            if user and check_password_hash(user[1], password) and user[2] == 1:
                session['admin_id'] = user[0]
                session['admin_username'] = username
                return redirect(url_for('admin_dashboard'))
            else:
                return render_template('admin_login.html', error='Invalid admin credentials.')
        except Exception as e:
            print(f"Admin login error: {e}")
            return render_template('admin_login.html', error='Login failed. Please try again.')
        finally:
            close_database_connection(connection)

    return render_template('admin_login.html')


@app.route('/admin/logout')
def admin_logout():
    """Admin logout."""
    session.pop('admin_id', None)
    session.pop('admin_username', None)
    return redirect(url_for('admin_login'))


@app.route('/admin')
def admin_dashboard():
    """Admin dashboard showing pending activities."""
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    connection = get_db_connection()
    if not connection:
        return render_template('admin_dashboard.html', error='Database connection failed.')

    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT a.id, a.title, a.description, a.created_at, a.review_status, a.points_awarded,
                   u.username, a.file_path, a.proof_file_path
            FROM activities a
            JOIN users u ON a.user_id = u.id
            WHERE a.review_status = 'pending_admin_review'
            ORDER BY a.created_at DESC
            """
        )
        pending_activities = cursor.fetchall()

        # Get review statistics
        cursor.execute("SELECT COUNT(*) FROM activities WHERE review_status = 'pending_admin_review'")
        pending_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM activities WHERE review_status = 'approved'")
        approved_count = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM activities WHERE review_status = 'rejected'")
        rejected_count = cursor.fetchone()[0]

        cursor.close()

        activities_data = []
        for activity in pending_activities:
            activities_data.append({
                'id': activity[0],
                'title': activity[1],
                'description': activity[2],
                'created_at': activity[3],
                'review_status': activity[4],
                'points_awarded': activity[5],
                'username': activity[6],
                'file_path': activity[7],
                'proof_file_path': activity[8]
            })

        return render_template('admin_dashboard.html',
                             activities=activities_data,
                             pending_count=pending_count,
                             approved_count=approved_count,
                             rejected_count=rejected_count)
    except Exception as e:
        print(f"Admin dashboard error: {e}")
        return render_template('admin_dashboard.html', error='Failed to load dashboard.')
    finally:
        close_database_connection(connection)


@app.route('/admin/review/<int:activity_id>', methods=['GET', 'POST'])
def admin_review(activity_id):
    """Review a specific activity."""
    if 'admin_id' not in session:
        return redirect(url_for('admin_login'))

    connection = get_db_connection()
    if not connection:
        return render_template('admin_review.html', error='Database connection failed.')

    if request.method == 'POST':
        action = request.form.get('action')
        points = request.form.get('points', 0)
        notes = request.form.get('notes', '').strip()

        try:
            points = int(points) if points else 0
        except ValueError:
            points = 0

        try:
            cursor = connection.cursor()

            if action == 'approve' and points > 0:
                # Update activity with admin points and approve
                cursor.execute(
                    """UPDATE activities
                       SET review_status = 'approved', admin_points = ?, review_notes = ?,
                           reviewed_by = ?, reviewed_at = ?, points_awarded = ?
                       WHERE id = ?""",
                    (points, notes, session['admin_id'], datetime.now(), points, activity_id)
                )
                # Add points to user's total
                cursor.execute(
                    "UPDATE users SET reward_points = reward_points + ? WHERE id = (SELECT user_id FROM activities WHERE id = ?)",
                    (points, activity_id)
                )
            elif action == 'reject':
                cursor.execute(
                    """UPDATE activities
                       SET review_status = 'rejected', review_notes = ?,
                           reviewed_by = ?, reviewed_at = ?
                       WHERE id = ?""",
                    (notes, session['admin_id'], datetime.now(), activity_id)
                )

            connection.commit()
            cursor.close()

            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            print(f"Admin review error: {e}")
            return render_template('admin_review.html', error='Failed to process review.')
        finally:
            close_database_connection(connection)

    # GET request - show activity details
    try:
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT a.*, u.username
            FROM activities a
            JOIN users u ON a.user_id = u.id
            WHERE a.id = ?
            """,
            (activity_id,)
        )
        activity = cursor.fetchone()
        cursor.close()

        if not activity:
            return render_template('admin_review.html', error='Activity not found.')

        activity_data = {
            'id': activity[0],
            'user_id': activity[1],
            'title': activity[2],
            'description': activity[3],
            'caption': activity[4],
            'file_path': activity[5],
            'proof_file_path': activity[6],
            'gps_lat': activity[7],
            'gps_lon': activity[8],
            'photo_timestamp': activity[9],
            'upload_source': activity[10],
            'device_info': activity[11],
            'created_at': activity[12],
            'points_awarded': activity[13],
            'review_status': activity[14],
            'admin_points': activity[15],
            'review_notes': activity[16],
            'reviewed_by': activity[17],
            'reviewed_at': activity[18],
            'username': activity[19]
        }

        return render_template('admin_review.html', activity=activity_data)
    except Exception as e:
        print(f"Admin review GET error: {e}")
        return render_template('admin_review.html', error='Failed to load activity.')
    finally:
        close_database_connection(connection)


@app.errorhandler(404)
def page_not_found(e):
    """Handle 404 errors."""
    return redirect(url_for('index'))


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors."""
    return f"An internal error occurred: {e}", 500


if __name__ == '__main__':
    app.run(debug=config.DEBUG, host=config.APP_HOST, port=config.APP_PORT)
