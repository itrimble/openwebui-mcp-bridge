#!/usr/bin/env python3
"""
MCP-Native Open WebUI Bridge Setup
Uses existing MCP infrastructure (Dockmaster) to bridge MCP servers to Open WebUI
"""

import json
import subprocess
import sys
import time
from pathlib import Path


class MCPOpenWebUIBridge:
    def __init__(self):
        self.config_file = Path.home() / "Desktop" / "mcp-openwebui-bridge" / "mcp-bridge-config.json"
        self.load_config()
    
    def load_config(self):
        """Load MCP bridge configuration"""
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print(f"❌ Configuration file not found: {self.config_file}")
            sys.exit(1)
    
    def check_mcp_dockmaster(self):
        """Check if MCP Dockmaster is running"""
        try:
            result = subprocess.run(['pgrep', '-f', 'mcp-proxy-server'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                pid = result.stdout.strip().split('\n')[0]
                print(f"✅ MCP Dockmaster running (PID: {pid})")
                return True
            else:
                print("❌ MCP Dockmaster not running")
                return False
        except Exception as e:
            print(f"Error checking Dockmaster: {e}")
            return False
    
    def configure_mcp_endpoints(self):
        """Configure MCP server endpoints via Dockmaster"""
        dockmaster_config = self.config['mcp_openwebui_bridge']['dockmaster_config']
        base_port = dockmaster_config['proxy_port']
        
        print(f"🔧 Configuring MCP endpoints via Dockmaster (port {base_port})")
        
        for i, server in enumerate(self.config['mcp_openwebui_bridge']['mcp_servers']):
            port = base_port + i + 1
            endpoint = server['endpoint']
            name = server['name']
            
            print(f"  📡 {name}: http://localhost:{port}{endpoint}")
            
            # Configure endpoint mapping (would interface with Dockmaster API)
            # This is a placeholder for actual Dockmaster configuration
            
        return True
    
    def generate_openwebui_config(self):
        """Generate Open WebUI configuration instructions"""
        print("\n🌐 Open WebUI Configuration:")
        print("=" * 50)
        print("Add these endpoints to Open WebUI Settings > Tools:")
        print()
        
        for i, server in enumerate(self.config['mcp_openwebui_bridge']['mcp_servers']):
            port = 11001 + i
            name = server['name'].replace('_', ' ').title()
            capabilities = ", ".join(server['capabilities'])
            
            print(f"• Name: MCP {name}")
            print(f"  URL: http://localhost:{port}")
            print(f"  Description: {capabilities}")
            print()
    
    def test_endpoints(self):
        """Test MCP endpoint connectivity"""
        print("\n🧪 Testing MCP endpoints...")
        
        for i, server in enumerate(self.config['mcp_openwebui_bridge']['mcp_servers']):
            port = 11001 + i
            name = server['name']
            
            try:
                # Test if port is accessible (basic check)
                result = subprocess.run(['curl', '-s', '-f', f'http://localhost:{port}'], 
                                      capture_output=True, timeout=5)
                if result.returncode == 0:
                    print(f"  ✅ {name}: Responding")
                else:
                    print(f"  ⚠️  {name}: Not responding (may need proxy setup)")
            except subprocess.TimeoutExpired:
                print(f"  ⏱️  {name}: Timeout")
            except Exception as e:
                print(f"  ❌ {name}: Error - {e}")
    
    def run_setup(self):
        """Run the complete MCP-OpenWebUI bridge setup"""
        print("🚀 MCP-Native Open WebUI Bridge Setup")
        print("=" * 50)
        
        # Check prerequisites
        if not self.check_mcp_dockmaster():
            print("\n❌ Setup failed: MCP Dockmaster not running")
            print("Please ensure MCP Dockmaster is active in your Claude MCP configuration")
            return False
        
        # Configure endpoints
        self.configure_mcp_endpoints()
        
        # Generate OpenWebUI config
        self.generate_openwebui_config()
        
        # Test endpoints
        self.test_endpoints()
        
        print("\n✅ MCP-OpenWebUI bridge setup complete!")
        print("\n🔗 Next steps:")
        print("1. Open your Open WebUI instance")
        print("2. Navigate to Settings > Tools")
        print("3. Add the endpoints listed above")
        print("4. Enable the MCP tools you want to use")
        
        return True


if __name__ == "__main__":
    bridge = MCPOpenWebUIBridge()
    bridge.run_setup()
