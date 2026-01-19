# Production Deployment Guide

## Prerequisites

- Python 3.9+
- pip
- systemd (for service management)
- nginx (for reverse proxy)
- SSL certificate (for HTTPS)

## Step 1: Prepare Environment

```bash
# Create application user
sudo useradd -m -s /bin/bash stickman

# Create directories
sudo mkdir -p /opt/stickman
sudo mkdir -p /var/log/stickman
sudo mkdir -p /etc/stickman

# Set permissions
sudo chown -R stickman:stickman /opt/stickman
sudo chown -R stickman:stickman /var/log/stickman
```

## Step 2: Deploy Application

```bash
# Copy application files
sudo cp -r . /opt/stickman/
cd /opt/stickman

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Copy configuration
sudo cp config.yml /etc/stickman/
sudo cp llm_config.example.yml /etc/stickman/llm_config.yml

# Edit configuration
sudo nano /etc/stickman/llm_config.yml
# Add your API keys
```

## Step 3: Configure Environment Variables

```bash
# Create production environment file
sudo cp .env.production /etc/stickman/.env

# Edit environment variables
sudo nano /etc/stickman/.env

# Generate secure secret key
python3 -c "import secrets; print(secrets.token_hex(32))"
# Update SECRET_KEY in .env

# Generate API key for your application
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
# Update API_KEY in .env
```

## Step 4: Create Systemd Service

```bash
# Create service file
sudo nano /etc/systemd/system/stickman.service
```

Add the following content:

```ini
[Unit]
Description=AI Stick Figure Story Animator
After=network.target

[Service]
Type=simple
User=stickman
Group=stickman
WorkingDirectory=/opt/stickman
Environment="PATH=/opt/stickman/venv/bin"
EnvironmentFile=/etc/stickman/.env
ExecStart=/opt/stickman/venv/bin/gunicorn \
    --bind 127.0.0.1:5000 \
    --workers 4 \
    --threads 2 \
    --timeout 120 \
    --access-logfile /var/log/stickman/access.log \
    --error-logfile /var/log/stickman/error.log \
    --log-level info \
    app:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Reload systemd
sudo systemctl daemon-reload

# Enable and start service
sudo systemctl enable stickman
sudo systemctl start stickman

# Check status
sudo systemctl status stickman
```

## Step 5: Configure Nginx Reverse Proxy

```bash
# Create nginx configuration
sudo nano /etc/nginx/sites-available/stickman
```

Add the following content:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # Security Headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    
    # Rate Limiting
    limit_req_zone $binary_remote_addr zone=api_limit:10m rate=20r/m;
    limit_req zone=api_limit burst=30 nodelay;
    
    # Client body size
    client_max_body_size 10M;
    
    # Timeouts
    proxy_connect_timeout 120s;
    proxy_send_timeout 120s;
    proxy_read_timeout 120s;
    
    # Proxy to Flask
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    # Static files (optional optimization)
    location /static {
        alias /opt/stickman/static;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
    
    # Health check endpoint (no rate limit)
    location /api/health {
        proxy_pass http://127.0.0.1:5000;
        access_log off;
    }
    
    # Access logs
    access_log /var/log/nginx/stickman_access.log;
    error_log /var/log/nginx/stickman_error.log;
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/stickman /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

## Step 6: SSL Certificate (Let's Encrypt)

```bash
# Install certbot
sudo apt install certbot python3-certbot-nginx

# Obtain certificate
sudo certbot --nginx -d your-domain.com

# Test auto-renewal
sudo certbot renew --dry-run
```

## Step 7: Monitoring & Maintenance

### Log Rotation

```bash
# Create logrotate configuration
sudo nano /etc/logrotate.d/stickman
```

Add:

```
/var/log/stickman/*.log {
    daily
    rotate 30
    compress
    delaycompress
    notifempty
    create 0640 stickman stickman
    sharedscripts
    postrotate
        systemctl reload stickman > /dev/null 2>&1 || true
    endscript
}
```

### Health Monitoring

```bash
# Create health check script
sudo nano /opt/stickman/health_check.sh
```

Add:

```bash
#!/bin/bash
response=$(curl -s http://127.0.0.1:5000/api/health)
status=$(echo $response | jq -r '.status')

if [ "$status" != "healthy" ]; then
    echo "Service unhealthy: $response"
    exit 1
fi

echo "Service healthy"
exit 0
```

```bash
# Make executable
sudo chmod +x /opt/stickman/health_check.sh

# Add to crontab for monitoring
sudo crontab -e
```

Add:

```
*/5 * * * * /opt/stickman/health_check.sh || systemctl restart stickman
```

### Performance Monitoring

```bash
# Check metrics
curl http://your-domain.com/api/metrics

# View logs
sudo journalctl -u stickman -f

# Check resource usage
htop
```

## Step 8: Firewall Configuration

```bash
# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status
```

## Step 9: Backup Strategy

```bash
# Create backup script
sudo nano /opt/stickman/backup.sh
```

Add:

```bash
#!/bin/bash
BACKUP_DIR="/var/backups/stickman"
DATE=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup configuration
tar -czf $BACKUP_DIR/config_$DATE.tar.gz /etc/stickman/

# Backup logs (last 7 days)
find /var/log/stickman -name "*.log" -mtime -7 -exec tar -czf $BACKUP_DIR/logs_$DATE.tar.gz {} +

# Keep only last 30 days of backups
find $BACKUP_DIR -name "*.tar.gz" -mtime +30 -delete
```

```bash
# Make executable
sudo chmod +x /opt/stickman/backup.sh

# Add to crontab
sudo crontab -e
```

Add:

```
0 2 * * * /opt/stickman/backup.sh
```

## Step 10: Security Hardening

### Application-Level Security

1. **API Key Protection**: Set strong API key in `/etc/stickman/.env`
2. **Secret Key**: Generate secure SECRET_KEY (32+ bytes)
3. **Input Validation**: All inputs are sanitized automatically
4. **Rate Limiting**: 20 requests/minute per IP (configured in nginx)

### System-Level Security

```bash
# Disable root SSH login
sudo nano /etc/ssh/sshd_config
# Set: PermitRootLogin no

# Reload SSH
sudo systemctl reload sshd

# Install fail2ban
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban

# Configure fail2ban for nginx
sudo nano /etc/fail2ban/jail.local
```

Add:

```ini
[nginx-limit-req]
enabled = true
filter = nginx-limit-req
logpath = /var/log/nginx/*error.log
maxretry = 5
bantime = 3600
```

## Troubleshooting

### Service won't start

```bash
# Check logs
sudo journalctl -u stickman -n 50

# Check environment
sudo -u stickman bash
source /opt/stickman/venv/bin/activate
cd /opt/stickman
python3 app.py
```

### High latency

```bash
# Check metrics
curl http://127.0.0.1:5000/api/metrics

# Check cache stats
# Increase cache size in .env if needed

# Scale workers
sudo nano /etc/systemd/system/stickman.service
# Increase --workers count
sudo systemctl daemon-reload
sudo systemctl restart stickman
```

### Memory issues

```bash
# Check memory usage
free -h

# Limit workers
# Edit /etc/systemd/system/stickman.service
# Reduce --workers count
```

## Performance Tuning

### Gunicorn Workers

```
workers = (2 * CPU_CORES) + 1
threads = 2-4
```

### Cache Tuning

Edit `/etc/stickman/.env`:

```
CACHE_MAX_SIZE=5000
CACHE_TTL_SECONDS=7200
```

### Database (if needed)

For production, consider adding Redis for caching:

```bash
sudo apt install redis-server
sudo systemctl enable redis-server
sudo systemctl start redis-server
```

Update `backend/cache_service.py` to use Redis instead of in-memory cache.

## Scaling

### Horizontal Scaling

1. Deploy multiple instances behind load balancer
2. Use external cache (Redis) for shared state
3. Use external session storage

### Vertical Scaling

1. Increase server resources (CPU, RAM)
2. Increase worker count
3. Optimize cache settings

## Monitoring & Alerting

Consider integrating:

- **Prometheus** + **Grafana**: Metrics visualization
- **Sentry**: Error tracking
- **ELK Stack**: Log aggregation
- **UptimeRobot**: Uptime monitoring

## Compliance & Legal

- **GDPR**: No user data is stored
- **Rate Limiting**: Prevents abuse
- **API Keys**: Controls access
- **Audit Logs**: All requests logged

## Support

For issues:
1. Check logs: `/var/log/stickman/`
2. Check metrics: `/api/metrics`
3. Check system resources: `htop`, `df -h`
4. Review security logs: `sudo journalctl -u stickman`
