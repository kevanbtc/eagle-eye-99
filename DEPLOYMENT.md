# Production Deployment Guide

Complete guide for deploying Eagle Eye + OSS integrations to production.

## Architecture Overview

```
Internet
   │
   ├─→ Reverse Proxy (Nginx/Traefik)
   │        ├─→ apps/web (Next.js) :3000
   │        ├─→ services/api (FastAPI) :8000
   │        ├─→ n8n :5678
   │        └─→ Odoo :8069
   │
   ├─→ Integration Layer
   │        ├─→ odoo-connector :5002
   │        └─→ ifcopenshell :5001
   │
   └─→ Data Layer
            ├─→ PostgreSQL :5432 (internal)
            ├─→ MinIO :9000 (internal)
            └─→ Redis :6379 (internal)
```

## Prerequisites

- Linux server (Ubuntu 22.04 LTS recommended)
- Docker 24+ & Docker Compose v2
- Domain name with DNS configured
- SSL certificates (Let's Encrypt recommended)
- Minimum specs:
  - 8 CPU cores
  - 32GB RAM
  - 500GB SSD storage
  - 1Gbps network

## 1. Server Preparation

### 1.1 Install Docker

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Install Docker Compose
sudo apt install docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER
newgrp docker

# Verify installation
docker --version
docker compose version
```

### 1.2 Clone Repository

```bash
cd /opt
git clone https://github.com/your-org/eagle-eye.git
cd eagle-eye
```

### 1.3 Configure Environment

```bash
# Copy environment template
cp .env.example .env.production

# Edit production variables
nano .env.production
```

**Required variables:**

```bash
# Database
POSTGRES_PASSWORD=<strong-random-password>
POSTGRES_DB=eagle_production

# MinIO
MINIO_ROOT_USER=<random-user>
MINIO_ROOT_PASSWORD=<strong-random-password>

# Redis
REDIS_PASSWORD=<strong-random-password>

# API
API_SECRET_KEY=<random-256-bit-key>
API_CORS_ORIGINS=https://yourdomain.com

# n8n
N8N_ENCRYPTION_KEY=<random-256-bit-key>
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=<strong-password>

# Odoo (if using)
ODOO_ADMIN_PASSWORD=<strong-password>
ODOO_DB_PASSWORD=<strong-random-password>

# External integrations
ODOO_URL=http://odoo:8069
ODOO_DB=eagle_odoo_prod
EAGLE_API_URL=http://api:8000
```

**Generate random secrets:**

```bash
# API secret key (256-bit)
openssl rand -hex 32

# Database password
openssl rand -base64 32

# n8n encryption key
openssl rand -hex 32
```

## 2. Reverse Proxy Setup

### 2.1 Install Nginx

```bash
sudo apt install nginx certbot python3-certbot-nginx
```

### 2.2 Configure Nginx

Create `/etc/nginx/sites-available/eagle-eye`:

```nginx
# API Backend
upstream eagle_api {
    server localhost:8000;
}

# Next.js Frontend
upstream eagle_web {
    server localhost:3000;
}

# n8n Workflow Engine
upstream eagle_n8n {
    server localhost:5678;
}

# Odoo (if using)
upstream eagle_odoo {
    server localhost:8069;
}

# Main domain (Frontend)
server {
    listen 80;
    listen [::]:80;
    server_name yourdomain.com;

    # Let's Encrypt verification
    location /.well-known/acme-challenge/ {
        root /var/www/html;
    }

    location / {
        return 301 https://$server_name$request_uri;
    }
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-Frame-Options "SAMEORIGIN" always;

    # Next.js frontend
    location / {
        proxy_pass http://eagle_web;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# API Subdomain
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name api.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/api.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/api.yourdomain.com/privkey.pem;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;

    location / {
        proxy_pass http://eagle_api;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # File upload size
        client_max_body_size 100M;
    }
}

# n8n Subdomain (Internal only - use firewall)
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name n8n.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/n8n.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/n8n.yourdomain.com/privkey.pem;

    # Restrict to office IP
    allow 203.0.113.0/24;  # Replace with your office IP
    deny all;

    location / {
        proxy_pass http://eagle_n8n;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}

# Odoo Subdomain (if using)
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name odoo.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/odoo.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/odoo.yourdomain.com/privkey.pem;

    location / {
        proxy_pass http://eagle_odoo;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Odoo file upload size
        client_max_body_size 200M;
    }
}
```

### 2.3 Enable Site & Get SSL

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/eagle-eye /etc/nginx/sites-enabled/

# Test configuration
sudo nginx -t

# Get SSL certificates
sudo certbot --nginx -d yourdomain.com -d api.yourdomain.com -d n8n.yourdomain.com -d odoo.yourdomain.com

# Reload Nginx
sudo systemctl reload nginx
```

## 3. Deploy Eagle Eye

### 3.1 Start Core Services

```bash
cd /opt/eagle-eye

# Use production environment
export COMPOSE_FILE=infra/docker-compose.yml
export COMPOSE_PROJECT_NAME=eagle_production

# Pull images
docker compose pull

# Start services
docker compose up -d

# Check status
docker compose ps
```

### 3.2 Initialize Database

```bash
# Wait for PostgreSQL to be ready
sleep 10

# Run migrations
docker compose exec -T db psql -U eagle -d eagle_production < infra/db/schema.sql

# Seed initial data
docker compose exec -T db psql -U eagle -d eagle_production < infra/seeds/regional_factors.csv
docker compose exec -T db psql -U eagle -d eagle_production < infra/seeds/spec_tier_bundles.sql

# Seed trade base
docker compose exec api python /app/seed_tradebase.py
```

### 3.3 Verify Core Services

```bash
# Check API health
curl https://api.yourdomain.com/health

# Check logs
docker compose logs -f api parser rules pricing reports
```

## 4. Deploy Integrations

### 4.1 Odoo Integration

```bash
cd /opt/eagle-eye/integrations/odoo

# Start Odoo stack
docker-compose up -d

# Wait for Odoo to initialize (2-3 minutes)
sleep 180

# Configure Odoo
# - Browse to https://odoo.yourdomain.com
# - Create database: eagle_odoo_prod
# - Install Construction Estimator module
# - Configure Eagle Eye integration settings
```

### 4.2 IfcOpenShell Service

```bash
# Already running from main compose file
# Verify health
curl http://localhost:5001/health
```

### 4.3 Import n8n Workflows

```bash
# Browse to https://n8n.yourdomain.com
# Login with N8N_BASIC_AUTH credentials
# Import workflows from: workflows/n8n/*.json
# Configure credentials for Odoo/ERPNext
# Activate workflows
```

## 5. Security Hardening

### 5.1 Firewall Configuration

```bash
# Install UFW
sudo apt install ufw

# Default policies
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP/HTTPS
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Enable firewall
sudo ufw enable

# Check status
sudo ufw status verbose
```

### 5.2 Fail2Ban for SSH

```bash
# Install Fail2Ban
sudo apt install fail2ban

# Configure
sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
sudo nano /etc/fail2ban/jail.local

# Enable and start
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

### 5.3 Database Backups

Create `/opt/eagle-eye/scripts/backup-db.sh`:

```bash
#!/bin/bash
BACKUP_DIR=/opt/backups/eagle-eye
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p $BACKUP_DIR

# Backup PostgreSQL
docker exec eagle-db pg_dump -U eagle eagle_production | gzip > $BACKUP_DIR/db_$TIMESTAMP.sql.gz

# Backup MinIO data
docker exec eagle-minio mc mirror /data $BACKUP_DIR/minio_$TIMESTAMP/

# Retain last 7 days
find $BACKUP_DIR -name "db_*.sql.gz" -mtime +7 -delete
find $BACKUP_DIR -name "minio_*" -type d -mtime +7 -exec rm -rf {} +

echo "Backup completed: $TIMESTAMP"
```

Make executable and schedule:

```bash
chmod +x /opt/eagle-eye/scripts/backup-db.sh

# Add to crontab (daily at 2 AM)
(crontab -l ; echo "0 2 * * * /opt/eagle-eye/scripts/backup-db.sh") | crontab -
```

## 6. Monitoring

### 6.1 Docker Health Checks

Already configured in docker-compose.yml:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### 6.2 Log Aggregation

Install Promtail + Loki (optional):

```bash
# See: https://grafana.com/docs/loki/latest/installation/docker/
```

### 6.3 Uptime Monitoring

Configure external monitoring:

- **Uptime Robot**: https://uptimerobot.com
- **Pingdom**: https://www.pingdom.com
- **StatusCake**: https://www.statuscake.com

Monitor endpoints:

- https://yourdomain.com (200 OK)
- https://api.yourdomain.com/health (200 OK)
- https://n8n.yourdomain.com/healthz (200 OK)

## 7. Scaling

### 7.1 Horizontal Scaling (Multiple Servers)

Use Docker Swarm or Kubernetes:

```bash
# Initialize Swarm
docker swarm init

# Deploy stack
docker stack deploy -c infra/docker-compose.yml eagle
```

### 7.2 Database Scaling

PostgreSQL read replicas:

```yaml
# Add to docker-compose.yml
db-replica:
  image: postgres:16-alpine
  environment:
    POSTGRES_PRIMARY_HOST: db
    POSTGRES_REPLICA: "true"
```

### 7.3 Load Balancing

Use Nginx upstream with multiple backends:

```nginx
upstream eagle_api {
    server api-1:8000;
    server api-2:8000;
    server api-3:8000;
}
```

## 8. Updates & Maintenance

### 8.1 Update Procedure

```bash
cd /opt/eagle-eye

# Pull latest code
git pull origin main

# Backup database first!
./scripts/backup-db.sh

# Rebuild services
docker compose build

# Rolling update (zero downtime)
docker compose up -d --no-deps --build api
docker compose up -d --no-deps --build parser
docker compose up -d --no-deps --build rules
docker compose up -d --no-deps --build pricing
docker compose up -d --no-deps --build reports

# Verify health
curl https://api.yourdomain.com/health
```

### 8.2 Rollback

```bash
# Restore database
gunzip < /opt/backups/eagle-eye/db_YYYYMMDD_HHMMSS.sql.gz | \
  docker exec -i eagle-db psql -U eagle eagle_production

# Revert code
git checkout <previous-commit-hash>

# Rebuild
docker compose up -d --build
```

## 9. Troubleshooting

### Service won't start

```bash
# Check logs
docker compose logs <service-name>

# Check disk space
df -h

# Check memory
free -h

# Restart service
docker compose restart <service-name>
```

### Database connection errors

```bash
# Verify PostgreSQL is running
docker compose ps db

# Check connection from API
docker compose exec api psql postgresql://eagle:password@db:5432/eagle_production

# Reset database container
docker compose restart db
```

### Out of disk space

```bash
# Clean Docker system
docker system prune -a --volumes

# Clean old images
docker image prune -a

# Clean logs
truncate -s 0 /var/lib/docker/containers/*/*-json.log
```

## 10. Support

- **Documentation**: `/opt/eagle-eye/README.md`
- **API Docs**: https://api.yourdomain.com/docs
- **Integration Guide**: `integrations/QUICKSTART.md`
- **Support Email**: support@eagleeye.ai

---

## Checklist

Pre-deployment:

- [ ] Server provisioned with minimum specs
- [ ] Domain DNS configured
- [ ] SSL certificates obtained
- [ ] Environment variables configured
- [ ] Backup strategy planned

Deployment:

- [ ] Docker installed and configured
- [ ] Repository cloned to `/opt/eagle-eye`
- [ ] Reverse proxy (Nginx) configured
- [ ] Core services started
- [ ] Database initialized and seeded
- [ ] Integration services deployed
- [ ] n8n workflows imported

Post-deployment:

- [ ] Health checks passing
- [ ] Firewall configured
- [ ] Backups scheduled
- [ ] Monitoring configured
- [ ] Team trained on workflow
- [ ] Rollback procedure tested

---

**Production deployment complete!** 🎉

Access your deployment:

- **Frontend**: https://yourdomain.com
- **API**: https://api.yourdomain.com/docs
- **n8n**: https://n8n.yourdomain.com
- **Odoo**: https://odoo.yourdomain.com (if configured)
