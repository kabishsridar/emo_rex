import cv2
from ultralytics import YOLO
from deepface import DeepFace
import numpy as np

YOLO_MODEL_PATH = r"D:\\emo_rex\\yolov8n-face.pt"
CONFIDENCE_THRESHOLD = 0.7  # Increased for better accuracy
MIN_FACE_SIZE = 80  # Minimum face size in pixels for reliable emotion detection
MAX_FACE_SIZE_RATIO = 0.8  # Maximum face size relative to frame (avoid close-up artifacts)
FACE_PADDING_RATIO = 0.15  # Padding as percentage of face size
TRACKING_DISTANCE_THRESHOLD = 50  # Maximum distance to consider same face (pixels)
CACHE_TIMEOUT = 10  # Frames to keep cached data without detection
SMOOTHING_FACTOR = 0.3  # Lower = more smoothing, Higher = more responsive

# Emotion colors (BGR format)
EMOTION_COLORS = {
    'angry': (0, 0, 255),      # Red
    'disgust': (0, 128, 0),    # Dark Green
    'fear': (128, 0, 128),     # Purple
    'happy': (0, 255, 255),    # Yellow
    'sad': (255, 0, 0),        # Blue
    'surprise': (0, 165, 255), # Orange
    'neutral': (200, 200, 200) # Gray
}

# Emotion emojis
EMOTION_EMOJIS = {
    'angry': '😠',
    'disgust': '🤢',
    'fear': '😨',
    'happy': '😊',
    'sad': '😢',
    'surprise': '😲',
    'neutral': '😐'
}

def draw_fancy_box(frame, x1, y1, x2, y2, color, thickness=2):
    """Draw a fancy bounding box with corner accents"""
    cv2.rectangle(frame, (x1, y1), (x2, y2), color, thickness)
    
    # Corner length
    corner_len = min(20, (x2-x1)//4, (y2-y1)//4)
    
    # Top-left corner
    cv2.line(frame, (x1, y1), (x1 + corner_len, y1), color, thickness + 2)
    cv2.line(frame, (x1, y1), (x1, y1 + corner_len), color, thickness + 2)
    
    # Top-right corner
    cv2.line(frame, (x2, y1), (x2 - corner_len, y1), color, thickness + 2)
    cv2.line(frame, (x2, y1), (x2, y1 + corner_len), color, thickness + 2)
    
    # Bottom-left corner
    cv2.line(frame, (x1, y2), (x1 + corner_len, y2), color, thickness + 2)
    cv2.line(frame, (x1, y2), (x1, y2 - corner_len), color, thickness + 2)
    
    # Bottom-right corner
    cv2.line(frame, (x2, y2), (x2 - corner_len, y2), color, thickness + 2)
    cv2.line(frame, (x2, y2), (x2, y2 - corner_len), color, thickness + 2)

def draw_label_box(frame, text, x, y, color, bg_alpha=0.7):
    """Draw text with a semi-transparent background"""
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.7
    thickness = 2
    
    (text_w, text_h), baseline = cv2.getTextSize(text, font, font_scale, thickness)
    
    # Create overlay for transparent background
    overlay = frame.copy()
    cv2.rectangle(overlay, (x, y - text_h - 10), (x + text_w + 10, y), color, -1)
    cv2.addWeighted(overlay, bg_alpha, frame, 1 - bg_alpha, 0, frame)
    
    # Draw text
    cv2.putText(frame, text, (x + 5, y - 5), font, font_scale, (255, 255, 255), thickness)

def draw_emotion_bar(frame, emotions_dict, x, y, width=150, height=15):
    """Draw emotion probability bars"""
    y_offset = 0
    for emotion, score in sorted(emotions_dict.items(), key=lambda x: -x[1]):
        color = EMOTION_COLORS.get(emotion, (200, 200, 200))
        
        # Background bar
        cv2.rectangle(frame, (x, y + y_offset), (x + width, y + y_offset + height), (50, 50, 50), -1)
        
        # Filled bar (score is 0-100 from DeepFace)
        bar_width = int(width * score / 100)
        cv2.rectangle(frame, (x, y + y_offset), (x + bar_width, y + y_offset + height), color, -1)
        
        # Label
        label = f"{emotion[:3].upper()}: {score:.0f}%"
        cv2.putText(frame, label, (x + 5, y + y_offset + height - 3), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.35, (255, 255, 255), 1)
        
        y_offset += height + 2

def validate_face_quality(face_img, original_bbox):
    """Validate if face is suitable for emotion analysis"""
    if face_img is None or face_img.size == 0:
        return False

    height, width = face_img.shape[:2]
    bbox_width = original_bbox[2] - original_bbox[0]
    bbox_height = original_bbox[3] - original_bbox[1]

    # Check minimum size
    if width < MIN_FACE_SIZE or height < MIN_FACE_SIZE:
        return False

    # Check aspect ratio (avoid extremely distorted faces)
    aspect_ratio = width / height
    if aspect_ratio < 0.5 or aspect_ratio > 2.0:
        return False

    # Check if face is not too close to camera (creates artifacts)
    if bbox_width > MAX_FACE_SIZE_RATIO * 1280 or bbox_height > MAX_FACE_SIZE_RATIO * 720:
        return False

    return True

def preprocess_face(face_img):
    """Preprocess face image for better DeepFace performance"""
    if face_img is None or face_img.size == 0:
        return None

    # Resize to standard size for consistent analysis
    target_size = (224, 224)  # Standard size for most emotion models
    resized = cv2.resize(face_img, target_size, interpolation=cv2.INTER_LINEAR)

    return resized

def find_closest_face(current_bbox, last_emotions, current_frame):
    """Find the closest cached face based on bounding box center distance"""
    current_center = ((current_bbox[0] + current_bbox[2]) / 2,
                     (current_bbox[1] + current_bbox[3]) / 2)

    closest_face_id = None
    min_distance = float('inf')

    for face_id, (_, _, cached_center, cached_frame) in last_emotions.items():
        # Check if cache is not too old
        if current_frame - cached_frame > CACHE_TIMEOUT:
            continue

        # Calculate distance between centers
        distance = ((current_center[0] - cached_center[0]) ** 2 +
                   (current_center[1] - cached_center[1]) ** 2) ** 0.5

        if distance < min_distance and distance < TRACKING_DISTANCE_THRESHOLD:
            min_distance = distance
            closest_face_id = face_id

    return closest_face_id

def smooth_emotions(current_emotions, face_id, emotion_history):
    """Apply temporal smoothing to emotion scores"""
    if face_id not in emotion_history:
        emotion_history[face_id] = current_emotions.copy()
        # Return both the emotions dict and the dominant emotion
        dominant_emotion = max(current_emotions, key=current_emotions.get)
        return current_emotions, dominant_emotion

    previous_emotions = emotion_history[face_id]
    smoothed_emotions = {}

    for emotion in current_emotions:
        if emotion in previous_emotions:
            # Exponential moving average
            smoothed_emotions[emotion] = (SMOOTHING_FACTOR * current_emotions[emotion] +
                                        (1 - SMOOTHING_FACTOR) * previous_emotions[emotion])
        else:
            smoothed_emotions[emotion] = current_emotions[emotion]

    # Update history
    emotion_history[face_id] = smoothed_emotions.copy()

    # Find new dominant emotion after smoothing
    dominant_emotion = max(smoothed_emotions, key=smoothed_emotions.get)

    return smoothed_emotions, dominant_emotion

def analyze_emotion(face_img, original_bbox):
    """Analyze emotion using DeepFace with preprocessing"""
    try:
        # Validate face quality first
        if not validate_face_quality(face_img, original_bbox):
            return None, None

        # Preprocess face for better accuracy
        processed_face = preprocess_face(face_img)
        if processed_face is None:
            return None, None

        # Use DeepFace with optimized parameters
        result = DeepFace.analyze(
            processed_face,
            actions=['emotion'],
            enforce_detection=False,
            silent=True,
            detector_backend='opencv'  # More reliable for pre-processed faces
        )

        if isinstance(result, list):
            result = result[0]

        emotions = result.get('emotion', {})
        dominant = result.get('dominant_emotion', 'neutral')

        # Convert scores to percentages and validate
        if emotions:
            total = sum(emotions.values())
            if total > 0:
                emotions = {k: (v / total) * 100 for k, v in emotions.items()}
            else:
                return None, None

        return emotions, dominant
    except Exception as e:
        return None, None

def main():
    print("=" * 50)
    print("🎭 EMOTION RECOGNITION SYSTEM")
    print("=" * 50)
    print("Loading models...")
    
    # Load YOLO face detection model
    model = YOLO(YOLO_MODEL_PATH)
    print("✅ YOLO Face Detection Model Loaded")
    
    # Initialize DeepFace (it downloads models on first use)
    print("✅ DeepFace Emotion Detector Ready")
    
    # Start webcam
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
    
    if not cap.isOpened():
        print(" Error: Could not open webcam!")
        return
    
    print("\n🎥 Webcam Started!")
    print(" Controls:")
    print("   [Q] - Quit")
    print("   [S] - Screenshot")
    print("   [B] - Toggle emotion bars")
    print("=" * 50)
    
    show_bars = True
    frame_count = 0

    # Cache for smoother display with temporal smoothing
    last_emotions = {}  # face_id -> (emotions, dominant, bbox_center, frame_count)
    emotion_history = {}  # face_id -> emotion scores for smoothing
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        frame_count += 1
        display_frame = frame.copy()
        
        # Add title overlay
        cv2.rectangle(display_frame, (0, 0), (400, 40), (30, 30, 30), -1)
        cv2.putText(display_frame, "EMOTION RECOGNITION", (10, 28), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        # Detect faces using YOLO
        results = model(frame, verbose=False, conf=CONFIDENCE_THRESHOLD)
        
        face_count = 0
        current_faces = []  # Track faces found in this frame

        for result in results:
            for box in result.boxes.xyxy:
                x1, y1, x2, y2 = map(int, box)
                bbox = (x1, y1, x2, y2)

                # Calculate adaptive padding based on face size
                face_width = x2 - x1
                face_height = y2 - y1
                pad_x = max(10, int(face_width * FACE_PADDING_RATIO))
                pad_y = max(10, int(face_height * FACE_PADDING_RATIO))

                # Extract face region with adaptive padding
                y1_pad = max(0, y1 - pad_y)
                y2_pad = min(frame.shape[0], y2 + pad_y)
                x1_pad = max(0, x1 - pad_x)
                x2_pad = min(frame.shape[1], x2 + pad_x)

                face = frame[y1_pad:y2_pad, x1_pad:x2_pad]

                # Skip invalid faces
                if face.size == 0:
                    continue

                face_count += 1

                # Find closest cached face for stable tracking
                face_id = find_closest_face(bbox, last_emotions, frame_count)

                # If no close face found, assign new ID
                if face_id is None:
                    face_id = len(last_emotions) + len(current_faces)

                current_faces.append(face_id)

                # Analyze more frequently for better responsiveness (every 2nd frame)
                should_analyze = (frame_count % 2 == 0 or face_id not in last_emotions)

                if should_analyze:
                    emotions_dict, dominant_emotion = analyze_emotion(face, bbox)
                    if emotions_dict and dominant_emotion:
                        # Apply temporal smoothing
                        smoothed_emotions, smoothed_dominant = smooth_emotions(emotions_dict, face_id, emotion_history)
                        # Store bbox center for tracking
                        bbox_center = ((x1 + x2) / 2, (y1 + y2) / 2)
                        last_emotions[face_id] = (smoothed_emotions, smoothed_dominant, bbox_center, frame_count)

                # Use cached results
                if face_id in last_emotions:
                    emotions_dict, dominant_emotion, _, _ = last_emotions[face_id]

                    # Get color for this emotion
                    color = EMOTION_COLORS.get(dominant_emotion, (0, 255, 0))

                    # Draw fancy bounding box
                    draw_fancy_box(display_frame, x1, y1, x2, y2, color, 2)

                    # Create label
                    confidence = emotions_dict.get(dominant_emotion, 0)
                    label = f"{dominant_emotion.upper()} {confidence:.0f}%"

                    # Draw label
                    draw_label_box(display_frame, label, x1, y1 - 5, color)

                    # Draw emotion bars if enabled
                    if show_bars and x2 + 170 < display_frame.shape[1]:
                        draw_emotion_bar(display_frame, emotions_dict, x2 + 10, y1, 150, 12)
                else:
                    # Face detected but analyzing
                    cv2.rectangle(display_frame, (x1, y1), (x2, y2), (100, 100, 100), 2)
                    cv2.putText(display_frame, "ANALYZING...", (x1, y1-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (100, 100, 100), 1)
        
        # Clean up old cached faces (not detected in current frame)
        faces_to_remove = []
        for face_id in last_emotions:
            if face_id not in current_faces:
                _, _, _, last_seen_frame = last_emotions[face_id]
                if frame_count - last_seen_frame > CACHE_TIMEOUT:
                    faces_to_remove.append(face_id)

        for face_id in faces_to_remove:
            last_emotions.pop(face_id, None)
            emotion_history.pop(face_id, None)
        
        # Show face count
        cv2.putText(display_frame, f"Faces: {face_count}", (10, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
        
        # Show controls hint
        cv2.putText(display_frame, "Press Q to quit | S to screenshot | B to toggle bars", 
                    (10, display_frame.shape[0] - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (150, 150, 150), 1)
        
        # Display the frame
        cv2.imshow("Emotion Recognition - Hackathon Demo", display_frame)
        
        # Handle key presses
        key = cv2.waitKey(1) & 0xFF
        
        if key == ord('q'):
            print("\n👋 Exiting...")
            break
        elif key == ord('s'):
            filename = f"screenshot_{frame_count}.png"
            cv2.imwrite(filename, display_frame)
            print(f"📸 Screenshot saved: {filename}")
        elif key == ord('b'):
            show_bars = not show_bars
            print(f"📊 Emotion bars: {'ON' if show_bars else 'OFF'}")
    
    cap.release()
    cv2.destroyAllWindows()
    print("✅ Cleanup complete!")

if __name__ == "__main__":
    main()