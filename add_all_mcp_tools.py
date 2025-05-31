#!/usr/bin/env python3
"""
OpenWebUI MCP Tools Auto-Configuration Script
Automatically adds all available MCP endpoints to OpenWebUI
"""

import sqlite3
import json
import sys
from datetime import datetime

# MCP tool configuration mapping
MCP_TOOLS = {
    11001: {"name": "MCP AppleScript", "description": "macOS system automation and app control via AppleScript"},
    11002: {"name": "MCP GitHub", "description": "GitHub repository and code management"},
    11003: {"name": "MCP Playwright", "description": "Browser automation and web testing"},
    11004: {"name": "MCP Notes", "description": "Note and document management"},
    11005: {"name": "MCP Screenshot", "description": "Screen capture and image analysis"},
    11006: {"name": "MCP TaskMaster", "description": "AI-powered task management"},
    11007: {"name": "MCP iTerm", "description": "Terminal integration and command execution"},
    11008: {"name": "MCP Desktop Commander", "description": "Desktop and system management"},
    11009: {"name": "MCP Moom", "description": "Window management and layouts"},
    11010: {"name": "MCP Image Viewer", "description": "Image processing and viewing"}
}

def get_current_config(db_path):
    """Get current OpenWebUI configuration from database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('SELECT data FROM config WHERE id = 1')
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return json.loads(result[0])
        else:
            print("❌ No configuration found in database")
            return None
    except Exception as e:
        print(f"❌ Error reading database: {e}")
        return None

def update_config(db_path, new_config):
    """Update OpenWebUI configuration in database"""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Update the configuration
        cursor.execute(
            'UPDATE config SET data = ?, updated_at = ? WHERE id = 1',
            (json.dumps(new_config), datetime.now().isoformat())
        )
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Error updating database: {e}")
        return False

def create_tool_config(port, tool_info):
    """Create tool configuration object"""
    return {
        "url": f"http://localhost:{port}",
        "path": "openapi.json",
        "auth_type": "bearer",
        "key": "",
        "config": {
            "enable": True,
            "access_control": {
                "read": {
                    "group_ids": [],
                    "user_ids": []
                },
                "write": {
                    "group_ids": [],
                    "user_ids": []
                }
            }
        },
        "info": {
            "name": tool_info["name"],
            "description": tool_info["description"]
        }
    }

def main():
    """Main configuration update function"""
    print("🚀 OpenWebUI MCP Tools Auto-Configuration")
    print("==========================================")
    
    # Database path inside Docker container
    db_path = "/app/backend/data/webui.db"
    
    # Get current configuration
    print("📖 Reading current configuration...")
    config = get_current_config(db_path)
    if not config:
        return False
    
    # Initialize tool_server section if it doesn't exist
    if 'tool_server' not in config:
        config['tool_server'] = {'connections': []}
    
    if 'connections' not in config['tool_server']:
        config['tool_server']['connections'] = []
    
    # Get existing tool URLs to avoid duplicates
    existing_urls = {conn['url'] for conn in config['tool_server']['connections']}
    
    print(f"📋 Found {len(existing_urls)} existing tool(s)")
    
    # Add new MCP tools
    added_count = 0
    for port, tool_info in MCP_TOOLS.items():
        tool_url = f"http://localhost:{port}"
        
        if tool_url not in existing_urls:
            print(f"➕ Adding {tool_info['name']} ({tool_url})")
            tool_config = create_tool_config(port, tool_info)
            config['tool_server']['connections'].append(tool_config)
            added_count += 1
        else:
            print(f"⏭️  Skipping {tool_info['name']} (already configured)")
    
    if added_count == 0:
        print("✅ All MCP tools are already configured!")
        return True
    
    # Update configuration in database
    print(f"💾 Updating configuration with {added_count} new tool(s)...")
    if update_config(db_path, config):
        print("✅ Configuration updated successfully!")
        print(f"🎉 Total configured tools: {len(config['tool_server']['connections'])}")
        
        # Display configured tools
        print("\n📋 All Configured MCP Tools:")
        for i, conn in enumerate(config['tool_server']['connections'], 1):
            status = "✅ ENABLED" if conn['config']['enable'] else "❌ DISABLED"
            print(f"   {i:2d}. {conn['info']['name']} ({conn['url']}) - {status}")
        
        print("\n🔄 Please restart OpenWebUI for changes to take effect:")
        print("   docker restart open-webui")
        
        return True
    else:
        print("❌ Failed to update configuration")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)