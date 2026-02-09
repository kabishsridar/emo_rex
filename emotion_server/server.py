from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit, join_room, leave_room
from flask_cors import CORS
import json
import threading
import time
from datetime import datetime
import base64
# OpenCV imports are handled conditionally to avoid NumPy compatibility issues
CV2_AVAILABLE = False
cv2 = None
np = None
from emotion_tracking import analyze_emotion, YOLO_MODEL_PATH, CONFIDENCE_THRESHOLD
# from ultralytics import YOLO  # Commented out due to NumPy compatibility issues

app = Flask(__name__)
app.config['SECRET_KEY'] = 'emotion-hr-secret-key-2026'
CORS(app, origins=["*"])  # Allow all origins for distributed setup
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global variables for tracking
connected_clients = {}  # client_id -> {'type': 'employee'/'hr', 'room': room_id}
emotion_data = {}  # room_id -> list of recent emotion entries
face_detection_model = None

# Initialize YOLO model for server-side processing
def init_models():
    global face_detection_model
    try:
        from ultralytics import YOLO
        face_detection_model = YOLO(YOLO_MODEL_PATH)
        print("Server: YOLO Face Detection Model Loaded")
    except Exception as e:
        print(f"Server: Failed to load YOLO model: {e}")
        face_detection_model = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/employee')
def employee_view():
    return render_template('employee.html')

@app.route('/hr')
def hr_view():
    return render_template('hr.html')

@app.route('/api/status')
def api_status():
    """API endpoint to check server status"""
    return jsonify({
        'status': 'running',
        'timestamp': datetime.now().isoformat(),
        'connected_clients': len(connected_clients)
    })

@socketio.on('connect')
def handle_connect():
    client_id = request.sid
    print(f"🔗 Client connected: {client_id}")

@socketio.on('disconnect')
def handle_disconnect():
    client_id = request.sid
    if client_id in connected_clients:
        client_info = connected_clients[client_id]
        room = client_info.get('room')
        if room:
            leave_room(room)
            # Notify others in the room
            emit('user_disconnected', {
                'client_id': client_id,
                'user_type': client_info.get('type')
            }, room=room, skip_sid=client_id)
        del connected_clients[client_id]
        print(f"👋 Client disconnected: {client_id}")

@socketio.on('join_room')
def handle_join_room(data):
    client_id = request.sid
    room_id = data.get('room_id')
    user_type = data.get('user_type')  # 'employee' or 'hr'
    user_name = data.get('user_name', f"User-{client_id[:6]}")

    if not room_id:
        emit('error', {'message': 'Room ID is required'})
        return

    # Store client info
    connected_clients[client_id] = {
        'type': user_type,
        'room': room_id,
        'name': user_name,
        'joined_at': datetime.now().isoformat()
    }

    join_room(room_id)

    # Initialize emotion data for this room if not exists
    if room_id not in emotion_data:
        emotion_data[room_id] = []

    # Notify others in the room
    emit('user_joined', {
        'client_id': client_id,
        'user_name': user_name,
        'user_type': user_type,
        'timestamp': datetime.now().isoformat()
    }, room=room_id, skip_sid=client_id)

    # Send current room status to the new client
    room_clients = [info for cid, info in connected_clients.items()
                   if info.get('room') == room_id]

    emit('room_status', {
        'room_id': room_id,
        'clients': room_clients,
        'emotion_history': emotion_data[room_id][-50:]  # Last 50 entries
    })

    print(f"User {user_name} ({user_type}) joined room: {room_id}")

@socketio.on('hr_emotion_frame')
def handle_hr_emotion_frame(data):
    client_id = request.sid
    if client_id not in connected_clients:
        return

    client_info = connected_clients[client_id]
    if client_info.get('type') != 'hr':
        return

    frame_data = data.get('frame')
    frame_count = data.get('frame_count', 0)

    if not frame_data or not face_detection_model or not CV2_AVAILABLE:
        return

    try:
        # Decode base64 frame
        frame_bytes = base64.b64decode(frame_data.split(',')[1])
        np_arr = np.frombuffer(frame_bytes, np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # Detect faces
        results = face_detection_model(frame, verbose=False, conf=CONFIDENCE_THRESHOLD)

        for result_idx, result in enumerate(results):
            for box_idx, box in enumerate(result.boxes.xyxy):
                x1, y1, x2, y2 = map(int, box)

                # Extract face
                face = frame[y1:y2, x1:x2]
                if face.size > 0:
                    emotions, dominant = analyze_emotion(face)
                    if emotions:
                        # Send back emotion data with bbox
                        emit('hr_emotion_result', {
                            'emotions': emotions,
                            'dominant_emotion': dominant,
                            'bbox': [x1, y1, x2, y2],
                            'face_index': box_idx
                        })
                        break  # Process only first face for HR
    except Exception as e:
        print(f"HR emotion processing error: {e}")

@socketio.on('emotion_update')
def handle_emotion_update(data):
    client_id = request.sid
    if client_id not in connected_clients:
        return

    client_info = connected_clients[client_id]
    room_id = client_info.get('room')
    user_name = client_info.get('name')

    if not room_id:
        return

    # Add timestamp and user info
    emotion_entry = {
        'client_id': client_id,
        'user_name': user_name,
        'timestamp': datetime.now().isoformat(),
        'emotions': data.get('emotions', {}),
        'dominant_emotion': data.get('dominant_emotion', 'neutral'),
        'face_detected': data.get('face_detected', False)
    }

    # Store in room's emotion data (keep last 100 entries)
    if room_id not in emotion_data:
        emotion_data[room_id] = []
    emotion_data[room_id].append(emotion_entry)
    emotion_data[room_id] = emotion_data[room_id][-100:]

    # Broadcast to HR clients in the same room
    emit('emotion_update', emotion_entry, room=room_id, skip_sid=client_id)

@socketio.on('video_frame')
def handle_video_frame(data):
    client_id = request.sid
    if client_id not in connected_clients:
        return

    client_info = connected_clients[client_id]
    room_id = client_info.get('room')

    if not room_id:
        return

    # Process frame for emotion detection on server side if needed
    frame_data = data.get('frame')
    process_server_side = data.get('process_server', False)

    if process_server_side and frame_data and face_detection_model and CV2_AVAILABLE:
        try:
            # Decode base64 frame
            frame_bytes = base64.b64decode(frame_data.split(',')[1])
            np_arr = np.frombuffer(frame_bytes, np.uint8)
            frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

            # Detect faces
            results = face_detection_model(frame, verbose=False, conf=CONFIDENCE_THRESHOLD)

            for result in results:
                for box in result.boxes.xyxy:
                    x1, y1, x2, y2 = map(int, box)

                    # Extract face
                    face = frame[y1:y2, x1:x2]
                    if face.size > 0:
                        emotions, dominant = analyze_emotion(face)
                        if emotions:
                            # Send back emotion data
                            emit('server_emotion_result', {
                                'emotions': emotions,
                                'dominant_emotion': dominant,
                                'bbox': [x1, y1, x2, y2]
                            })
                            break
        except Exception as e:
            print(f"Server-side processing error: {e}")

    # Broadcast frame to HR clients (for monitoring)
    if client_info.get('type') == 'employee':
        emit('employee_frame', {
            'client_id': client_id,
            'user_name': client_info.get('name'),
            'frame': frame_data,
            'timestamp': datetime.now().isoformat()
        }, room=room_id, skip_sid=client_id)

@socketio.on('hr_command')
def handle_hr_command(data):
    client_id = request.sid
    if client_id not in connected_clients:
        return

    client_info = connected_clients[client_id]
    if client_info.get('type') != 'hr':
        emit('error', {'message': 'Only HR can send commands'})
        return

    room_id = client_info.get('room')
    command = data.get('command')
    target_client = data.get('target_client')

    if command == 'request_emotion_focus':
        # Ask specific employee to focus on emotion detection
        emit('hr_command', {
            'command': 'focus_emotion',
            'hr_name': client_info.get('name')
        }, room=room_id, to=target_client)

    elif command == 'broadcast_message':
        message = data.get('message', '')
        emit('hr_announcement', {
            'message': message,
            'hr_name': client_info.get('name'),
            'timestamp': datetime.now().isoformat()
        }, room=room_id)

@socketio.on('get_room_stats')
def handle_get_room_stats():
    client_id = request.sid
    if client_id not in connected_clients:
        return

    client_info = connected_clients[client_id]
    room_id = client_info.get('room')

    if not room_id:
        return

    # Calculate room statistics
    room_clients = [info for cid, info in connected_clients.items()
                   if info.get('room') == room_id]

    employees = [c for c in room_clients if c['type'] == 'employee']
    hrs = [c for c in room_clients if c['type'] == 'hr']

    # Calculate emotion statistics
    recent_emotions = emotion_data.get(room_id, [])
    if recent_emotions:
        latest_emotions = recent_emotions[-len(employees):] if employees else []

        emotion_counts = {}
        for entry in latest_emotions:
            emotion = entry.get('dominant_emotion', 'neutral')
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

        most_common_emotion = max(emotion_counts.items(), key=lambda x: x[1]) if emotion_counts else ('neutral', 0)
    else:
        most_common_emotion = ('neutral', 0)

    stats = {
        'total_clients': len(room_clients),
        'employees': len(employees),
        'hrs': len(hrs),
        'room_id': room_id,
        'most_common_emotion': most_common_emotion[0],
        'emotion_distribution': emotion_counts if 'emotion_counts' in locals() else {},
        'timestamp': datetime.now().isoformat()
    }

    emit('room_stats', stats)

def cleanup_old_data():
    """Clean up old emotion data and disconnected clients"""
    while True:
        current_time = datetime.now()
        # Clean up old emotion data (keep only last 24 hours)
        for room_id in list(emotion_data.keys()):
            emotion_data[room_id] = [
                entry for entry in emotion_data[room_id]
                if (current_time - datetime.fromisoformat(entry['timestamp'])).total_seconds() < 86400
            ]
            if not emotion_data[room_id]:
                del emotion_data[room_id]

        time.sleep(300)  # Clean up every 5 minutes

if __name__ == '__main__':
    # Initialize models
    init_models()

    # Start cleanup thread
    cleanup_thread = threading.Thread(target=cleanup_old_data, daemon=True)
    cleanup_thread.start()

    print("Starting Emotion HR Server...")
    print("WebSocket server ready for real-time emotion monitoring")
    print("=" * 60)
    print("Server URLs:")
    print("   Main Page:     http://0.0.0.0:5000")
    print("   Employee View: http://0.0.0.0:5000/employee")
    print("   HR Dashboard:  http://0.0.0.0:5000/hr")
    print("   API Status:    http://0.0.0.0:5000/api/status")
    print("=" * 60)
    print("Network Configuration:")
    print("   - Make sure port 5000 is open in firewall")
    print("   - Note your server's IP address for clients")
    print("   - Clients will connect using: http://[SERVER-IP]:5000")
    print("=" * 60)

    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)