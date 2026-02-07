# 👤 Employee Emotion Client

Distributed client for employee emotion monitoring. Connects to the central Emotion HR server.

## 🚀 Quick Start

### Prerequisites
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Webcam-enabled device
- Network connection to Emotion HR server

### Setup

1. **Open the client:**
   - Open `index.html` in your web browser
   - Or serve via local web server (optional)

2. **Connect to server:**
   - Enter the server's IP address
   - Enter your name
   - Enter the Room ID (same as HR uses)
   - Click "Connect to HR"

## 🔧 Configuration

### Server Connection
- **Server IP:** IP address of the machine running `emotion_server`
- **Port:** 5000 (default)
- **Room ID:** Shared identifier for your team/session

### Finding Server IP

Ask your HR admin for the server IP address, or:

**If server is on same network:**
- Server typically runs on: `192.168.1.xxx`
- Check with HR for exact IP

**If server is remote:**
- Use the public IP provided by HR
- May require VPN for secure access

## 🎯 Features

### Real-time Monitoring
- Live camera feed with emotion detection
- 7 emotion types: Happy, Sad, Angry, Neutral, Surprise, Fear, Disgust
- Fancy bounding boxes and emotion labels
- Real-time emotion overlay

### Connection Management
- Visual connection status
- Automatic reconnection on network issues
- Room-based session management

### Privacy & Security
- Camera feed stays local to your browser
- Only emotion data sent to server
- No video streaming (only processed data)

## 🌐 Browser Requirements

### Supported Browsers
- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+

### Required Permissions
- **Camera Access:** Allow webcam permission when prompted
- **WebRTC:** Enable for real-time communication
- **JavaScript:** Must be enabled

## 📱 Usage Guide

### Step-by-Step Setup

1. **Launch Client:**
   ```bash
   # Option 1: Open directly in browser
   # Double-click index.html

   # Option 2: Serve locally (if needed)
   python -m http.server 8000
   # Then visit: http://localhost:8000
   ```

2. **Enter Connection Details:**
   - Server IP: `192.168.1.100` (example)
   - Your Name: `John Doe`
   - Room ID: `workplace-2026`

3. **Allow Camera:**
   - Browser will prompt for camera permission
   - Click "Allow" to enable emotion detection

4. **Start Monitoring:**
   - Click "Connect to HR"
   - Wait for "Connected" status
   - Your emotions are now being monitored!

### Understanding the Interface

- **🟢 Green Status:** Connected to server
- **🔴 Red Status:** Disconnected
- **📹 Camera Feed:** Your live video with emotion overlays
- **😊 Current Emotion:** Your detected emotional state
- **📊 Confidence:** Accuracy percentage of detection

## 🔒 Privacy & Data

### What We Track
- **Emotions:** 7 emotion types with confidence scores
- **Face Detection:** Presence of faces in frame
- **Timestamps:** When emotions change

### What We Don't Track
- ❌ Raw video footage
- ❌ Audio recordings
- ❌ Personal images
- ❌ Location data

### Data Transmission
- Real-time emotion data sent to HR server
- Encrypted WebSocket connection
- Processed locally on your device
- Only aggregated analytics stored

## 🛠️ Troubleshooting

### Connection Issues

**"Failed to connect to server":**
- ✅ Check server IP address
- ✅ Verify server is running
- ✅ Check network connectivity
- ✅ Ensure port 5000 is not blocked

**"Camera not accessible":**
- ✅ Allow camera permissions in browser
- ✅ Check if camera is used by another app
- ✅ Try refreshing the page
- ✅ Test camera in other applications

**"Room connection failed":**
- ✅ Verify Room ID matches HR's room
- ✅ Check if room exists on server
- ✅ Try different room name

### Performance Issues

**Slow emotion detection:**
- Close other browser tabs
- Restart browser
- Check internet connection
- Update browser to latest version

**Laggy interface:**
- Close unnecessary applications
- Free up system memory
- Use Chrome for best performance

## 🎨 Customization

### Interface Themes
The client uses a modern gradient design. For custom branding:
- Edit CSS in `index.html`
- Change colors and styling
- Add company logo/images

### Connection Settings
Modify default values in the HTML:
```html
<input type="text" id="serverIP" value="192.168.1.100">
<input type="text" id="roomId" value="your-room-id">
```

## 📊 System Requirements

### Minimum Requirements
- **Browser:** Modern web browser
- **CPU:** 2GHz dual-core
- **RAM:** 4GB
- **Network:** 5 Mbps internet
- **Camera:** 720p webcam

### Recommended Requirements
- **Browser:** Chrome 90+
- **CPU:** 3GHz quad-core
- **RAM:** 8GB
- **Network:** 25 Mbps internet
- **Camera:** 1080p webcam

## 🔄 Updates

### Checking for Updates
- Download latest client files from HR
- Replace `index.html` with updated version
- Clear browser cache if issues persist

### Version Compatibility
- Ensure client and server versions match
- Check with HR for compatible versions
- Update both simultaneously for best results

## 📞 Support

### Getting Help
1. **Check this README** for common solutions
2. **Contact HR Admin** for server-specific issues
3. **Browser Console** for technical errors (F12 → Console)

### Common Support Questions

**"Why can't I see my emotions?"**
- Camera permission not granted
- Face not clearly visible
- Poor lighting conditions

**"Connection keeps dropping?"**
- Unstable network connection
- Server overload (many users)
- Firewall blocking connections

**"Emotions seem inaccurate?"**
- Face detection requires good lighting
- Remove glasses/sunglasses if possible
- Ensure face is clearly visible

## 🚀 Advanced Usage

### Multiple Monitors
- Use separate browser windows
- Connect to different rooms
- Monitor multiple teams simultaneously

### Integration
- Can be embedded in other web applications
- API available for custom integrations
- Webhook support for notifications

---

**Happy monitoring! Your emotional wellness matters to us. 💙**