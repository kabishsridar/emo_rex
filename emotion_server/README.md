# 🖥️ Emotion HR Server

Central server component for the distributed Emotion HR monitoring system.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Webcam-enabled device (optional, for HR monitoring)
- Open port 5000 in firewall

### Installation

1. **Navigate to server directory:**
   ```bash
   cd emotion_server
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Update model path (if needed):**
   Edit `emotion_tracking.py` and update the YOLO model path:
   ```python
   YOLO_MODEL_PATH = r"D:\\arun-pt2\\yolov8n-face.pt"
   ```

### Running the Server

```bash
python server.py
```

The server will start on `http://0.0.0.0:5000` and accept connections from any IP.

## 🌐 Network Configuration

### For Local Network (Recommended)
- Server IP: `192.168.1.xxx` (your local IP)
- Clients connect using: `http://192.168.1.xxx:5000`

### For Internet Access
- Port forward port 5000 to your server
- Clients connect using: `http://your-public-ip:5000`
- **Security Note:** Use HTTPS and authentication for production

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

Look for your local network IP (usually 192.168.x.x or 10.x.x.x).

## 🔧 Configuration

Edit `config.py` to customize:

```python
SERVER_HOST = '0.0.0.0'        # Listen on all interfaces
SERVER_PORT = 5000             # Server port
DEBUG_MODE = False             # Debug mode
YOLO_MODEL_PATH = r"path\to\model"  # Model location
```

## 📊 Server Features

### Real-time Processing
- Face detection using YOLOv8
- Emotion analysis using DeepFace
- WebSocket communication
- Room-based organization

### Web Interface
- Landing page at `/`
- Employee interface at `/employee`
- HR interface at `/hr`
- API status at `/api/status`

### Multi-client Support
- Multiple employees per room
- Multiple HR staff monitoring
- Real-time synchronization

## 🔒 Security Considerations

### Development Setup
- CORS enabled for all origins
- No authentication required
- Suitable for local network testing

### Production Deployment
- Restrict CORS to specific IPs
- Add user authentication
- Use HTTPS (SSL/TLS)
- Implement rate limiting
- Use reverse proxy (nginx)

## 📈 Monitoring & Logs

The server provides real-time logs:
- Client connections/disconnections
- Room joins/leaves
- Emotion processing status
- Error handling

## 🛠️ Troubleshooting

### Common Issues

**Port Already in Use:**
```bash
# Find process using port 5000
netstat -ano | findstr :5000
# Kill the process
taskkill /PID <PID> /F
```

**Model Loading Errors:**
- Ensure `yolov8n-face.pt` exists at specified path
- Check file permissions
- Verify sufficient disk space

**Network Issues:**
- Check firewall settings
- Verify port 5000 is open
- Test connection: `telnet localhost 5000`

**CORS Errors:**
- Clients can't connect from different IPs
- Check server IP configuration
- Verify no firewall blocking connections

## 🔄 API Endpoints

- `GET /` - Landing page
- `GET /employee` - Employee interface
- `GET /hr` - HR dashboard
- `GET /api/status` - Server status

## 📋 System Requirements

- **CPU:** Multi-core recommended
- **RAM:** 4GB minimum, 8GB recommended
- **Storage:** 2GB for models and logs
- **Network:** Stable internet connection
- **OS:** Windows/Linux/Mac supported

## 🚀 Production Deployment

For production use, consider:

1. **Gunicorn for serving:**
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 server:app
   ```

2. **Nginx reverse proxy:**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;

       location / {
           proxy_pass http://127.0.0.1:5000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

3. **SSL Certificate** (Let's Encrypt recommended)

## 📞 Support

If you encounter issues:
1. Check server logs for error messages
2. Verify client configurations match server IP
3. Test basic connectivity between machines
4. Ensure all dependencies are installed correctly

---

**Server Status:** Ready to accept client connections! 🎯