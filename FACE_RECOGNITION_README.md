# Face Recognition Attendance System

This system allows students to mark their attendance using face recognition technology. The system includes a student dashboard with face registration and attendance marking capabilities.

## Features

### For Students:
- **Face Registration**: Students can register their face for attendance marking
- **Face Recognition Attendance**: Mark attendance using face recognition
- **Attendance History**: View their attendance records
- **Real-time Camera**: Live camera feed for face capture

### For Teachers:
- **View Student Attendance**: Check attendance for individual students
- **Class Attendance**: View attendance for entire classes
- **Student Management**: Add, edit, and manage student records

### For Principals:
- **Full System Access**: Access to all features
- **System Logs**: View all system activities
- **Teacher Management**: Manage teacher accounts

## How to Use

### 1. Installation

1. Install the required dependencies:
```bash
cd backend
pip install -r requirements.txt
```

2. Start the application:
```bash
python app.py
```

3. Open your browser and navigate to `http://localhost:5000`

### 2. Student Login

1. On the login page, click the "Student Login" tab
2. Enter your roll number (e.g., 2024001, 2024002, etc.)
3. Click "Student Login"

### 3. Face Registration (First Time Only)

1. After logging in, you'll see the student dashboard
2. In the "Register Face" section, click "Register Face"
3. Position your face clearly in the camera view
4. The system will capture and store your face data

### 4. Marking Attendance

1. In the "Face Recognition Attendance" section, click "Mark Attendance"
2. Position your face in the camera view
3. The system will verify your face and mark your attendance
4. You'll see a success message if attendance is marked successfully

### 5. View Attendance History

- Your attendance history is displayed at the bottom of the dashboard
- Shows all your attendance records with dates and times

## Demo Accounts

### Staff Accounts:
- **Principal**: username: `principal`, password: `principal123`
- **Teacher**: username: `teacher1`, password: `teacher123`

### Student Accounts:
- **Roll Numbers**: 2024001, 2024002, 2024003, 2024004, 2024005
- **No password required** - just enter the roll number

## Technical Details

### Face Recognition Technology:
- Uses OpenCV for image processing
- Face detection and encoding using face_recognition library
- Stores face encodings securely in JSON format
- Tolerance level: 0.6 (adjustable for accuracy vs. flexibility)

### Security Features:
- Face data is stored locally and securely
- Session-based authentication
- Role-based access control
- Comprehensive logging of all activities

### Data Storage:
- Students: `students.json`
- Users: `users.json`
- Attendance: `attendance.json`
- Face Data: `face_data.json`
- System Logs: `master.log`

## Troubleshooting

### Camera Issues:
- Ensure camera permissions are granted in your browser
- Try refreshing the page if camera doesn't load
- Check that your camera is not being used by another application

### Face Recognition Issues:
- Ensure good lighting for face capture
- Position your face clearly in the camera view
- Try registering your face again if recognition fails
- Make sure you're looking directly at the camera

### Login Issues:
- Verify you're using the correct roll number
- Check that the student exists in the system
- Try logging out and logging back in

## Browser Compatibility

The system works best with:
- Chrome (recommended)
- Firefox
- Safari
- Edge

## Privacy and Security

- Face data is stored locally on the server
- No face images are stored, only mathematical encodings
- All data is encrypted and secure
- Session data is cleared on logout

## Support

For technical support or questions, please contact the system administrator.

## Future Enhancements

- Multiple face registration per student
- Attendance analytics and reports
- Mobile app version
- Integration with school management systems
- Real-time attendance notifications 