# GCP Compute Engine Deployment Guide

## Overview
This guide is for deploying the backend on Google Compute Engine (VM instance), not Cloud Run. The frontend runs on Streamlit Cloud.

## Issues Fixed

### 1. **NetworkX Version Conflict**
- **Problem**: `networkx==3.5` doesn't exist
- **Solution**: Removed unnecessary dependencies, kept only essential packages

### 2. **Requirements Optimization**
- **Problem**: Too many dependencies causing conflicts
- **Solution**: Cleaned up requirements.txt with only essential packages

## Deployment Steps

### 1. **Create Compute Engine Instance**

```bash
# Create a VM instance
gcloud compute instances create ai-manager-backend \
  --zone=us-central1-a \
  --machine-type=e2-standard-4 \
  --image-family=debian-11 \
  --image-project=debian-cloud \
  --boot-disk-size=50GB \
  --tags=http-server,https-server

# Allow HTTP traffic
gcloud compute firewall-rules create allow-http \
  --allow tcp:8000 \
  --source-ranges 0.0.0.0/0 \
  --target-tags http-server
```

### 2. **Connect to Instance and Setup**

```bash
# SSH into your instance
gcloud compute ssh ai-manager-backend --zone=us-central1-a

# Update system
sudo apt-get update && sudo apt-get upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Logout and login again to apply docker group
exit
# SSH back in
gcloud compute ssh ai-manager-backend --zone=us-central1-a
```

### 3. **Deploy Application**

```bash
# Clone your repository
git clone <your-repo-url>
cd sse-aiManager/backend

# Create environment file
cp .env.example .env
# Edit .env with your production values

# Build and run Docker container
docker build -t ai-manager-backend .
docker run -d \
  --name ai-manager-backend \
  -p 8000:8000 \
  --restart unless-stopped \
  --env-file .env \
  ai-manager-backend
```

### 4. **Environment Variables**

Create `.env` file with:

```bash
OPENAI_API_KEY=your_openai_key
DJANGO_SECRET_KEY=your_secret_key
DEBUG=False
QDRANT_URL=your_qdrant_url
QDRANT_API_KEY=your_qdrant_key
ALLOWED_HOSTS=your-instance-ip,localhost,127.0.0.1
```

### 5. **Database Setup**

```bash
# Run migrations
docker exec ai-manager-backend python manage.py migrate

# Create superuser (optional)
docker exec -it ai-manager-backend python manage.py createsuperuser
```

### 6. **Health Check**

Add this to your `urls.py`:

```python
from django.http import JsonResponse

def health_check(request):
    return JsonResponse({"status": "healthy"})

urlpatterns = [
    # ... your existing URLs
    path('api/health/', health_check, name='health_check'),
]
```

## Configuration Files

### **requirements.txt** (Optimized)
- Removed conflicting versions
- Kept only essential dependencies
- Clean and production-ready

### **Dockerfile** (Compute Engine Optimized)
- Standard Docker setup
- Port 8000 exposed
- 3 Gunicorn workers for better performance
- File-based logging (appropriate for VMs)

### **logging.conf** (Server Ready)
- Uses file-based logging with rotation
- Appropriate for persistent server environments

## Monitoring and Management

### **View Logs**
```bash
# View application logs
docker logs ai-manager-backend

# View log files
docker exec ai-manager-backend tail -f logs/ai_manager.log
```

### **Restart Application**
```bash
docker restart ai-manager-backend
```

### **Update Application**
```bash
# Stop container
docker stop ai-manager-backend

# Remove old container
docker rm ai-manager-backend

# Pull latest code
git pull

# Rebuild and run
docker build -t ai-manager-backend .
docker run -d \
  --name ai-manager-backend \
  -p 8000:8000 \
  --restart unless-stopped \
  --env-file .env \
  ai-manager-backend
```

## Production Checklist

- [ ] Compute Engine instance created
- [ ] Docker installed and configured
- [ ] Environment variables set
- [ ] Application container running
- [ ] Database migrations run
- [ ] Health check endpoint working
- [ ] Firewall rules configured
- [ ] Logging configured properly
- [ ] CORS configured for Streamlit frontend

## Security Considerations

- **Firewall**: Only port 8000 is open
- **HTTPS**: Consider adding SSL certificate
- **Backup**: Set up regular backups of your data
- **Monitoring**: Use Cloud Monitoring for VM metrics

## Cost Optimization

- Use appropriate machine type (e2-standard-4 recommended)
- Monitor usage with Cloud Monitoring
- Consider using preemptible instances for development
- Set up auto-shutdown for non-production instances

## Troubleshooting

### **Container Not Starting**
```bash
# Check container logs
docker logs ai-manager-backend

# Check if port is in use
sudo netstat -tlnp | grep 8000
```

### **Database Issues**
```bash
# Check database connection
docker exec ai-manager-backend python manage.py dbshell
```

### **Memory Issues**
```bash
# Check memory usage
free -h

# Check Docker resource usage
docker stats ai-manager-backend
```

## Frontend Integration

Your Streamlit frontend should point to:
```
http://YOUR_INSTANCE_IP:8000
```

Replace `YOUR_INSTANCE_IP` with your Compute Engine instance's external IP address. 