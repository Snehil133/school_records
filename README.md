# Student Information System with Face Recognition Attendance

A modern, full-stack student information system built with Python Flask backend and vanilla HTML/CSS/JavaScript frontend, featuring role-based authentication, access control, and **face recognition attendance marking**.

## Features

- **🔐 Role-Based Authentication**: Login system with Principal, Teacher, and Student roles
- **👨‍💼 Principal Access**: Full CRUD operations (Add, Edit, Delete students)
- **👩‍🏫 Teacher Access**: Limited operations (Add, Edit students only)
- **👨‍🎓 Student Access**: Face recognition attendance marking
- **📸 Face Recognition**: Students can register their face and mark attendance
- **📝 Edit History Tracking**: See who created and last edited each student
- **🔍 Search Functionality**: Search students by name or roll number
- **📱 Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **⚡ Real-time Updates**: Instant UI updates without page refresh
- **✅ Data Validation**: Server-side validation for all inputs
- **🎨 Modern UI**: Beautiful gradient design with smooth animations
- **📊 Attendance Tracking**: Complete attendance history and reporting

## User Roles & Permissions

### Principal
- ✅ Add new students
- ✅ Edit student information
- ✅ Delete students
- ✅ View all students
- ✅ Search students
- ✅ View edit history
- ✅ View attendance reports
- ✅ Manage teachers

### Teacher
- ✅ Add new students
- ✅ Edit student information
- ❌ Delete students (restricted)
- ✅ View all students
- ✅ Search students
- ✅ View edit history
- ✅ View student attendance
- ✅ View class attendance

### Student
- ✅ Login with roll number
- ✅ Register face for attendance
- ✅ Mark attendance using face recognition
- ✅ View personal attendance history

## Demo Accounts

| Role | Username/ID | Password |
|------|-------------|----------|
| Principal | `principal` | `principal123` |
| Teacher | `teacher1` | `teacher123` |
| Teacher | `teacher2` | `teacher123` |
| Student | `2024001` | No password |
| Student | `2024002` | No password |
| Student | `2024003` | No password |
| Student | `2024004` | No password |
| Student | `2024005` | No password |

## Project Structure

```
student_system/
├── backend/
│   ├── app.py                    # Flask backend server with auth
│   ├── requirements.txt          # Python dependencies
│   ├── start_face_recognition.py # Face recognition startup script
│   ├── static/
│   │   ├── login.css            # Login page styles
│   │   ├── dashboard.css        # Dashboard styles
│   │   ├── principal.js         # Principal dashboard logic
│   │   └── teacher.js           # Teacher dashboard logic
│   ├── templates/
│   │   ├── login.html           # Login page
│   │   ├── principal_dashboard.html  # Principal dashboard
│   │   ├── teacher_dashboard.html    # Teacher dashboard
│   │   └── student_dashboard.html    # Student dashboard
│   ├── students.json            # Student data
│   ├── users.json               # User data
│   ├── attendance.json          # Attendance data
│   ├── face_data.json          # Face recognition data
│   └── master.log               # System logs
├── frontend/                    # Legacy frontend (deprecated)
├── start.py                     # Python startup script
├── start.bat                    # Windows batch startup script
├── FACE_RECOGNITION_README.md   # Face recognition documentation
└── README.md                    # This file
```

## Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)
- Webcam (for face recognition features)

### Easy Setup (Recommended)

1. Navigate to the project directory:
```bash
cd student_system
```

2. Run the face recognition startup script:
```bash
cd backend
python start_face_recognition.py
```

The application will automatically:
- Install dependencies
- Start the backend server
- Open your browser to the login page

### Alternative Setup

1. Navigate to the backend directory:
```bash
cd student_system/backend
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Start the application:
```bash
python app.py
```

4. Open your browser and go to `http://localhost:5000`

### Manual Setup

1. **Backend Setup**:
```bash
cd student_system/backend
pip install -r requirements.txt
python app.py
```

2. **Access the Application**:
- Open your browser and go to `http://localhost:5000`
- Login with one of the demo accounts above

## API Endpoints

| Method | Endpoint | Description | Access |
|--------|----------|-------------|--------|
| GET | `/` | Login page | Public |
| POST | `/login` | User authentication | Public |
| POST | `/student/login` | Student authentication | Public |
| GET | `/logout` | User logout | Authenticated |
| GET | `/dashboard` | Role-based dashboard | Authenticated |
| GET | `/api/user` | Get current user info | Authenticated |
| GET | `/api/students` | Get all students | Authenticated |
| POST | `/api/students` | Add new student | Authenticated |
| GET | `/api/students/<id>` | Get specific student | Authenticated |
| PUT | `/api/students/<id>` | Update student | Authenticated |
| DELETE | `/api/students/<id>` | Delete student | Principal only |
| GET | `/api/students/search?q=<query>` | Search students | Authenticated |
| POST | `/api/student/attendance` | Mark attendance with face | Student only |
| POST | `/api/student/register-face` | Register face data | Student only |
| GET | `/api/student/attendance-history` | Get student attendance | Student only |
| GET | `/api/students/<id>/attendance` | Get student attendance | Teacher/Principal |
| GET | `/api/attendance/class/<class>` | Get class attendance | Teacher/Principal |

## Student Data Structure

```json
{
  "id": 1,
  "name": "John Doe",
  "age": 20,
  "class": "Computer Science",
  "roll_number": "2024001",
  "created_at": "2024-01-01T00:00:00",
  "created_by": "principal",
  "created_by_role": "principal",
  "updated_at": "2024-01-02T00:00:00",
  "updated_by": "teacher1",
  "updated_by_role": "teacher"
}
```

## Features in Detail

### Face Recognition System
- **OpenCV-based face detection** for reliable face recognition
- **Real-time camera integration** with live video feed
- **Face registration system** for students to register their faces
- **Attendance marking** using face verification
- **Attendance history tracking** with timestamps
- **Multiple face detection** prevention for security
- **Cross-browser compatibility** for camera access

### Authentication System
- **Session-based authentication** with Flask sessions
- **Role-based access control** with decorators
- **Password hashing** using SHA-256
- **Student roll number authentication** (no password required)
- **Automatic redirect** to login for unauthenticated users

### Backend Features
- **Flask REST API** with authentication middleware
- **CORS Support** for cross-origin requests
- **Data Validation** with comprehensive error handling
- **JSON Storage** with automatic file creation
- **Edit History Tracking** for audit trails
- **Role-based Permissions** with decorators

### Frontend Features
- **Role-specific Dashboards** with different UI elements
- **Modern UI** with gradient designs and animations
- **Real-time Search** with instant results
- **Modal Dialogs** for edit operations
- **Form Validation** with client-side checks
- **Loading States** and notifications
- **Responsive Design** for all devices

## Usage Guide

### For Students
1. **Login** with your roll number (e.g., 2024001)
2. **Register Face** (first time only):
   - Click "Register Face" in the right panel
   - Position your face clearly in the camera
   - Click "Register Face" to save your face data
3. **Mark Attendance**:
   - Click "Mark Attendance" in the left panel
   - Position your face in the camera
   - The system will verify your face and mark attendance
4. **View History**: Your attendance history is displayed at the bottom

### For Principals
1. **Login** with principal credentials
2. **Add Students** using the form on the left
3. **Search Students** using the search box
4. **Edit Students** by clicking the "Edit" button
5. **Delete Students** by clicking the "Delete" button (with confirmation)
6. **View Edit History** to see who made changes
7. **View Attendance Reports** for all students

### For Teachers
1. **Login** with teacher credentials
2. **Add Students** using the form on the left
3. **Search Students** using the search box
4. **Edit Students** by clicking the "Edit" button
5. **View Edit History** to see who made changes
6. **View Student Attendance** for individual students
7. **View Class Attendance** for entire classes
8. **Note**: Delete functionality is not available

## Data Storage

- **Student Data**: Stored in `students.json` file
- **User Data**: Stored in `users.json` file
- **Sessions**: Stored in Flask session (in-memory)

## Security Features

- **Password Hashing**: All passwords are hashed using SHA-256
- **Session Management**: Secure session handling
- **Role-based Access**: API endpoints protected by role decorators
- **Input Validation**: Server-side validation for all inputs
- **CSRF Protection**: Built-in Flask CSRF protection

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 12+
- Edge 79+

## Development

### Backend Development
- Flask app with debug mode for development
- CORS enabled for frontend communication
- Session-based authentication
- Role-based middleware

### Frontend Development
- Vanilla JavaScript with ES6+ features
- CSS Grid and Flexbox for responsive layout
- Font Awesome icons for better UX
- No external frameworks (except Font Awesome)

## Troubleshooting

### General Issues
1. **Login Issues**: Check if the backend is running on port 5000
2. **Permission Errors**: Ensure you're logged in with the correct role
3. **Data Not Saving**: Check file permissions in the backend directory
4. **CORS Errors**: Verify the backend CORS settings
5. **Session Issues**: Clear browser cookies and try again

### Face Recognition Issues
1. **Camera Not Working**: 
   - Ensure camera permissions are granted in your browser
   - Try refreshing the page
   - Check that your camera is not being used by another application
2. **Face Not Detected**:
   - Ensure good lighting
   - Position your face clearly in the camera view
   - Make sure you're looking directly at the camera
3. **Multiple Faces Detected**:
   - Ensure only one face is visible in the camera
   - Move away from other people
4. **Face Registration Fails**:
   - Try registering your face again
   - Ensure your face is clearly visible and well-lit
5. **Attendance Marking Fails**:
   - Make sure you've registered your face first
   - Try marking attendance again
   - Check that your face is clearly visible

## License

This project is open source and available under the MIT License. 