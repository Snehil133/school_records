#!/usr/bin/env python3
"""
Test script to verify face recognition dependencies are working
"""

import sys
import os

def test_imports():
    """Test if all required libraries can be imported"""
    try:
        import cv2
        print("✅ OpenCV imported successfully")
    except ImportError as e:
        print(f"❌ OpenCV import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ NumPy imported successfully")
    except ImportError as e:
        print(f"❌ NumPy import failed: {e}")
        return False
    
    try:
        import face_recognition
        print("✅ Face Recognition imported successfully")
    except ImportError as e:
        print(f"❌ Face Recognition import failed: {e}")
        return False
    
    try:
        from PIL import Image
        print("✅ Pillow imported successfully")
    except ImportError as e:
        print(f"❌ Pillow import failed: {e}")
        return False
    
    return True

def test_face_recognition_basic():
    """Test basic face recognition functionality"""
    try:
        import face_recognition
        import numpy as np
        
        # Create a simple test image (1x1 pixel)
        test_image = np.zeros((100, 100, 3), dtype=np.uint8)
        
        # Try to find faces (should return empty list)
        face_locations = face_recognition.face_locations(test_image)
        print("✅ Face recognition basic functionality works")
        return True
        
    except Exception as e:
        print(f"❌ Face recognition test failed: {e}")
        return False

def main():
    print("Testing Face Recognition Dependencies...")
    print("=" * 40)
    
    # Test imports
    if not test_imports():
        print("\n❌ Some imports failed. Please install missing dependencies:")
        print("pip install opencv-python face-recognition Pillow numpy")
        return False
    
    # Test basic functionality
    if not test_face_recognition_basic():
        print("\n❌ Face recognition functionality test failed.")
        return False
    
    print("\n✅ All tests passed! Face recognition system is ready to use.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 