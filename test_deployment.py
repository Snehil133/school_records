#!/usr/bin/env python3
"""
Simple test script to verify deployment configuration
"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from app_vercel import app
    print("✅ Successfully imported Flask app")
    
    # Test basic app configuration
    print(f"✅ App name: {app.name}")
    print(f"✅ App secret key configured: {'secret_key' in app.config}")
    
    # Test data loading functions
    from app_vercel import load_users, load_students, load_attendance
    
    users = load_users()
    print(f"✅ Users loaded: {len(users)} users found")
    
    students = load_students()
    print(f"✅ Students loaded: {len(students)} students found")
    
    attendance = load_attendance()
    print(f"✅ Attendance loaded: {len(attendance)} attendance records found")
    
    print("\n🎉 All tests passed! Deployment should work.")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    sys.exit(1) 