# Securing Containers
Final lab for the "Container Security" specialization

## Architecture

This project consists of three hardened security containers:

* **Frontend** - Nginx serving static files with security headers
* **API Layer** - FastAPI with JWT authentication and password validation
* **Database** - PostgreSQL with health checks and non-root user

***Note: The code to test the code without using the images on docker Hub is on the 'images' folder***

## Prerequisites

- Docker and Docker Compose installed
- Git (to clone the repository)
- Port 8080 available on your system

## Setup Instructions

### 1. Clone the Repository
```bash
git clone git@github.com:LuDorado/docker-security.git
cd docker-security
```

### 2. Configure Environment Variables
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with secure values
nano .env
```

**Required environment variables:**
```bash
POSTGRES_USER=app
POSTGRES_PASSWORD=your_secure_password_here
POSTGRES_DB=appdb
DB_HOST=db
DB_USER=app
DB_PASSWORD=your_secure_password_here
DB_NAME=appdb
JWT_SECRET=your_super_secret_jwt_key_32_chars_min
JWT_EXPIRE_MINUTES=30
```

### 3. Run with Pre-built Images (Docker Hub)
```bash
# Pull and start all services using Docker Hub images
docker compose -f docker-compose.yaml up -d

# Check status
docker compose -f docker-compose.yaml ps
```

### 3. Alternative: Build Locally
```bash
# Build all containers locally
docker compose build

# Start all services
docker compose up -d

# Check status
docker compose ps
```

### 4. Access the Application
- **Frontend**: http://localhost:8080
- **API Health**: http://localhost:8080/health

## Usage

### User Registration
1. Go to http://localhost:8080
2. Click "Register"
3. Create a user with the following password requirements:
   - Minimum 10 characters
   - 1 lowercase letter
   - 1 uppercase letter
   - 1 number
   - 1 symbol

### User Login
1. Click "Login"
2. Enter your credentials
3. Access the protected area

## Management Commands

### View Logs
```bash
# All services (Docker Hub images)
docker compose -f docker-compose.yaml logs

# All services (local build)
docker compose logs

# Specific service
docker compose logs frontend
```

### Database Access
```bash
# Connect to database
docker compose exec db psql -U app -d appdb

# View users table to validate proper user's registration
docker compose exec db psql -U app -d appdb -c "SELECT * FROM users;"
```

### Stop Services
```bash
# Stop all services (Docker Hub)
docker compose -f docker-compose.yaml down

# Stop all services (local build)
docker compose down

# Stop and remove volumes
docker compose down -v
```

## Security Features

- **Non-root users** in all containers
- **Environment variables** for sensitive data
- **Health checks** for service monitoring
- **Security headers** in nginx
- **JWT authentication** with secure secrets
- **Password validation** with complexity requirements
- **Database isolation** (not exposed to host)
- **Minimal attack surface** with Alpine Linux

## Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Check what's using port 8080
sudo netstat -tulpn | grep 8080
# Kill the process or change port in docker-compose.yaml
```

**Permission denied:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Logout and login again
```

**Build failures:**
```bash
# Clean build cache
docker system prune -a
# Rebuild without cache
docker compose build --no-cache
```

**Database connection issues:**
```bash
# Check database health
docker compose exec db pg_isready -U app -d appdb
# View database logs
docker compose logs db
```
