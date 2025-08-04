from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
import json
import os
from datetime import datetime, date
import hashlib
import logging
import cv2
import numpy as np
import base64
from PIL import Image
import io

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'  # Change this in production
CORS(app, supports_credentials=True)

# Data file paths
DATA_FILE = 'students.json'
USERS_FILE = 'users.json'
ATTENDANCE_FILE = 'attendance.json'
FACE_DATA_FILE = 'face_data.json'

# Default users (in production, use proper password hashing)
DEFAULT_USERS = {
    'principal': {
        'username': 'principal',
        'password': hashlib.sha256('principal123'.encode()).hexdigest(),
        'role': 'principal',
        'name': 'Principal'
    },
    'teacher1': {
        'username': 'teacher1',
        'password': hashlib.sha256('teacher123'.encode()).hexdigest(),
        'role': 'teacher',
        'name': 'Teacher 1'
    },
    'teacher2': {
        'username': 'teacher2',
        'password': hashlib.sha256('teacher123'.encode()).hexdigest(),
        'role': 'teacher',
        'name': 'Teacher 2'
    }
}

# Set up logging for CRUD operations
LOG_FILE = 'master.log'
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s'
)

# Load OpenCV face detection classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def load_students():
    """Load students from JSON file"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return []

def save_students(students):
    """Save students to JSON file"""
    with open(DATA_FILE, 'w') as f:
        json.dump(students, f, indent=2)

def load_users():
    """Load users from JSON file or create default users"""
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    else:
        # Create default users file
        save_users(DEFAULT_USERS)
        return DEFAULT_USERS

def save_users(users):
    """Save users to JSON file"""
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)

def load_attendance():
    """Load attendance data from JSON file"""
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_attendance(attendance):
    """Save attendance data to JSON file"""
    with open(ATTENDANCE_FILE, 'w') as f:
        json.dump(attendance, f, indent=2)

def load_face_data():
    """Load face data from JSON file"""
    if os.path.exists(FACE_DATA_FILE):
        with open(FACE_DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

def save_face_data(face_data):
    """Save face data to JSON file"""
    with open(FACE_DATA_FILE, 'w') as f:
        json.dump(face_data, f, indent=2)

def generate_roll_number():
    """Generate a unique roll number"""
    students = load_students()
    logging.info(f"Total students loaded: {len(students)}")
    
    if not students:
        logging.info("No students found, returning 2024001")
        return "2024001"
    
    # Get all existing roll numbers
    existing_rolls = []
    for student in students:
        try:
            if 'roll_number' in student and student['roll_number']:
                roll_num = int(student['roll_number'][3:])
                existing_rolls.append(roll_num)
                logging.info(f"Found roll number: {student['roll_number']} -> {roll_num}")
        except (ValueError, KeyError, IndexError) as e:
            logging.warning(f"Invalid roll number for student {student.get('name', 'Unknown')}: {e}")
            continue
    
    logging.info(f"All existing roll numbers: {existing_rolls}")
    
    if not existing_rolls:
        logging.info("No valid roll numbers found, returning 2024001")
        return "2024001"
    
    # Find the first gap or use the next number after the highest
    existing_rolls = sorted(existing_rolls)
    next_roll = 1
    for roll in existing_rolls:
        if roll == next_roll:
            next_roll += 1
        else:
            break
    
    logging.info(f"Sorted existing rolls: {existing_rolls}, Next roll: {next_roll}")
    
    # Ensure we don't exceed 999 students
    if next_roll > 999:
        raise ValueError("Maximum number of students (999) reached")
    
    result = f"2024{next_roll:03d}"
    logging.info(f"Final generated roll number: {result}")
    return result

def require_auth(f):
    """Decorator to require authentication"""
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def require_role(role):
    """Decorator to require specific role"""
    def decorator(f):
        def decorated_function(*args, **kwargs):
            if 'user' not in session:
                return jsonify({'error': 'Authentication required'}), 401
            if session['user']['role'] != role and session['user']['role'] != 'principal':
                return jsonify({'error': f'{role.capitalize()} role required'}), 403
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function
    return decorator

# Helper to log CRUD actions
def log_crud_action(action, user, details=None):
    msg = f"{action} by {user['username']} ({user['role']})"
    if details:
        msg += f" | {details}"
    logging.info(msg)

def calculate_age(dob_str):
    try:
        if not dob_str:
            return None
        dob = datetime.strptime(dob_str, '%Y-%m-%d')
        today = datetime.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age if age >= 0 else None
    except Exception as e:
        log_crud_action('ERROR', 'system', f'Failed to calculate age for DOB "{dob_str}": {str(e)}')
        return None

def resolve_username_to_name(username):
    """Convert username to display name"""
    users = load_users()
    user = users.get(username)
    if user:
        return user.get('name', username)
    return username

def get_student_by_roll_number(roll_number):
    """Get student by roll number"""
    students = load_students()
    return next((s for s in students if s['roll_number'] == roll_number), None)

def mark_attendance(student_id, status='present'):
    """Mark attendance for a student"""
    attendance = load_attendance()
    today = date.today().isoformat()
    
    if today not in attendance:
        attendance[today] = {}
    
    attendance[today][str(student_id)] = {
        'status': status,
        'timestamp': datetime.now().isoformat(),
        'method': 'face_recognition'
    }
    
    save_attendance(attendance)
    return attendance[today][str(student_id)]

def get_attendance_for_student(student_id, start_date=None, end_date=None):
    """Get attendance records for a specific student"""
    attendance = load_attendance()
    student_attendance = []
    
    for date_str, day_attendance in attendance.items():
        if str(student_id) in day_attendance:
            record = day_attendance[str(student_id)]
            record['date'] = date_str
            student_attendance.append(record)
    
    # Sort by date
    student_attendance.sort(key=lambda x: x['date'], reverse=True)
    return student_attendance

def detect_faces(image_array):
    """Detect faces in an image using OpenCV"""
    try:
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        return len(faces) > 0, len(faces)
    except Exception as e:
        return False, 0

def verify_face(image_data, student_roll_number):
    """Verify face using simple face detection"""
    try:
        # Decode base64 image
        image_bytes = base64.b64decode(image_data.split(',')[1])
        image = Image.open(io.BytesIO(image_bytes))
        image_array = np.array(image)
        
        # Convert RGB to BGR for OpenCV
        if len(image_array.shape) == 3:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
        
        # Load face data
        face_data = load_face_data()
        if student_roll_number not in face_data:
            return False, "No face data registered for this student. Please register your face first."
        
        # Check if face is detected
        face_detected, face_count = detect_faces(image_array)
        
        if not face_detected:
            return False, "No face detected in the image. Please position your face clearly in the camera."
        
        if face_count > 1:
            return False, "Multiple faces detected. Please ensure only one face is visible in the camera."
        
        # For this simplified version, we'll just verify that a face is detected
        # In a real implementation, you would compare face features
        return True, "Face verified successfully"
        
    except Exception as e:
        return False, f"Error during face verification: {str(e)}"

def register_face(image_data, student_roll_number):
    """Register face data for a student"""
    try:
        # Decode base64 image
        image_bytes = base64.b64decode(image_data.split(',')[1])
        image = Image.open(io.BytesIO(image_bytes))
        image_array = np.array(image)
        
        # Convert RGB to BGR for OpenCV
        if len(image_array.shape) == 3:
            image_array = cv2.cvtColor(image_array, cv2.COLOR_RGB2BGR)
        
        # Check if face is detected
        face_detected, face_count = detect_faces(image_array)
        
        if not face_detected:
            return False, "No face detected in the image. Please position your face clearly in the camera."
        
        if face_count > 1:
            return False, "Multiple faces detected. Please ensure only one face is visible in the camera."
        
        # Store face data (simplified - just store that face was detected)
        face_data = load_face_data()
        face_data[student_roll_number] = {
            'registered_at': datetime.now().isoformat(),
            'face_detected': True
        }
        
        save_face_data(face_data)
        return True, "Face registered successfully. Please login again to mark attendance."
        
    except Exception as e:
        return False, f"Error during face registration: {str(e)}"

def check_face_registered(student_roll_number):
    """Check if a student has registered their face"""
    face_data = load_face_data()
    return student_roll_number in face_data

@app.route('/')
def index():
    """Serve the main page"""
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Handle login"""
    if request.method == 'GET':
        if 'user' in session:
            return redirect(url_for('dashboard'))
        return render_template('login.html')
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    users = load_users()
    user = users.get(username)
    
    if not user or user['password'] != hashlib.sha256(password.encode()).hexdigest():
        return jsonify({'error': 'Invalid username or password'}), 401
    
    session['user'] = {
        'username': user['username'],
        'role': user['role'],
        'name': user['name']
    }
    
    return jsonify({
        'message': 'Login successful',
        'user': session['user']
    })

@app.route('/logout')
def logout():
    """Handle logout"""
    session.pop('user', None)
    return jsonify({'message': 'Logged out successfully'})

@app.route('/dashboard')
def dashboard():
    """Serve the dashboard based on user role"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if session['user']['role'] == 'principal':
        return render_template('principal_dashboard.html')
    elif session['user']['role'] == 'teacher':
        return render_template('teacher_dashboard.html')
    elif session['user']['role'] == 'student':
        return render_template('student_dashboard.html')
    else:
        return render_template('teacher_dashboard.html')

@app.route('/api/user')
def get_current_user():
    """Get current user information"""
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    return jsonify(session['user'])

@app.route('/api/students', methods=['GET'])
@require_auth
def get_students():
    """Get all students"""
    students = load_students()
    # Add dynamic age calculation and resolve usernames to names
    for s in students:
        s['age'] = calculate_age(s['dob']) if 'dob' in s else None
        # Resolve created_by username to name
        if 'created_by' in s:
            s['created_by'] = resolve_username_to_name(s['created_by'])
        # Resolve updated_by username to name
        if 'updated_by' in s:
            s['updated_by'] = resolve_username_to_name(s['updated_by'])
    return jsonify(students)

@app.route('/api/students', methods=['POST'])
@require_auth
def add_student():
    """Add a new student"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'dob', 'class']
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({'error': f'{field} is required'}), 400
    
    # Validate dob
    try:
        dob = datetime.strptime(data['dob'], '%Y-%m-%d')
    except ValueError:
        return jsonify({'error': 'DOB must be in YYYY-MM-DD format'}), 400
    
    students = load_students()
    
    # Check if name already exists
    if any(student['name'].lower() == data['name'].lower() for student in students):
        return jsonify({'error': 'Student with this name already exists'}), 400
    
    # Generate roll number
    try:
        roll_number = generate_roll_number()
        logging.info(f"Generated roll number: {roll_number}")
    except Exception as e:
        logging.error(f"Error generating roll number: {str(e)}")
        return jsonify({'error': 'Failed to generate roll number. Please try again.'}), 500
    
    # Create new student with proper ID generation
    new_id = 1
    if students:
        new_id = max(student['id'] for student in students) + 1
    
    # Debug session information
    logging.info(f"Session user: {session.get('user', 'No user in session')}")
    
    # Safely get user information from session
    user_name = session.get('user', {}).get('name', 'Unknown')
    user_role = session.get('user', {}).get('role', 'unknown')
    
    logging.info(f"Generated roll number: {roll_number} for new student: {data['name']}")
    
    new_student = {
        'id': new_id,
        'name': data['name'],
        'dob': data['dob'],
        'class': data['class'],
        'roll_number': roll_number,
        'created_at': datetime.now().isoformat(),
        'created_by': user_name,
        'created_by_role': user_role
    }
    
    students.append(new_student)
    save_students(students)
    log_crud_action('CREATE', session['user'], f"Student: {new_student['name']} (ID: {new_student['id']})")
    
    return jsonify(new_student), 201

@app.route('/api/students/<int:student_id>', methods=['GET'])
@require_auth
def get_student(student_id):
    """Get a specific student by ID"""
    students = load_students()
    student = next((s for s in students if s['id'] == student_id), None)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    # Add dynamic age calculation and resolve usernames to names
    if 'dob' in student:
        student['age'] = calculate_age(student['dob'])
    # Resolve created_by username to name
    if 'created_by' in student:
        student['created_by'] = resolve_username_to_name(student['created_by'])
    # Resolve updated_by username to name
    if 'updated_by' in student:
        student['updated_by'] = resolve_username_to_name(student['updated_by'])
    log_crud_action('READ', session['user'], f"Student: {student['name']} (ID: {student['id']})")
    
    return jsonify(student)

@app.route('/api/students/<int:student_id>', methods=['PUT'])
@require_auth
def update_student(student_id):
    """Update a student"""
    data = request.get_json()
    students = load_students()
    
    student = next((s for s in students if s['id'] == student_id), None)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    # Update fields
    if 'name' in data:
        # Check if name already exists for other students
        if any(s['name'].lower() == data['name'].lower() and s['id'] != student_id for s in students):
            return jsonify({'error': 'Student with this name already exists'}), 400
        student['name'] = data['name']
    
    if 'dob' in data:
        try:
            dob = datetime.strptime(data['dob'], '%Y-%m-%d')
            student['dob'] = data['dob']
        except ValueError:
            return jsonify({'error': 'DOB must be in YYYY-MM-DD format'}), 400
    
    if 'class' in data:
        student['class'] = data['class']
    
    # Track who edited the student
    student['updated_at'] = datetime.now().isoformat()
    student['updated_by'] = session['user']['name']
    student['updated_by_role'] = session['user']['role']
    
    save_students(students)
    log_crud_action('UPDATE', session['user'], f"Student: {student['name']} (ID: {student['id']})")
    
    return jsonify(student)

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
@require_role('principal')
def delete_student(student_id):
    """Delete a student and all associated data - only principals can delete"""
    students = load_students()
    student = next((s for s in students if s['id'] == student_id), None)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    # Remove the student from students list
    students = [s for s in students if s['id'] != student_id]
    save_students(students)
    
    # Remove all attendance records for this student
    attendance = load_attendance()
    for date in list(attendance.keys()):
        if str(student_id) in attendance[date]:
            del attendance[date][str(student_id)]
            # If no more records for this date, remove the entire date entry
            if not attendance[date]:
                del attendance[date]
    save_attendance(attendance)
    
    # Remove face registration data for this student
    face_data = load_face_data()
    if str(student_id) in face_data:
        del face_data[str(student_id)]
        save_face_data(face_data)
    
    log_crud_action('DELETE', session['user'], f"Student: {student['name']} (ID: {student['id']}) - Removed all attendance and face data")
    
    return jsonify({'message': 'Student and all associated data deleted successfully'})

@app.route('/api/students/search', methods=['GET'])
@require_auth
def search_students():
    """Search students by name or roll number"""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])
    
    students = load_students()
    filtered_students = [
        student for student in students
        if query in student['name'].lower() or query in student['roll_number'].lower()
    ]
    
    # Resolve usernames to names for search results
    for student in filtered_students:
        if 'created_by' in student:
            student['created_by'] = resolve_username_to_name(student['created_by'])
        if 'updated_by' in student:
            student['updated_by'] = resolve_username_to_name(student['updated_by'])
    
    return jsonify(filtered_students)

@app.route('/api/change_password', methods=['POST'])
@require_auth
def change_password():
    data = request.get_json()
    current_password = data.get('current_password')
    new_password = data.get('new_password')
    if not current_password or not new_password:
        return jsonify({'error': 'All fields are required'}), 400
    username = session['user']['username']
    users = load_users()
    user = users.get(username)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    # Only allow teachers (and optionally principal)
    if user['role'] not in ['teacher', 'principal']:
        return jsonify({'error': 'Not allowed'}), 403
    # Check current password
    if user['password'] != hashlib.sha256(current_password.encode()).hexdigest():
        return jsonify({'error': 'Current password is incorrect'}), 400
    # Validate new password (add more rules if needed)
    if len(new_password) < 6:
        return jsonify({'error': 'New password must be at least 6 characters'}), 400
    # Update password and history for teachers
    if user['role'] == 'teacher':
        if 'password_history' not in user:
            user['password_history'] = []
        user['password_history'].append({
            'password': user['password'],
            'changed_at': datetime.now().isoformat()
        })
    user['password'] = hashlib.sha256(new_password.encode()).hexdigest()
    users[username] = user
    save_users(users)
    return jsonify({'message': 'Password changed successfully'})

@app.route('/api/teachers', methods=['GET'])
@require_auth
def get_teachers():
    # Only principal can access
    if session['user']['role'] != 'principal':
        return jsonify({'error': 'Access denied'}), 403
    users = load_users()
    teachers = []
    for user in users.values():
        if user.get('role') == 'teacher':
            teachers.append({
                'username': user['username'],
                'name': user.get('name', ''),
                'password': user['password'],
                'password_history': user.get('password_history', [])
            })
    return jsonify(teachers)

@app.route('/api/teachers/<username>', methods=['PUT'])
@require_role('principal')
def update_teacher(username):
    """Update teacher information (name)"""
    data = request.get_json()
    new_name = data.get('name', '').strip()
    
    if not new_name:
        return jsonify({'error': 'Name is required'}), 400
    
    users = load_users()
    if username not in users:
        return jsonify({'error': 'Teacher not found'}), 404
    
    user = users[username]
    if user.get('role') != 'teacher':
        return jsonify({'error': 'User is not a teacher'}), 400
    
    old_name = user.get('name', '')
    user['name'] = new_name
    users[username] = user
    save_users(users)
    
    log_crud_action('UPDATE', session['user'], f"Teacher name changed: {old_name} → {new_name} (Username: {username})")
    
    return jsonify({
        'message': 'Teacher name updated successfully',
        'teacher': {
            'username': user['username'],
            'name': user['name'],
            'role': user['role']
        }
    })

@app.route('/teachers_list')
@require_auth
def teachers_list_page():
    if session['user']['role'] != 'principal':
        return jsonify({'error': 'Access denied'}), 403
    return render_template('teachers_list.html')

@app.route('/students_list')
@require_auth
def students_list_page():
    return render_template('students_list.html')

@app.route('/master_log')
@require_auth
def master_log():
    # Only principal can access
    if session['user']['role'] != 'principal':
        return jsonify({'error': 'Access denied'}), 403
    log_entries = []
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            log_entries = f.readlines()
    return render_template('master_log.html', logs=log_entries)

# Student Authentication Routes
@app.route('/student/login', methods=['POST'])
def student_login():
    """Handle student login with roll number"""
    data = request.get_json()
    roll_number = data.get('roll_number')
    
    if not roll_number:
        return jsonify({'error': 'Roll number is required'}), 400
    
    # Find student by roll number
    student = get_student_by_roll_number(roll_number)
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    # Create student session
    session['user'] = {
        'username': student['roll_number'],
        'role': 'student',
        'name': student['name'],
        'student_id': student['id']
    }
    
    return jsonify({
        'message': 'Login successful',
        'user': session['user']
    })

@app.route('/api/student/attendance', methods=['POST'])
@require_auth
def mark_student_attendance():
    """Mark attendance using face recognition"""
    if session['user']['role'] != 'student':
        return jsonify({'error': 'Only students can mark attendance'}), 403
    
    data = request.get_json()
    image_data = data.get('image')
    student_roll_number = session['user']['username']
    
    if not image_data:
        return jsonify({'error': 'Image data is required'}), 400
    
    # Verify face
    success, message = verify_face(image_data, student_roll_number)
    
    if not success:
        return jsonify({'error': message}), 400
    
    # Mark attendance
    student_id = session['user']['student_id']
    attendance_record = mark_attendance(student_id)
    
    log_crud_action('ATTENDANCE', session['user'], f"Student: {session['user']['name']} marked present")
    
    return jsonify({
        'message': 'Attendance marked successfully',
        'attendance': attendance_record
    })

@app.route('/api/student/register-face', methods=['POST'])
@require_auth
def register_student_face():
    """Register face data for a student"""
    if session['user']['role'] != 'student':
        return jsonify({'error': 'Only students can register face data'}), 403
    
    data = request.get_json()
    image_data = data.get('image')
    student_roll_number = session['user']['username']
    
    if not image_data:
        return jsonify({'error': 'Image data is required'}), 400
    
    # Register face
    success, message = register_face(image_data, student_roll_number)
    
    if not success:
        return jsonify({'error': message}), 400
    
    log_crud_action('FACE_REGISTRATION', session['user'], f"Student: {session['user']['name']} registered face")
    
    return jsonify({
        'message': message,
        'student_roll_number': student_roll_number
    })

@app.route('/api/student/face-status')
@require_auth
def get_student_face_status():
    """Check if student has registered their face"""
    if session['user']['role'] != 'student':
        return jsonify({'error': 'Only students can check face status'}), 403
    
    student_roll_number = session['user']['username']
    is_registered = check_face_registered(student_roll_number)
    
    return jsonify({
        'face_registered': is_registered,
        'student_roll_number': student_roll_number
    })

@app.route('/api/student/attendance-history')
@require_auth
def get_student_attendance_history():
    """Get attendance history for the logged-in student"""
    if session['user']['role'] != 'student':
        return jsonify({'error': 'Only students can view their attendance'}), 403
    
    student_id = session['user']['student_id']
    attendance_records = get_attendance_for_student(student_id)
    
    return jsonify({
        'student': {
            'name': session['user']['name'],
            'roll_number': session['user']['username']
        },
        'attendance': attendance_records
    })

@app.route('/api/students/<int:student_id>/attendance')
@require_role('teacher')
def get_student_attendance_by_teacher(student_id):
    """Get attendance for a specific student (teacher access)"""
    students = load_students()
    student = next((s for s in students if s['id'] == student_id), None)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    attendance_records = get_attendance_for_student(student_id)
    
    return jsonify({
        'student': student,
        'attendance': attendance_records
    })

@app.route('/api/attendance/class/<class_name>')
@require_role('teacher')
def get_class_attendance(class_name):
    """Get attendance for all students in a class"""
    students = load_students()
    class_students = [s for s in students if s['class'] == class_name]
    
    attendance = load_attendance()
    today = date.today().isoformat()
    
    class_attendance = []
    for student in class_students:
        student_attendance = {
            'student': student,
            'today_status': 'absent'
        }
        
        if today in attendance and str(student['id']) in attendance[today]:
            student_attendance['today_status'] = attendance[today][str(student['id'])]['status']
            student_attendance['timestamp'] = attendance[today][str(student['id'])]['timestamp']
        
        class_attendance.append(student_attendance)
    
    return jsonify({
        'class': class_name,
        'date': today,
        'attendance': class_attendance
    })

@app.route('/api/attendance/remove/<int:student_id>/<date>', methods=['DELETE'])
@require_role('principal')
def remove_attendance(student_id, date):
    """Remove attendance record for a specific student on a specific date"""
    try:
        attendance = load_attendance()
        
        if date not in attendance:
            return jsonify({'error': 'No attendance records found for this date'}), 404
        
        if str(student_id) not in attendance[date]:
            return jsonify({'error': 'No attendance record found for this student on this date'}), 404
        
        # Remove the attendance record
        del attendance[date][str(student_id)]
        
        # If no more records for this date, remove the entire date entry
        if not attendance[date]:
            del attendance[date]
        
        save_attendance(attendance)
        
        log_crud_action('ATTENDANCE_REMOVAL', session['user'], f"Removed attendance for student ID {student_id} on {date}")
        
        return jsonify({
            'message': 'Attendance record removed successfully',
            'student_id': student_id,
            'date': date
        })
        
    except Exception as e:
        return jsonify({'error': f'Error removing attendance: {str(e)}'}), 500

@app.route('/api/attendance/student/<int:student_id>')
@require_role('principal')
def get_student_attendance_for_principal(student_id):
    """Get all attendance records for a specific student (principal access)"""
    students = load_students()
    student = next((s for s in students if s['id'] == student_id), None)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    attendance_records = get_attendance_for_student(student_id)
    
    return jsonify({
        'student': student,
        'attendance': attendance_records
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 