#!/usr/bin/env python3
"""
Emotion HR Server Launcher
Run this script to start the central Emotion HR server.
"""

import os
import sys
import subprocess
import platform
import socket

def get_local_ip():
    """Get the local IP address of this machine"""
    try:
        # Create a socket to get local IP
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Connect to Google DNS
        local_ip = s.getsockname()[0]
        s.close()
        return local_ip
    except:
        return "localhost"

def check_requirements():
    """Check if required packages are installed"""
    try:
        import flask
        import flask_socketio
        import cv2
        import ultralytics
        print("✅ All required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def check_models():
    """Check if required model files exist"""
    try:
        from config import YOLO_MODEL_PATH
        if os.path.exists(YOLO_MODEL_PATH):
            print("✅ YOLO model file found")
            return True
        else:
            print(f"⚠️  YOLO model not found at: {YOLO_MODEL_PATH}")
            print("Please download yolov8n-face.pt and update the path in config.py")
            return False
    except ImportError:
        print("⚠️  Could not check model path (config.py not found)")
        return False

def main():
    local_ip = get_local_ip()

    print("=" * 70)
    print("🖥️  EMOTION HR SERVER LAUNCHER")
    print("=" * 70)
    print(f"📍 Server will run on: http://0.0.0.0:5000")
    print(f"🌐 Local network IP: http://{local_ip}:5000")
    print("=" * 70)

    # Check requirements
    if not check_requirements():
        sys.exit(1)

    # Check models
    check_models()

    print("\n🚀 Starting Emotion HR Central Server...")
    print("📡 WebSocket server ready for distributed emotion monitoring")
    print("=" * 70)
    print("🌐 Client Connection URLs:")
    print(f"   Employee Client: http://{local_ip}:5000/employee")
    print(f"   HR Dashboard:    http://{local_ip}:5000/hr")
    print(f"   Landing Page:    http://{local_ip}:5000")
    print("=" * 70)
    print("📋 Instructions for Clients:")
    print(f"   1. Copy this IP address: {local_ip}")
    print("   2. On employee laptops: Open browser, enter server IP")
    print("   3. On HR laptop: Open browser, enter server IP")
    print("   4. Use same Room ID on all clients")
    print("=" * 70)
    print("⚠️  Network Notes:")
    print("   - Ensure port 5000 is open in firewall")
    print("   - All clients must be on same network")
    print("   - Press Ctrl+C to stop server")
    print("=" * 70)

    try:
        # Import and run server
        from server import socketio, app
        socketio.run(app, host='0.0.0.0', port=5000, debug=False)

    except KeyboardInterrupt:
        print("\n👋 Shutting down Emotion HR Server...")
        print("✅ Server stopped successfully!")

    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("💡 Check that:")
        print("   - Port 5000 is not in use")
        print("   - All dependencies are installed")
        print("   - Model files exist")
        sys.exit(1)

if __name__ == "__main__":
    main()