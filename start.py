#!/usr/bin/env python3
"""
Student Information System Startup Script
This script helps you start both the backend and frontend servers.
"""

import os
import sys
import subprocess
import webbrowser
import time
import threading
from pathlib import Path

def check_python():
    """Check if Python is available"""
    try:
        subprocess.run([sys.executable, "--version"], check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False

def install_requirements():
    """Install backend requirements"""
    backend_dir = Path(__file__).parent / "backend"
    requirements_file = backend_dir / "requirements.txt"
    
    if not requirements_file.exists():
        print("❌ Requirements file not found!")
        return False
    
    print("📦 Installing backend requirements...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", str(requirements_file)
        ], check=True, cwd=backend_dir)
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def start_backend():
    """Start the Flask backend server"""
    backend_dir = Path(__file__).parent / "backend"
    app_file = backend_dir / "app.py"
    
    if not app_file.exists():
        print("❌ Backend app.py not found!")
        return False
    
    print("🚀 Starting backend server...")
    try:
        # Start the Flask server
        process = subprocess.Popen([
            sys.executable, str(app_file)
        ], cwd=backend_dir)
        
        # Wait a moment for server to start
        time.sleep(3)
        
        # Check if server is running
        try:
            import requests
            response = requests.get("http://localhost:5000", timeout=5)
            if response.status_code == 200:
                print("✅ Backend server is running on http://localhost:5000")
                return process
        except:
            print("⚠️  Backend server started but couldn't verify connection")
            return process
            
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False

def start_frontend():
    """Start the frontend server"""
    frontend_dir = Path(__file__).parent / "frontend"
    index_file = frontend_dir / "index.html"
    
    if not index_file.exists():
        print("❌ Frontend index.html not found!")
        return False
    
    print("🌐 Starting frontend server...")
    try:
        # Start a simple HTTP server
        process = subprocess.Popen([
            sys.executable, "-m", "http.server", "8000"
        ], cwd=frontend_dir)
        
        time.sleep(2)
        print("✅ Frontend server is running on http://localhost:8000")
        return process
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")
        return False

def open_browser():
    """Open the application in the browser"""
    print("🌍 Opening application in browser...")
    time.sleep(2)
    webbrowser.open("http://localhost:5000")

def main():
    """Main function"""
    print("🎓 Student Information System")
    print("=" * 40)
    
    # Check Python
    if not check_python():
        print("❌ Python is not available!")
        return
    
    # Install requirements
    if not install_requirements():
        print("❌ Failed to install requirements!")
        return
    
    # Start backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Failed to start backend!")
        return
    
    # Start frontend (optional, for legacy support)
    frontend_process = start_frontend()
    if not frontend_process:
        print("⚠️  Frontend server failed to start (optional)")
    
    # Open browser
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    print("\n🎉 Application is ready!")
    print("📱 Main Application: http://localhost:5000")
    if frontend_process:
        print("🌐 Legacy Frontend: http://localhost:8000 (redirects to main)")
    
    print("\n🔐 Login Credentials:")
    print("   Principal: username=principal, password=principal123")
    print("   Teacher: username=teacher1, password=teacher123")
    
    print("\nPress Ctrl+C to stop the servers...")
    
    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        backend_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print("✅ Servers stopped!")

if __name__ == "__main__":
    main() 