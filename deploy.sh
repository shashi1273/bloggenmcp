#!/bin/bash

# MCP Technical Blog Server Deployment Script
# This script automates the deployment process for the MCP blog server

set -e  # Exit on any error

echo "=========================================="
echo "MCP Technical Blog Server Deployment"
echo "=========================================="

# Configuration variables
SERVER_DIR="/opt/mcp-blog-server"
SERVICE_USER="mcp-blog"
SERVICE_NAME="mcp-blog-server"
PYTHON_VERSION="3.11"

# Function to print status messages
print_status() {
    echo "[INFO] $1"
}

print_error() {
    echo "[ERROR] $1" >&2
}

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   print_error "This script must be run as root for system-wide deployment"
   exit 1
fi

print_status "Starting MCP Blog Server deployment..."

# Update system packages
print_status "Updating system packages..."
apt-get update
apt-get upgrade -y

# Install Python and required system packages
print_status "Installing Python $PYTHON_VERSION and dependencies..."
apt-get install -y python$PYTHON_VERSION python$PYTHON_VERSION-venv python$PYTHON_VERSION-pip
apt-get install -y git curl wget build-essential

# Create service user
print_status "Creating service user: $SERVICE_USER"
if ! id "$SERVICE_USER" &>/dev/null; then
    useradd --system --shell /bin/bash --home-dir $SERVER_DIR --create-home $SERVICE_USER
    print_status "Service user created successfully"
else
    print_status "Service user already exists"
fi

# Create server directory
print_status "Setting up server directory: $SERVER_DIR"
mkdir -p $SERVER_DIR
chown $SERVICE_USER:$SERVICE_USER $SERVER_DIR

# Copy server files
print_status "Copying server files..."
if [ -d "./mcp-blog-server" ]; then
    cp -r ./mcp-blog-server/* $SERVER_DIR/
else
    print_error "Server source directory not found. Please run this script from the project root."
    exit 1
fi

# Set proper ownership
chown -R $SERVICE_USER:$SERVICE_USER $SERVER_DIR

# Create Python virtual environment
print_status "Creating Python virtual environment..."
sudo -u $SERVICE_USER python$PYTHON_VERSION -m venv $SERVER_DIR/venv

# Install Python dependencies
print_status "Installing Python dependencies..."
sudo -u $SERVICE_USER $SERVER_DIR/venv/bin/pip install --upgrade pip
sudo -u $SERVICE_USER $SERVER_DIR/venv/bin/pip install -r $SERVER_DIR/requirements.txt

# Create systemd service file
print_status "Creating systemd service..."
cat > /etc/systemd/system/$SERVICE_NAME.service << EOF
[Unit]
Description=MCP Technical Blog Server
After=network.target

[Service]
Type=simple
User=$SERVICE_USER
Group=$SERVICE_USER
WorkingDirectory=$SERVER_DIR
Environment=PATH=$SERVER_DIR/venv/bin
ExecStart=$SERVER_DIR/venv/bin/python server.py
Restart=always
RestartSec=10

# Security settings
NoNewPrivileges=true
PrivateTmp=true
ProtectSystem=strict
ProtectHome=true
ReadWritePaths=$SERVER_DIR

[Install]
WantedBy=multi-user.target
EOF

# Create log directory
print_status "Setting up logging..."
mkdir -p /var/log/$SERVICE_NAME
chown $SERVICE_USER:$SERVICE_USER /var/log/$SERVICE_NAME

# Create configuration directory
print_status "Setting up configuration..."
mkdir -p /etc/$SERVICE_NAME
chown $SERVICE_USER:$SERVICE_USER /etc/$SERVICE_NAME

# Create default configuration file
cat > /etc/$SERVICE_NAME/config.json << EOF
{
    "server": {
        "name": "mcp-blog-server",
        "version": "1.0.0",
        "log_level": "INFO",
        "log_file": "/var/log/$SERVICE_NAME/server.log"
    },
    "business_rules": {
        "title": {
            "min_length": 40,
            "max_length": 80
        },
        "introduction": {
            "min_words": 150,
            "max_words": 300
        },
        "conclusion": {
            "min_words": 100,
            "max_words": 200
        }
    },
    "content_generation": {
        "default_audience": "intermediate",
        "default_length": "medium",
        "enable_seo_optimization": true
    }
}
EOF

chown $SERVICE_USER:$SERVICE_USER /etc/$SERVICE_NAME/config.json

# Run tests to verify installation
print_status "Running installation tests..."
sudo -u $SERVICE_USER $SERVER_DIR/venv/bin/python $SERVER_DIR/test_server.py

if [ $? -eq 0 ]; then
    print_status "Installation tests passed successfully"
else
    print_error "Installation tests failed. Please check the logs."
    exit 1
fi

# Enable and start the service
print_status "Enabling and starting the service..."
systemctl daemon-reload
systemctl enable $SERVICE_NAME
systemctl start $SERVICE_NAME

# Check service status
sleep 5
if systemctl is-active --quiet $SERVICE_NAME; then
    print_status "Service started successfully"
else
    print_error "Service failed to start. Check logs with: journalctl -u $SERVICE_NAME"
    exit 1
fi

# Create management scripts
print_status "Creating management scripts..."

# Start script
cat > /usr/local/bin/mcp-blog-start << 'EOF'
#!/bin/bash
systemctl start mcp-blog-server
echo "MCP Blog Server started"
EOF

# Stop script
cat > /usr/local/bin/mcp-blog-stop << 'EOF'
#!/bin/bash
systemctl stop mcp-blog-server
echo "MCP Blog Server stopped"
EOF

# Status script
cat > /usr/local/bin/mcp-blog-status << 'EOF'
#!/bin/bash
systemctl status mcp-blog-server
EOF

# Logs script
cat > /usr/local/bin/mcp-blog-logs << 'EOF'
#!/bin/bash
journalctl -u mcp-blog-server -f
EOF

# Make scripts executable
chmod +x /usr/local/bin/mcp-blog-*

# Create backup script
cat > /usr/local/bin/mcp-blog-backup << EOF
#!/bin/bash
BACKUP_DIR="/var/backups/mcp-blog-server"
DATE=\$(date +%Y%m%d_%H%M%S)
mkdir -p \$BACKUP_DIR
tar -czf \$BACKUP_DIR/mcp-blog-server_\$DATE.tar.gz -C $SERVER_DIR .
echo "Backup created: \$BACKUP_DIR/mcp-blog-server_\$DATE.tar.gz"
EOF

chmod +x /usr/local/bin/mcp-blog-backup

# Set up log rotation
cat > /etc/logrotate.d/$SERVICE_NAME << EOF
/var/log/$SERVICE_NAME/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 $SERVICE_USER $SERVICE_USER
    postrotate
        systemctl reload $SERVICE_NAME
    endscript
}
EOF

print_status "=========================================="
print_status "Deployment completed successfully!"
print_status "=========================================="
print_status ""
print_status "Service Status: $(systemctl is-active $SERVICE_NAME)"
print_status "Service Location: $SERVER_DIR"
print_status "Configuration: /etc/$SERVICE_NAME/config.json"
print_status "Logs: /var/log/$SERVICE_NAME/"
print_status ""
print_status "Management Commands:"
print_status "  Start:   mcp-blog-start"
print_status "  Stop:    mcp-blog-stop"
print_status "  Status:  mcp-blog-status"
print_status "  Logs:    mcp-blog-logs"
print_status "  Backup:  mcp-blog-backup"
print_status ""
print_status "To check service status: systemctl status $SERVICE_NAME"
print_status "To view logs: journalctl -u $SERVICE_NAME"
print_status ""
print_status "The MCP Blog Server is now ready for use!"

