# Docker Setup Guide

This project is containerized using Docker and Docker Compose. The setup includes:

- **Backend**: FastAPI application
- **Frontend**: Flutter web application
- **Database**: MySQL 8.0
- **Mail Service**: MailHog (for development/testing)

## Prerequisites

- Docker Engine 20.10+
- Docker Compose 2.0+

## Quick Start

1. **Create environment file** (optional - defaults are provided):
   ```bash
   cp .env.example .env
   # Edit .env with your preferred values
   ```

2. **Build and start all services**:
   ```bash
   docker-compose up -d --build
   ```

3. **View logs**:
   ```bash
   docker-compose logs -f
   ```

4. **Stop all services**:
   ```bash
   docker-compose down
   ```

5. **Stop and remove volumes** (clears database data):
   ```bash
   docker-compose down -v
   ```

## Services

### Backend (FastAPI)
- **URL**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Port**: 8000
- **Container**: `rennefzo_backend`

### Frontend (Flutter Web)
- **URL**: http://localhost
- **Port**: 80
- **Container**: `rennefzo_frontend`

### Database (MySQL)
- **Host**: `db` (internal) or `localhost` (external)
- **Port**: 3306
- **Database**: `rennefzo` (default)
- **Root Password**: `password` (default)
- **User**: `rennefzo_user` (default)
- **Password**: `rennefzo_password` (default)
- **Container**: `rennefzo_db`

### Mail Service (MailHog)
- **SMTP Port**: 1025
- **Web UI**: http://localhost:8025
- **Container**: `rennefzo_mail`

## Environment Variables

Create a `.env` file in the root directory with the following variables (or use defaults):

```env
# Database Configuration
MYSQL_ROOT_PASSWORD=password
MYSQL_DATABASE=rennefzo
MYSQL_USER=rennefzo_user
MYSQL_PASSWORD=rennefzo_password

# Backend Configuration
SECRET_KEY=your-secret-key-change-this-in-production
BACKEND_CORS_ORIGINS=*
```

## Development

### Backend Development

For development with hot-reload, you can mount the backend directory:

```yaml
# Already configured in docker-compose.yml
volumes:
  - ./rennefzo_backend:/app
```

The backend will automatically reload when you make changes to Python files.

### Database Access

Connect to the database from your host machine:

```bash
mysql -h localhost -P 3306 -u rennefzo_user -prennefzo_password rennefzo
```

Or use any MySQL client with:
- Host: `localhost`
- Port: `3306`
- User: `rennefzo_user`
- Password: `rennefzo_password`
- Database: `rennefzo`

### Mail Testing

All emails sent by the application will be captured by MailHog. View them at:
http://localhost:8025

Configure your backend to use MailHog SMTP:
- SMTP Host: `mail` (service name in docker-compose)
- SMTP Port: `1025`
- No authentication required

## Troubleshooting

### Check service status:
```bash
docker-compose ps
```

### View logs for a specific service:
```bash
docker-compose logs backend
docker-compose logs frontend
docker-compose logs db
docker-compose logs mail
```

### Restart a specific service:
```bash
docker-compose restart backend
```

### Rebuild a specific service:
```bash
docker-compose up -d --build backend
```

### Database connection issues:
- Ensure the database service is healthy: `docker-compose ps`
- Check database logs: `docker-compose logs db`
- Verify DATABASE_URL in backend environment matches docker-compose settings

### Frontend not updating:
- Rebuild the frontend: `docker-compose up -d --build frontend`
- Clear browser cache

## Production Considerations

For production deployment:

1. **Change default passwords** in `.env`
2. **Set a strong SECRET_KEY**
3. **Restrict CORS origins** in `BACKEND_CORS_ORIGINS`
4. **Use a production mail service** (replace MailHog with real SMTP)
5. **Enable SSL/TLS** for frontend (use nginx with SSL certificates)
6. **Set up database backups**
7. **Use Docker secrets** for sensitive data
8. **Remove volume mounts** from backend in production
9. **Set appropriate resource limits** in docker-compose.yml

