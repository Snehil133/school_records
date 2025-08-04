# Student Information System - Backend

This is the backend API for the Student Information System built with Flask, featuring role-based authentication and access control.

## Features

- **🔐 Authentication System**: Session-based login with role-based access
- **👨‍💼 Principal Role**: Full CRUD operations (Add, Edit, Delete students)
- **👩‍🏫 Teacher Role**: Limited operations (Add, Edit students only)
- **📝 Edit History Tracking**: Track who created and modified student records
- **🔍 Search Functionality**: Search students by name or roll number
- **✅ Data Validation**: Comprehensive input validation
- **📊 JSON Storage**: File-based data storage with automatic creation

## Authentication

### User Roles
- **Principal**: Full administrative access
- **Teacher**: Limited access (no delete permissions)

### Default Users
| Username | Password | Role |
|----------|----------|------|
| principal | principal123 | Principal |
| teacher1 | teacher123 | Teacher |
| teacher2 | teacher123 | Teacher |

## Setup

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

The server will start on `http://localhost:5000`

## API Endpoints

### Authentication
- `GET /` - Login page (redirects to dashboard if authenticated)
- `POST /login` - User authentication
- `GET /logout` - User logout
- `GET /dashboard` - Role-based dashboard
- `GET /api/user` - Get current user information

### Students (All endpoints require authentication)
- `GET /api/students` - Get all students
- `POST /api/students` - Add a new student
- `GET /api/students/<id>` - Get a specific student
- `PUT /api/students/<id>` - Update a student
- `DELETE /api/students/<id>` - Delete a student (Principal only)
- `GET /api/students/search?q=<query>` - Search students

### Student Data Structure
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

## Security Features

- **Password Hashing**: SHA-256 hashing for all passwords
- **Session Management**: Flask session-based authentication
- **Role-based Access**: Decorators protect endpoints by role
- **Input Validation**: Server-side validation for all inputs
- **CORS Support**: Cross-origin resource sharing enabled

## Data Storage

- **Student Data**: `students.json` file
- **User Data**: `users.json` file (auto-created with default users)
- **Sessions**: Flask session storage (in-memory)

## Role-based Permissions

### Principal Access
- ✅ View all students
- ✅ Add new students
- ✅ Edit student information
- ✅ Delete students
- ✅ Search students
- ✅ View edit history

### Teacher Access
- ✅ View all students
- ✅ Add new students
- ✅ Edit student information
- ❌ Delete students (restricted)
- ✅ Search students
- ✅ View edit history

## Development

### Authentication Decorators
```python
@require_auth  # Requires any authenticated user
@require_role('principal')  # Requires principal role
```

### Adding New Users
Users are stored in `users.json`. To add a new user:

```python
import hashlib

new_user = {
    'username': 'newuser',
    'password': hashlib.sha256('password123'.encode()).hexdigest(),
    'role': 'teacher',  # or 'principal'
    'name': 'New User'
}
```

## Error Handling

The API returns appropriate HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request (validation errors)
- `401` - Unauthorized (authentication required)
- `403` - Forbidden (insufficient permissions)
- `404` - Not Found
- `500` - Internal Server Error

## File Structure

```
backend/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── static/                  # Static files (CSS, JS)
│   ├── login.css           # Login page styles
│   ├── dashboard.css       # Dashboard styles
│   ├── principal.js        # Principal dashboard logic
│   └── teacher.js          # Teacher dashboard logic
├── templates/              # HTML templates
│   ├── login.html         # Login page
│   ├── principal_dashboard.html  # Principal dashboard
│   └── teacher_dashboard.html    # Teacher dashboard
├── students.json          # Student data (auto-created)
├── users.json            # User data (auto-created)
└── README.md             # This file
``` 