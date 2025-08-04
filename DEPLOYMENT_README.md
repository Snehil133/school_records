# Student System - Vercel Deployment Guide

## Overview
This guide will help you deploy your Student Management System to Vercel. The deployment has been optimized for Vercel's serverless environment.

## Important Notes
- **Face Recognition**: OpenCV has been removed for Vercel compatibility. Face recognition features are simplified and will work with basic image validation.
- **Data Storage**: Data is stored in JSON files. For production, consider using a database service.
- **File System**: Vercel has read-only file system, so data persistence may be limited.

## Pre-deployment Changes Made

### 1. Requirements Updated
- Removed `opencv-python` dependency
- Added `gunicorn` for production server
- Kept essential Flask dependencies

### 2. Code Modifications
- Simplified face detection functions
- Removed OpenCV dependencies
- Added Vercel configuration

## Deployment Steps

### Step 1: Install Vercel CLI
```bash
npm install -g vercel
```

### Step 2: Login to Vercel
```bash
vercel login
```

### Step 3: Deploy to Vercel
```bash
vercel
```

### Step 4: Follow the Prompts
- Choose to link to existing project or create new
- Set project name (e.g., "student-system")
- Choose default settings

### Step 5: Access Your Deployed App
After deployment, Vercel will provide you with:
- Production URL (e.g., `https://your-app.vercel.app`)
- Preview URL for testing

## Configuration Files

### vercel.json
```json
{
  "version": 2,
  "builds": [
    {
      "src": "backend/app.py",
      "use": "@vercel/python",
      "config": {
        "requirements": "backend/requirements-vercel.txt"
      }
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "backend/app.py"
    }
  ]
}
```

### backend/requirements-vercel.txt
```
Flask==2.3.3
Flask-CORS==4.0.0
Pillow==10.0.1
numpy==1.24.3
gunicorn==21.2.0
```

## Default Login Credentials

### Principal
- Username: `principal`
- Password: `principal123`

### Teachers
- Username: `teacher1` or `teacher2`
- Password: `teacher123`

## Features Available After Deployment

### ✅ Working Features
- User authentication (Principal, Teachers, Students)
- Student management (CRUD operations)
- Attendance tracking
- Teacher management
- Dashboard for different user roles
- Search functionality
- Password change functionality

### ⚠️ Simplified Features
- Face recognition (simplified for Vercel)
- Image upload (basic validation only)

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Ensure all dependencies are in `requirements-vercel.txt`
   - Check that `vercel.json` is in the root directory

2. **Import Errors**
   - Make sure OpenCV imports are removed
   - Check that all imports are available in requirements

3. **File System Errors**
   - Vercel has read-only file system
   - Data persistence may be limited

### Environment Variables
If you need to add environment variables:
1. Go to your Vercel dashboard
2. Select your project
3. Go to Settings > Environment Variables
4. Add any required variables

## Post-Deployment

### 1. Test the Application
- Visit your deployed URL
- Test login with default credentials
- Verify all features work as expected

### 2. Custom Domain (Optional)
- Go to Vercel dashboard
- Add custom domain in project settings

### 3. Monitor Performance
- Use Vercel analytics to monitor usage
- Check function execution logs

## Security Considerations

### For Production Use
1. **Change Default Passwords**
   - Update default user passwords
   - Use environment variables for secrets

2. **Add HTTPS**
   - Vercel provides HTTPS by default

3. **Database Migration**
   - Consider migrating to a proper database
   - Use services like MongoDB Atlas or PostgreSQL

## Support
If you encounter issues:
1. Check Vercel function logs
2. Verify all files are committed to GitHub
3. Ensure `vercel.json` is in the root directory

## Next Steps
After successful deployment:
1. Test all functionality
2. Update documentation
3. Consider adding monitoring
4. Plan for database migration if needed 