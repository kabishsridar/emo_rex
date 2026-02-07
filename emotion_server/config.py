"""
Emotion HR Server Configuration
Modify these settings as needed for your deployment.
"""

# Server Configuration
SERVER_HOST = '0.0.0.0'  # Listen on all interfaces
SERVER_PORT = 5000
DEBUG_MODE = False

# Model Configuration
YOLO_MODEL_PATH = r"D:\\arun-pt2\\yolov8n-face.pt"  # Update this path
CONFIDENCE_THRESHOLD = 0.5

# CORS Configuration (for distributed setup)
ALLOWED_ORIGINS = ["*"]  # Allow all origins - you can restrict this to specific IPs

# Emotion Processing
FRAME_PROCESSING_INTERVAL = 3  # Process every Nth frame
MAX_EMOTION_HISTORY = 100  # Keep last N emotion entries per room
DATA_CLEANUP_INTERVAL = 300  # Clean up old data every 5 minutes (seconds)
MAX_DATA_AGE = 86400  # Keep data for max 24 hours (seconds)

# WebSocket Configuration
CORS_ALLOWED_ORIGINS = "*"  # Allow connections from any origin

# Logging
LOG_LEVEL = 'INFO'

# Default Room Settings
DEFAULT_ROOM_ID = 'workplace-2026'