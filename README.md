# 🧠 Distributed Emotion HR System

A complete workplace emotional intelligence monitoring platform designed for distributed deployment across multiple laptops.

## 🏗️ Architecture Overview

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Employee      │    │     Server      │    │       HR        │
│   Laptop #1     │◄──►│   (Central)     │◄──►│   Dashboard     │
│                 │    │                 │    │                 │
│ • Web Browser   │    │ • Flask Server  │    │ • Web Browser   │
│ • Camera Feed   │    │ • AI Processing │    │ • Multi-View    │
│ • Real-time     │    │ • WebSocket Hub │    │ • Analytics     │
│   Emotions      │    │ • Database      │    │ • Controls      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
       ▲                       ▲                       ▲
       │                       │                       │
       └───────── Network ─────┴───────────────────────┘
```

## 🎯 System Components

### 1. 🖥️ **Emotion Server** (`emotion_server/`)
**Central processing unit** - handles all AI processing and coordination.

**Features:**
- Flask web server with WebSocket support
- YOLOv8 face detection + DeepFace emotion analysis
- Real-time data processing and storage
- Multi-client connection management
- Room-based session organization

### 2. 👤 **Employee Client** (`emotion_employee_client/`)
**Employee monitoring interface** - runs on employee laptops.

**Features:**
- Real-time emotion detection from webcam
- Beautiful UI with emotion overlays
- Privacy-focused (only emotion data transmitted)
- Easy server connection setup

### 3. 🎯 **HR Client** (`emotion_hr_client/`)
**Management dashboard** - runs on HR laptops.

**Features:**
- Multi-employee monitoring dashboard
- Real-time analytics and charts
- HR controls and announcements
- Optional HR self-monitoring

## 🚀 Quick Deployment Guide

### Prerequisites
- **3 Laptops/Computers** (one for each component)
- **Python 3.8+** (for server only)
- **Modern Web Browsers** (Chrome/Firefox recommended)
- **Webcams** (for emotion detection)
- **Network Connection** (same network or internet)

### Step 1: Prepare the Server Laptop

1. **Install Python dependencies:**
   ```bash
   cd emotion_server
   pip install -r requirements.txt
   ```

2. **Download AI models:**
   - Download `yolov8n-face.pt` from Ultralytics
   - Place at path specified in `config.py`

3. **Start the server:**
   ```bash
   python run_server.py
   ```

4. **Note the server IP address** (displayed on startup)

### Step 2: Configure Employee Laptops

1. **Copy `emotion_employee_client/` folder**

2. **Open `index.html` in web browser**

3. **Enter connection details:**
   - Server IP: `[SERVER-IP-ADDRESS]`
   - Room ID: `workplace-2026` (same for all)
   - Employee Name: Individual names

4. **Allow camera permissions and connect**

### Step 3: Configure HR Laptop

1. **Copy `emotion_hr_client/` folder**

2. **Open `index.html` in web browser**

3. **Enter connection details:**
   - Server IP: `[SERVER-IP-ADDRESS]`
   - Room ID: `workplace-2026` (same as employees)
   - HR Name: `HR Manager`

4. **Connect and start monitoring**

## 🌐 Network Configuration

### Local Network Setup (Recommended)
```
Network: 192.168.1.0/24
Server: 192.168.1.100:5000
Employees: Connect to 192.168.1.100
HR: Connect to 192.168.1.100
```

### Internet Setup (Advanced)
```
Server: your-public-ip:5000
Clients: Connect to your-public-ip
Requirements: Port forwarding, firewall config
```

### Finding Your Server IP

**Windows:**
```cmd
ipconfig
```

**Linux/Mac:**
```bash
ifconfig
# or
ip addr show
```

Look for: `192.168.x.x` or `10.x.x.x` (local network IP)

## 📋 Component Details

### Server Specifications
- **CPU:** Quad-core 3GHz+ (for AI processing)
- **RAM:** 8GB minimum, 16GB recommended
- **Storage:** 5GB (models + logs)
- **Network:** Stable 10Mbps+ connection

### Client Specifications
- **Browser:** Chrome 80+, Firefox 75+, Edge 80+
- **CPU:** Dual-core 2GHz+ (for UI rendering)
- **RAM:** 4GB minimum
- **Camera:** 720p webcam minimum

## 🔧 Configuration Files

### Server Configuration (`emotion_server/config.py`)
```python
SERVER_HOST = '0.0.0.0'        # Listen on all interfaces
SERVER_PORT = 5000             # Server port
DEBUG_MODE = False             # Production mode
YOLO_MODEL_PATH = r"path\to\model"  # AI model location
```

### Client Configuration
- **Server IP:** Update in browser interface
- **Room ID:** Shared across all clients
- **User Names:** Individual identifiers

## 🎨 Features Overview

### Employee Experience
- **Privacy-First:** Only emotion data transmitted
- **Real-Time Feedback:** Live emotion detection
- **Beautiful UI:** Modern gradient design
- **Easy Setup:** Browser-based, no installation

### HR Experience
- **Multi-Employee View:** Monitor entire team
- **Analytics Dashboard:** Charts and statistics
- **Interactive Controls:** Announcements, focus requests
- **Self-Monitoring:** Optional HR emotion tracking

### Server Capabilities
- **AI Processing:** Face detection + emotion analysis
- **Real-Time Sync:** WebSocket communication
- **Data Management:** Emotion history and analytics
- **Scalability:** Support multiple rooms/teams

## 🔒 Security & Privacy

### Data Protection
- **No Video Storage:** Live processing only
- **Encrypted Transmission:** WebSocket security
- **Local Processing:** Employee cameras stay private
- **Aggregated Analytics:** Individual privacy preserved

### Network Security
- **Firewall Configuration:** Open only port 5000
- **IP Restrictions:** Limit server access (optional)
- **VPN Recommended:** For remote access
- **HTTPS Support:** For production deployment

## 🛠️ Troubleshooting

### Server Issues
```
❌ "Port 5000 already in use"
✅ Kill existing process or change port

❌ "Model file not found"
✅ Download yolov8n-face.pt and update path

❌ "Cannot bind to address"
✅ Check firewall and network settings
```

### Client Connection Issues
```
❌ "Cannot connect to server"
✅ Verify server IP and port
✅ Check network connectivity
✅ Ensure server is running

❌ "Camera permission denied"
✅ Allow camera access in browser
✅ Check camera not used by other apps

❌ "Room connection failed"
✅ Verify Room ID matches
✅ Check server logs for errors
```

### Performance Issues
```
❌ "Slow emotion detection"
✅ Check server CPU/RAM usage
✅ Reduce number of employees
✅ Optimize network connection

❌ "Browser lag"
✅ Close unnecessary tabs
✅ Update browser to latest
✅ Use Chrome for best performance
```

## 🚀 Production Deployment

### Advanced Server Setup
```bash
# Use Gunicorn for production
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 server:app

# Use nginx as reverse proxy
# Configure SSL certificates
# Set up monitoring and logging
```

### Enterprise Features
- **User Authentication:** Add login system
- **Role-Based Access:** Different permission levels
- **Audit Logging:** Track all activities
- **Data Export:** Analytics and reporting
- **API Integration:** Connect to HR systems

## 📊 Monitoring & Analytics

### Real-Time Metrics
- **Emotion Distribution:** Live charts and graphs
- **Room Statistics:** Connection counts and status
- **Individual Tracking:** Per-employee analytics
- **Trend Analysis:** Emotional patterns over time

### Data Export
- **Screenshot Reports:** Dashboard captures
- **CSV Export:** Raw emotion data
- **API Access:** Programmatic data retrieval
- **Integration:** Connect to business intelligence tools

## 🔄 Updates & Maintenance

### Version Management
- **Server Updates:** Deploy new server version
- **Client Updates:** Download latest HTML files
- **Compatibility:** Ensure version matching
- **Backup:** Preserve configuration and data

### Regular Maintenance
- **Log Rotation:** Manage server log files
- **Performance Monitoring:** Track system resources
- **Security Updates:** Apply latest patches
- **Data Cleanup:** Remove old emotion records

## 📞 Support & Documentation

### Documentation
- 📖 **Server README:** `emotion_server/README.md`
- 📖 **Employee Guide:** `emotion_employee_client/README.md`
- 📖 **HR Manual:** `emotion_hr_client/README.md`

### Getting Help
1. **Check component READMEs** for specific guidance
2. **Review troubleshooting sections** for common issues
3. **Check server logs** for technical errors
4. **Browser developer tools** for client-side issues

### Community Resources
- **GitHub Issues:** Report bugs and request features
- **Documentation Wiki:** Extended guides and tutorials
- **Community Forum:** Share experiences and solutions

---

## 🎉 Getting Started

1. **Set up the server** on one laptop
2. **Configure employees** to connect to server
3. **Launch HR dashboard** for monitoring
4. **Start emotional wellness tracking!**

**Transform your workplace with emotional intelligence! 💙**