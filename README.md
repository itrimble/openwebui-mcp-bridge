# Open WebUI MCP Bridge

**Native MCP-based integration for Open WebUI using existing Claude MCP servers**

## Overview

This repository provides a **pure MCP-based approach** to integrate your Claude MCP servers with Open WebUI, using your existing MCP infrastructure without external dependencies.

## Your Current MCP Infrastructure

Based on your active configuration, you have these MCP servers ready:

### 🤖 AI & Automation
- **applescript_execute**: Native macOS automation
- **taskmaster-ai**: AI-powered task management  
- **context7-mcp**: Context management
- **openmemory**: Memory management

### 🌐 Web & Browser
- **playwright**: Browser automation & testing
- **puppeteer**: Web scraping & control
- **github**: Repository management (this repo!)

### 💻 Development & System
- **desktop-commander**: Desktop management
- **iterm-mcp**: Terminal integration
- **wcgw**: Development workflow
- **notes**: Note management system
- **moom**: Window management

### 📸 Media & Content
- **screenshot**: Screen capture with OCR
- **screenpipe**: Screen recording & analysis
- **image-viewer**: Image processing
- **weather**: Weather data

## MCP-Native Bridge Architecture

### Core Components
1. **MCP Dockmaster** - Your existing HTTP proxy server
2. **MCP Router** - Multi-server management
3. **Native MCP Protocol** - Direct communication

### Integration Method

Instead of external proxy tools, we use your existing MCP infrastructure:

```
Claude MCP Servers → MCP Dockmaster → HTTP Endpoints → Open WebUI
```

## Setup Instructions

### 1. Verify MCP Infrastructure

Your MCP servers are already running:
- MCP Dockmaster: `PID 49706, 20510`
- MCP Router: `PID 793`
- Individual MCP servers: Active via Claude config

### 2. Configure MCP Dockmaster as Bridge

MCP Dockmaster provides HTTP proxy capabilities for your MCP servers.

### 3. Map MCP Endpoints

| MCP Server | Suggested Endpoint | Purpose |
|------------|-------------------|---------|
| applescript_execute | `/mcp/applescript` | macOS automation |
| github | `/mcp/github` | Repository ops |
| playwright | `/mcp/playwright` | Browser automation |
| notes | `/mcp/notes` | Note management |
| screenshot | `/mcp/screenshot` | Screen capture |

### 4. Open WebUI Configuration

Add MCP Dockmaster endpoints to Open WebUI:
- Base URL: `http://localhost:<dockmaster_port>`
- Endpoints: Use MCP server paths above

## Benefits of MCP-Native Approach

✅ **No External Dependencies** - Uses existing MCP infrastructure  
✅ **Unified Protocol** - Native MCP communication  
✅ **Centralized Management** - Via MCP Router/Dockmaster  
✅ **Consistent Configuration** - Same as Claude setup  
✅ **Real-time Updates** - Direct MCP protocol benefits  

## Repository Structure

```
openwebui-mcp-bridge/
├── README.md (this file)
├── mcp-config/ 
│   ├── dockmaster-config.json
│   ├── endpoint-mappings.json
│   └── openwebui-settings.json
├── scripts/
│   ├── verify-mcp-status.sh
│   ├── configure-endpoints.sh
│   └── test-integration.sh
└── docs/
    ├── setup-guide.md
    ├── troubleshooting.md
    └── mcp-architecture.md
```

## Next Steps

1. **Document current MCP configuration** using Notes MCP
2. **Configure endpoint mappings** via Desktop Commander
3. **Test integration** using Screenshot MCP for verification
4. **Automate setup** with AppleScript MCP

---

*Created and managed using native MCP tools: GitHub MCP, Notes MCP, AppleScript MCP*
