#!/bin/bash

# OpenWebUI MCP Tools Auto-Configuration Script
# Automatically adds all MCP endpoints to OpenWebUI configuration

set -e

echo "🚀 OpenWebUI MCP Auto-Configuration"
echo "===================================="

# Check if OpenWebUI container is running
if ! docker ps | grep -q open-webui; then
    echo "❌ OpenWebUI container is not running!"
    echo "   Start it with: docker start open-webui"
    exit 1
fi

echo "✅ OpenWebUI container is running"

# Copy the Python script into the container
echo "📁 Copying configuration script to container..."
docker cp add_all_mcp_tools.py open-webui:/tmp/add_all_mcp_tools.py

# Execute the Python script inside the container
echo "🔧 Running auto-configuration script..."
docker exec open-webui python3 /tmp/add_all_mcp_tools.py

# Check the exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "🎉 SUCCESS! All MCP tools have been configured!"
    echo ""
    echo "🔄 Restarting OpenWebUI to apply changes..."
    docker restart open-webui
    
    echo "⏳ Waiting for OpenWebUI to start..."
    sleep 5
    
    # Wait for container to be healthy
    timeout=30
    counter=0
    while [ $counter -lt $timeout ]; do
        if docker ps | grep open-webui | grep -q "healthy"; then
            echo "✅ OpenWebUI is ready!"
            break
        fi
        echo "   Waiting for OpenWebUI to be healthy... ($counter/$timeout)"
        sleep 2
        counter=$((counter + 2))
    done
    
    echo ""
    echo "🌐 OpenWebUI URL: http://localhost:3000"
    echo "🛠️  Go to Settings > Tools to see all configured MCP endpoints"
    echo ""
    echo "🧪 Test with: 'Take a screenshot of my desktop'"
else
    echo "❌ Configuration failed!"
    exit 1
fi

# Cleanup
docker exec open-webui rm -f /tmp/add_all_mcp_tools.py

echo "✨ Configuration complete!"