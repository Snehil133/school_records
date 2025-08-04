from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from flask_cors import CORS
import json
import os
from datetime import datetime, date
import hashlib
import logging
from PIL import Image
import io

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-in-production'  # Change this in production
CORS(app, supports_credentials=True)

# Data file paths
DATA_FILE = 'students.json'
USERS_FILE = 'users.json'
ATTENDANCE_FILE = 'attendance.json'

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

def generate_roll_number():
    """Generate a unique roll number"""
    students = load_students()
    if not students:
        return "STU001"
    
    # Find the highest roll number
    max_roll = max(int(s['roll_number'].replace('STU', '')) for s in students if s['roll_number'].startswith('STU'))
    new_roll = f"STU{str(max_roll + 1).zfill(3)}"
    return new_roll

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
            
            users = load_users()
            user = users.get(session['user'])
            if not user or user['role'] != role:
                return jsonify({'error': 'Insufficient permissions'}), 403
            
            return f(*args, **kwargs)
        decorated_function.__name__ = f.__name__
        return decorated_function
    return decorator

def log_crud_action(action, user, details=None):
    """Log CRUD actions"""
    log_message = f"USER: {user} | ACTION: {action}"
    if details:
        log_message += f" | DETAILS: {details}"
    logging.info(log_message)

def calculate_age(dob_str):
    """Calculate age from date of birth"""
    try:
        dob = datetime.strptime(dob_str, '%Y-%m-%d').date()
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        return age
    except:
        return None

def resolve_username_to_name(username):
    """Resolve username to display name"""
    users = load_users()
    user = users.get(username)
    return user['name'] if user else username

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
        'timestamp': datetime.now().isoformat()
    }
    
    save_attendance(attendance)

def get_attendance_for_student(student_id, start_date=None, end_date=None):
    """Get attendance records for a student"""
    attendance = load_attendance()
    student_records = []
    
    for date_str, records in attendance.items():
        if str(student_id) in records:
            student_records.append({
                'date': date_str,
                'status': records[str(student_id)]['status'],
                'timestamp': records[str(student_id)]['timestamp']
            })
    
    return sorted(student_records, key=lambda x: x['date'], reverse=True)

@app.route('/')
def index():
    """Home page"""
    if 'user' in session:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login endpoint"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        users = load_users()
        user = users.get(username)
        
        if user and user['password'] == hashlib.sha256(password.encode()).hexdigest():
            session['user'] = username
            session['role'] = user['role']
            session['name'] = user['name']
            return jsonify({'success': True, 'role': user['role']})
        else:
            return jsonify({'error': 'Invalid credentials'}), 401
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Logout endpoint"""
    session.clear()
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    """Dashboard page"""
    if 'user' not in session:
        return redirect(url_for('login'))
    
    role = session['role']
    if role == 'principal':
        return render_template('principal_dashboard.html')
    elif role == 'teacher':
        return render_template('teacher_dashboard.html')
    else:
        return render_template('student_dashboard.html')

@app.route('/api/user')
def get_current_user():
    """Get current user info"""
    if 'user' not in session:
        return jsonify({'error': 'Not authenticated'}), 401
    
    return jsonify({
        'username': session['user'],
        'role': session['role'],
        'name': session['name']
    })

@app.route('/api/students', methods=['GET'])
@require_auth
def get_students():
    """Get all students"""
    students = load_students()
    return jsonify(students)

@app.route('/api/students', methods=['POST'])
@require_auth
def add_student():
    """Add a new student"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'class', 'dob', 'parent_name', 'phone']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        students = load_students()
        
        # Generate unique ID and roll number
        new_id = max([s['id'] for s in students], default=0) + 1
        roll_number = generate_roll_number()
        
        # Calculate age
        age = calculate_age(data['dob'])
        
        new_student = {
            'id': new_id,
            'roll_number': roll_number,
            'name': data['name'],
            'class': data['class'],
            'dob': data['dob'],
            'age': age,
            'parent_name': data['parent_name'],
            'phone': data['phone'],
            'address': data.get('address', ''),
            'created_at': datetime.now().isoformat()
        }
        
        students.append(new_student)
        save_students(students)
        
        log_crud_action('STUDENT_CREATE', session['user'], f"Created student: {new_student['name']} (ID: {new_id})")
        
        return jsonify(new_student), 201
        
    except Exception as e:
        return jsonify({'error': f'Error creating student: {str(e)}'}), 500

@app.route('/api/students/<int:student_id>', methods=['GET'])
@require_auth
def get_student(student_id):
    """Get a specific student"""
    students = load_students()
    student = next((s for s in students if s['id'] == student_id), None)
    
    if not student:
        return jsonify({'error': 'Student not found'}), 404
    
    return jsonify(student)

@app.route('/api/students/<int:student_id>', methods=['PUT'])
@require_auth
def update_student(student_id):
    """Update a student"""
    try:
        data = request.get_json()
        students = load_students()
        
        student_index = next((i for i, s in enumerate(students) if s['id'] == student_id), None)
        if student_index is None:
            return jsonify({'error': 'Student not found'}), 404
        
        # Update fields
        for field in ['name', 'class', 'dob', 'parent_name', 'phone', 'address']:
            if field in data:
                students[student_index][field] = data[field]
        
        # Recalculate age if DOB changed
        if 'dob' in data:
            students[student_index]['age'] = calculate_age(data['dob'])
        
        save_students(students)
        
        log_crud_action('STUDENT_UPDATE', session['user'], f"Updated student ID {student_id}")
        
        return jsonify(students[student_index])
        
    except Exception as e:
        return jsonify({'error': f'Error updating student: {str(e)}'}), 500

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
@require_role('principal')
def delete_student(student_id):
    """Delete a student"""
    try:
        students = load_students()
        student = next((s for s in students if s['id'] == student_id), None)
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        students = [s for s in students if s['id'] != student_id]
        save_students(students)
        
        log_crud_action('STUDENT_DELETE', session['user'], f"Deleted student: {student['name']} (ID: {student_id})")
        
        return jsonify({'message': 'Student deleted successfully'})
        
    except Exception as e:
        return jsonify({'error': f'Error deleting student: {str(e)}'}), 500

@app.route('/api/students/search', methods=['GET'])
@require_auth
def search_students():
    """Search students"""
    query = request.args.get('q', '').lower()
    students = load_students()
    
    if not query:
        return jsonify(students)
    
    filtered_students = [
        s for s in students
        if query in s['name'].lower() or 
           query in s['roll_number'].lower() or
           query in s['class'].lower()
    ]
    
    return jsonify(filtered_students)

@app.route('/api/change_password', methods=['POST'])
@require_auth
def change_password():
    """Change user password"""
    try:
        data = request.get_json()
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return jsonify({'error': 'Both current and new password are required'}), 400
        
        users = load_users()
        user = users.get(session['user'])
        
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        # Verify current password
        if user['password'] != hashlib.sha256(current_password.encode()).hexdigest():
            return jsonify({'error': 'Current password is incorrect'}), 401
        
        # Update password
        user['password'] = hashlib.sha256(new_password.encode()).hexdigest()
        save_users(users)
        
        log_crud_action('PASSWORD_CHANGE', session['user'], 'Password changed successfully')
        
        return jsonify({'message': 'Password changed successfully'})
        
    except Exception as e:
        return jsonify({'error': f'Error changing password: {str(e)}'}), 500

@app.route('/api/teachers', methods=['GET'])
@require_auth
def get_teachers():
    """Get all teachers (principal only)"""
    if session['role'] != 'principal':
        return jsonify({'error': 'Access denied'}), 403
    
    users = load_users()
    teachers = [user for user in users.values() if user['role'] == 'teacher']
    return jsonify(teachers)

@app.route('/api/teachers/<username>', methods=['PUT'])
@require_role('principal')
def update_teacher(username):
    """Update teacher information"""
    try:
        data = request.get_json()
        users = load_users()
        
        if username not in users:
            return jsonify({'error': 'Teacher not found'}), 404
        
        if users[username]['role'] != 'teacher':
            return jsonify({'error': 'User is not a teacher'}), 400
        
        # Update allowed fields
        if 'name' in data:
            users[username]['name'] = data['name']
        
        if 'password' in data:
            users[username]['password'] = hashlib.sha256(data['password'].encode()).hexdigest()
        
        save_users(users)
        
        log_crud_action('TEACHER_UPDATE', session['user'], f"Updated teacher: {username}")
        
        return jsonify(users[username])
        
    except Exception as e:
        return jsonify({'error': f'Error updating teacher: {str(e)}'}), 500

@app.route('/teachers_list')
@require_auth
def teachers_list_page():
    """Teachers list page"""
    if session['role'] != 'principal':
        return redirect(url_for('dashboard'))
    return render_template('teachers_list.html')

@app.route('/students_list')
@require_auth
def students_list_page():
    """Students list page"""
    return render_template('students_list.html')

@app.route('/master_log')
@require_auth
def master_log():
    """Master log page (principal only)"""
    if session['role'] != 'principal':
        return redirect(url_for('dashboard'))
    return render_template('master_log.html')

@app.route('/student/login', methods=['POST'])
def student_login():
    """Student login endpoint"""
    try:
        data = request.get_json()
        roll_number = data.get('roll_number')
        
        if not roll_number:
            return jsonify({'error': 'Roll number is required'}), 400
        
        students = load_students()
        student = get_student_by_roll_number(roll_number)
        
        if not student:
            return jsonify({'error': 'Student not found'}), 404
        
        # For student login, we'll use the roll number as the session identifier
        session['user'] = f"student_{roll_number}"
        session['role'] = 'student'
        session['name'] = student['name']
        session['student_id'] = student['id']
        
        return jsonify({
            'success': True,
            'student': student
        })
        
    except Exception as e:
        return jsonify({'error': f'Login error: {str(e)}'}), 500

@app.route('/api/student/attendance', methods=['POST'])
@require_auth
def mark_student_attendance():
    """Mark attendance for current student"""
    try:
        if session['role'] != 'student':
            return jsonify({'error': 'Only students can mark their own attendance'}), 403
        
        student_id = session.get('student_id')
        if not student_id:
            return jsonify({'error': 'Student ID not found'}), 400
        
        mark_attendance(student_id, 'present')
        
        log_crud_action('STUDENT_ATTENDANCE', session['user'], f"Marked attendance for student ID {student_id}")
        
        return jsonify({
            'message': 'Attendance marked successfully',
            'student_id': student_id,
            'date': date.today().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': f'Error marking attendance: {str(e)}'}), 500

@app.route('/api/student/attendance-history')
@require_auth
def get_student_attendance_history():
    """Get attendance history for current student"""
    try:
        if session['role'] != 'student':
            return jsonify({'error': 'Only students can view their attendance history'}), 403
        
        student_id = session.get('student_id')
        if not student_id:
            return jsonify({'error': 'Student ID not found'}), 400
        
        attendance_records = get_attendance_for_student(student_id)
        
        return jsonify({
            'student_id': student_id,
            'attendance': attendance_records
        })
        
    except Exception as e:
        return jsonify({'error': f'Error getting attendance history: {str(e)}'}), 500

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