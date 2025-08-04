#!/usr/bin/env python3
"""
Startup script for the Face Recognition Attendance System
"""

import os
import sys
import webbrowser
import time
from threading import Timer

def open_browser():
    """Open the browser after a short delay"""
    webbrowser.open('http://localhost:5000')

def main():
    print("=" * 60)
    print("🎓 Face Recognition Attendance System")
    print("=" * 60)
    print()
    print("Starting the application...")
    print("The system will open in your browser automatically.")
    print()
    print("Demo Accounts:")
    print("  Staff:")
    print("    Principal: username=principal, password=principal123")
    print("    Teacher: username=teacher1, password=teacher123")
    print()
    print("  Students:")
    print("    Roll Numbers: 2024001, 2024002, 2024003, 2024004, 2024005")
    print("    (No password required for students)")
    print()
    print("Features:")
    print("  ✅ Student face registration")
    print("  ✅ Face recognition attendance marking")
    print("  ✅ Attendance history tracking")
    print("  ✅ Teacher and principal dashboards")
    print("  ✅ Real-time camera integration")
    print()
    print("Press Ctrl+C to stop the server")
    print("=" * 60)
    
    # Open browser after 3 seconds
    Timer(3, open_browser).start()
    
    # Import and run the Flask app
    from app import app
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
        print("Thank you for using the Face Recognition Attendance System!")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("Please check that all dependencies are installed:")
        print("pip install -r requirements.txt")
        sys.exit(1) 