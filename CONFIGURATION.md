# Open WebUI MCP Bridge Configuration Guide

## 🎯 Current Setup Status

✅ **Open WebUI**: Running at http://localhost:3000 (Docker)  
✅ **MCP Bridge**: Active with 10 endpoints on ports 11001-11010  
✅ **MCP Dockmaster**: Running (PID: 20510)  
✅ **All MCP Servers**: 92 active processes detected

## 📋 Step-by-Step Open WebUI Configuration

### 1. Access Open WebUI Settings

1. Open **http://localhost:3000** in your browser
2. Sign in to your Open WebUI account
3. Click the **Settings** icon (⚙️) in the top right corner
4. Navigate to **Tools** in the left sidebar

### 2. Add MCP Tool Endpoints

For **Docker-based Open WebUI**, add these endpoints in **Settings > Tools**:

> **Important**: Since your Open WebUI is running in Docker and the MCP bridge is on the host, use `localhost` (not `host.docker.internal`) because the bridge is accessible from within the container.

#### 🖥️ System Automation Tools
```
Name: AppleScript Automation
URL: http://localhost:11001
Description: macOS system automation and app control
```

```
Name: Desktop Commander
URL: http://localhost:11008
Description: Desktop and system management
```

```
Name: Moom Window Manager
URL: http://localhost:11009
Description: Window management and layouts
```

#### 💻 Development Tools
```
Name: GitHub Integration
URL: http://localhost:11002
Description: GitHub repository and code management
```

```
Name: iTerm Terminal
URL: http://localhost:11007
Description: Terminal integration and command execution
```

```
Name: Playwright Browser
URL: http://localhost:11003
Description: Browser automation and web testing
```

#### 📝 Productivity Tools
```
Name: Notes Manager
URL: http://localhost:11004
Description: Note and document management
```

```
Name: TaskMaster AI
URL: http://localhost:11006
Description: AI-powered task management
```

#### 🎨 Media Tools
```
Name: Screenshot Capture
URL: http://localhost:11005
Description: Screen capture and image analysis
```

```
Name: Image Viewer
URL: http://localhost:11010
Description: Image processing and viewing
```

### 3. Test Your MCP Integration

After adding the endpoints, test them in a new conversation:

#### System Commands
```
Take a screenshot of my current desktop
```

#### Note Management
```
Create a new note about today's meeting agenda
```

#### GitHub Operations
```
Show me my GitHub repositories
```

#### Window Management
```
Use Moom to create a 2x2 window layout with my current applications
```

## 🧪 Verification & Testing

### Check MCP Bridge Status
```bash
# Test main endpoints
curl http://localhost:11001/health  # AppleScript
curl http://localhost:11002/health  # GitHub
curl http://localhost:11003/health  # Playwright
curl http://localhost:11004/health  # Notes
curl http://localhost:11005/health  # Screenshot
```

### Expected Response
```json
{
  "server": "applescript",
  "status": "ok", 
  "description": "macOS system automation and app control",
  "category": "system"
}
```

### Test Docker Network Access
```bash
# Verify Open WebUI can reach MCP endpoints
docker exec open-webui curl -s http://localhost:11001/health
```

## 🛠️ Available MCP Tools Summary

| Port | Tool | Category | Key Capabilities |
|------|------|----------|------------------|
| 11001 | **AppleScript** | System | Automate macOS apps, system controls, Finder operations |
| 11002 | **GitHub** | Development | Repository management, file operations, issue tracking |
| 11003 | **Playwright** | Automation | Browser automation, web scraping, UI testing |
| 11004 | **Notes** | Productivity | Note creation, document management, text processing |
| 11005 | **Screenshot** | Media | Screen capture, region selection, image analysis |
| 11006 | **TaskMaster** | Productivity | AI task management, project planning, workflows |
| 11007 | **iTerm** | Development | Terminal commands, shell integration, process management |
| 11008 | **Desktop Commander** | System | File operations, system management, process control |
| 11009 | **Moom** | System | Window layouts, workspace management, display configuration |
| 11010 | **Image Viewer** | Media | Image processing, file viewing, format conversion |

## 🔧 Troubleshooting

### Issue: Tools Not Appearing in Open WebUI
**Solution:**
1. Verify MCP bridge is running: `curl http://localhost:11001/health`
2. Check Docker network: `docker exec open-webui curl http://localhost:11001/health`
3. Restart Open WebUI if needed: `docker restart open-webui`

### Issue: "Connection Refused" Errors
**Solution:**
1. Ensure all MCP servers are running: `ps aux | grep mcp`
2. Check MCP Dockmaster status: `ps aux | grep mcp-proxy-server`
3. Restart MCP bridge if needed: `cd ~/Desktop/mcp-openwebui-bridge && ./setup-mcp-bridge.sh`

### Issue: Tool Execution Fails
**Solution:**
1. Check individual tool health: `curl http://localhost:1100X/health`
2. Verify permissions (especially for AppleScript)
3. Test tools individually before using in conversations

## 🚀 Usage Examples

### System Automation
```
"Use AppleScript to open Finder and create a new folder on my Desktop called 'Project Files'"
```

### Development Workflow
```
"Use GitHub to show me the README file from my latest repository"
```

### Productivity
```
"Take a screenshot of my current work and create a note summarizing what I'm working on"
```

### Window Management
```
"Use Moom to organize my windows: put Terminal on the left half and VS Code on the right half"
```

## 📁 Configuration Files Location

All configuration files are stored in:
```
~/Desktop/mcp-openwebui-bridge/
├── setup-mcp-bridge.sh
├── mcp-openwebui-bridge-config.txt
├── mcp-bridge-config.json
└── dockmaster-http-config.json
```

## 🔄 Maintenance

### Restart MCP Bridge
```bash
cd ~/Desktop/mcp-openwebui-bridge
./setup-mcp-bridge.sh
```

### Restart Open WebUI
```bash
docker restart open-webui
```

### Check System Status
```bash
# Check Docker container
docker ps | grep open-webui

# Check MCP processes
ps aux | grep mcp | wc -l

# Test endpoints
for port in {11001..11010}; do
  echo "Testing port $port:"
  curl -s http://localhost:$port/health | jq -r '.server + ": " + .status'
done
```

---

**🎉 Your Open WebUI is now fully integrated with MCP tools!**

Start a conversation and try: *"Take a screenshot and save it to my notes with today's date"*
