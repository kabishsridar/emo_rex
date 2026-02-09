import cv2
from ultralytics import YOLO
from deepface import DeepFace
import numpy as np

YOLO_MODEL_PATH = r"D:\\emo_rex\\yolov8n-face.pt"
CONFIDENCE_THRESHOLD = 0.5

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

def analyze_emotion(face_img):
    """Analyze emotion using DeepFace"""
    try:
        # DeepFace expects BGR image
        result = DeepFace.analyze(
            face_img, 
            actions=['emotion'],
            enforce_detection=False,
            silent=True
        )
        
        if isinstance(result, list):
            result = result[0]
        
        emotions = result.get('emotion', {})
        dominant = result.get('dominant_emotion', 'neutral')
        
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
    print("   [M] - Toggle mirror mode")
    print("=" * 50)

    show_bars = True
    mirror_mode = True  # Start with mirrored view (natural for users)
    frame_count = 0

    # Cache for smoother display
    last_emotions = {}
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Apply mirror effect if enabled (flip horizontally)
        if mirror_mode:
            frame = cv2.flip(frame, 1)  # 1 = horizontal flip

        display_frame = frame.copy()
        
        # Add title overlay
        cv2.rectangle(display_frame, (0, 0), (400, 40), (30, 30, 30), -1)
        cv2.putText(display_frame, "EMOTION RECOGNITION", (10, 28), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        
        # Detect faces using YOLO
        results = model(frame, verbose=False, conf=CONFIDENCE_THRESHOLD)
        
        face_count = 0
        
        for result in results:
            for idx, box in enumerate(result.boxes.xyxy):
                x1, y1, x2, y2 = map(int, box)
                
                # Extract face region with padding
                pad = 10
                y1_pad = max(0, y1 - pad)
                y2_pad = min(frame.shape[0], y2 + pad)
                x1_pad = max(0, x1 - pad)
                x2_pad = min(frame.shape[1], x2 + pad)
                
                face = frame[y1_pad:y2_pad, x1_pad:x2_pad]
                
                if face.size == 0 or face.shape[0] < 20 or face.shape[1] < 20:
                    continue
                
                face_count += 1
                
                # Analyze every 3rd frame for performance
                if frame_count % 3 == 0 or idx not in last_emotions:
                    emotions_dict, dominant_emotion = analyze_emotion(face)
                    if emotions_dict:
                        last_emotions[idx] = (emotions_dict, dominant_emotion)
                
                # Use cached or new results
                if idx in last_emotions:
                    emotions_dict, dominant_emotion = last_emotions[idx]
                    
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
        
        # Clear cache if no faces
        if face_count == 0:
            last_emotions.clear()
        
        # Show face count
        cv2.putText(display_frame, f"Faces: {face_count}", (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        # Show mirror mode indicator
        mirror_indicator = "🪞 MIRRORED" if mirror_mode else "📷 NORMAL"
        cv2.putText(display_frame, mirror_indicator, (display_frame.shape[1] - 150, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
        
        # Show controls hint
        mirror_status = "ON" if mirror_mode else "OFF"
        cv2.putText(display_frame, f"Press Q to quit | S to screenshot | B to toggle bars | M to toggle mirror ({mirror_status})",
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
        elif key == ord('m'):
            mirror_mode = not mirror_mode
            print(f"🪞 Mirror mode: {'ON' if mirror_mode else 'OFF'}")
    
    cap.release()
    cv2.destroyAllWindows()
    print("✅ Cleanup complete!")

if __name__ == "__main__":
    main()