# 🎯 HR Emotion Client

Distributed HR dashboard for monitoring employee emotional wellness. Connects to the central Emotion HR server.

## 🚀 Quick Start

### Prerequisites
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Webcam-enabled device (optional, for HR self-monitoring)
- Network connection to Emotion HR server

### Setup

1. **Open the dashboard:**
   - Open `index.html` in your web browser
   - Or serve via local web server (optional)

2. **Connect to server:**
   - Enter the server's IP address
   - Enter the Room ID (same as employees use)
   - Enter your HR name
   - Click "Connect"

3. **Start monitoring:**
   - View employee feeds in real-time
   - Monitor emotion analytics
   - Use HR controls as needed

## 🔧 Configuration

### Server Connection
- **Server IP:** IP address of the machine running `emotion_server`
- **Port:** 5000 (default)
- **Room ID:** Shared identifier for your team/session

### Finding Server IP

Ask your IT admin or:

**If server is on same network:**
- Server typically runs on: `192.168.1.xxx`
- Check server logs for IP address

**If server is remote:**
- Use the public IP or domain
- May require VPN for secure access

## 🎯 Features

### Multi-Employee Monitoring
- Live video feeds from all connected employees
- Real-time emotion detection and display
- Employee status indicators
- Room-based organization

### HR Self-Monitoring
- Optional HR camera for personal emotion tracking
- Same detection algorithm as employees
- Fancy bounding boxes and emotion bars
- Screenshot capability

### Analytics Dashboard
- Real-time emotion statistics
- Interactive charts and graphs
- Room-wide emotion trends
- Employee count and status

### HR Controls
- Send announcements to all employees
- Request emotion focus from specific employees
- Private messaging capabilities
- Room management tools

## 🌐 Browser Requirements

### Supported Browsers
- ✅ Chrome 80+
- ✅ Firefox 75+
- ✅ Safari 13+
- ✅ Edge 80+

### Required Permissions
- **Camera Access:** Optional, for HR self-monitoring
- **WebRTC:** Enable for real-time communication
- **JavaScript:** Must be enabled

## 📊 Dashboard Overview

### Main Sections

1. **Connection Panel:**
   - Server IP input
   - Room ID management
   - Connection status

2. **HR Local Monitor:**
   - HR's own emotion detection
   - Camera controls (start/stop)
   - Screenshot functionality

3. **Employee Feeds:**
   - Grid of all connected employees
   - Live emotion overlays
   - Individual controls

4. **Analytics Panel:**
   - Real-time statistics
   - Emotion distribution charts
   - Room metrics

5. **HR Controls:**
   - Announcement system
   - Employee interaction tools

## 📱 Usage Guide

### Step-by-Step Setup

1. **Launch Dashboard:**
   ```bash
   # Option 1: Open directly in browser
   # Double-click index.html

   # Option 2: Serve locally (if needed)
   python -m http.server 8000
   # Then visit: http://localhost:8000
   ```

2. **Enter Connection Details:**
   - Server IP: `192.168.1.100` (example)
   - Room ID: `workplace-2026`
   - HR Name: `Sarah Johnson`

3. **Connect to Server:**
   - Click "Connect"
   - Wait for "Connected" status
   - Dashboard will populate with employee feeds

4. **Optional: Enable HR Camera:**
   - Click "Start Camera" for personal monitoring
   - Allow camera permissions
   - Your emotions will also be tracked

### Understanding Metrics

- **Total Clients:** All connected users (employees + HR)
- **Active Employees:** Number of monitored employees
- **Active HR:** Number of HR staff monitoring
- **Avg Emotion:** Most common emotion in the room

## 🔒 Privacy & Compliance

### Data Handling
- **Employee Privacy:** Only emotion data transmitted
- **No Video Storage:** Live processing only
- **Aggregated Analytics:** Individual data anonymized
- **Secure Transmission:** WebSocket encryption

### Compliance Features
- Transparent monitoring indicators
- Employee consent notifications
- Data retention policies
- Audit logging capabilities

## 🛠️ Troubleshooting

### Connection Issues

**"Cannot connect to server":**
- ✅ Verify server IP address
- ✅ Check if server is running (`http://server-ip:5000/api/status`)
- ✅ Test network connectivity
- ✅ Ensure firewall allows port 5000

**"No employee feeds showing":**
- ✅ Verify Room ID matches employee settings
- ✅ Check if employees are connected
- ✅ Refresh statistics manually

**"Charts not updating":**
- ✅ Check WebSocket connection
- ✅ Refresh browser page
- ✅ Verify server is processing data

### Performance Issues

**Slow dashboard loading:**
- Close unnecessary browser tabs
- Clear browser cache
- Use Chrome for best performance

**Laggy employee feeds:**
- Reduce number of concurrent employees
- Check server performance
- Optimize network connection

**Emotion detection lag:**
- Server processing overload
- Network latency issues
- Check server logs for errors

## 🎨 Customization

### Interface Themes
Customize the HR dashboard appearance:
- Edit CSS styles in `index.html`
- Change color schemes
- Add company branding
- Modify layout grid

### Default Settings
Modify default connection values:
```html
<input type="text" id="serverIP" value="192.168.1.100">
<input type="text" id="roomId" value="workplace-2026">
<input type="text" id="hrName" value="HR Manager">
```

## 📈 Analytics & Reporting

### Available Metrics
- **Emotion Distribution:** Pie chart of emotion types
- **Room Statistics:** Real-time counts and averages
- **Individual Tracking:** Per-employee emotion history
- **Trend Analysis:** Emotion changes over time

### Exporting Data
- Screenshot dashboard for reports
- Server-side data export (contact admin)
- Manual data collection from logs

## 🔧 Advanced Features

### HR Camera Controls
- **Start/Stop:** Control personal monitoring
- **Toggle Bars:** Show/hide emotion probability bars
- **Screenshot:** Capture current state
- **Real-time Overlay:** Same as employee interface

### Employee Management
- **Focus Requests:** Ask employees to pay attention
- **Announcements:** Broadcast messages to all
- **Individual Messages:** Private communications
- **Status Monitoring:** Track connection health

### Room Management
- **Multiple Rooms:** Monitor different teams
- **Room Switching:** Change monitoring focus
- **Access Control:** Room-based permissions

## 📊 System Requirements

### Minimum Requirements
- **Browser:** Modern web browser
- **CPU:** 3GHz dual-core
- **RAM:** 8GB
- **Network:** 10 Mbps internet
- **Display:** 1920x1080 resolution

### Recommended Requirements
- **Browser:** Chrome 90+
- **CPU:** 3GHz quad-core
- **RAM:** 16GB
- **Network:** 50 Mbps internet
- **Display:** 2560x1440 resolution

## 🔄 Updates & Maintenance

### Version Updates
- Download latest client files
- Replace `index.html` with updated version
- Clear browser cache
- Test all features after update

### Compatibility
- Ensure client version matches server
- Check browser compatibility
- Update WebSocket libraries if needed

## 📞 Support & Resources

### Getting Help
1. **Read this documentation** thoroughly
2. **Check server logs** for backend issues
3. **Browser developer tools** (F12) for client errors
4. **Contact IT admin** for network/server issues

### Common Issues & Solutions

**Dashboard not loading:**
```
✅ Check internet connection
✅ Verify server IP and port
✅ Clear browser cache
✅ Try different browser
```

**Employee feeds blank:**
```
✅ Confirm employees are connected
✅ Check room ID matching
✅ Verify server processing
✅ Refresh statistics
```

**Charts not displaying:**
```
✅ Enable JavaScript
✅ Update Chart.js library
✅ Check console for errors
✅ Refresh page
```

## 🚀 Integration Options

### Enterprise Features
- **LDAP Integration:** Company directory sync
- **API Access:** Custom dashboard integrations
- **Webhook Alerts:** Automated notifications
- **Reporting Tools:** Advanced analytics

### Custom Development
- **API Endpoints:** Server provides REST APIs
- **WebSocket Events:** Real-time data streaming
- **Custom Dashboards:** Build specialized interfaces
- **Mobile Apps:** Native mobile applications

---

**Empowering HR with emotional intelligence insights. 🎯**