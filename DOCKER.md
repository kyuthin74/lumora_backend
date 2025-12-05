# Docker Deployment Guide

## Quick Start with Docker

### Using Docker Compose (Recommended)

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

Access:
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- pgAdmin: http://localhost:5050

### Using Docker Only

```bash
# Build image
docker build -t lumora-backend .

# Run container
docker run -d -p 8000:8000 \
  -e DATABASE_URL=sqlite:///./lumora.db \
  -e SECRET_KEY=your-secret-key \
  --name lumora-api \
  lumora-backend

# View logs
docker logs -f lumora-api

# Stop container
docker stop lumora-api
```

## Production Deployment

### Environment Variables

Create a `.env` file:
```env
SECRET_KEY=your-production-secret-key
DATABASE_URL=postgresql://user:password@db:5432/lumora_db
SMTP_USER=your-email@domain.com
SMTP_PASSWORD=your-password
OPENAI_API_KEY=sk-your-key
```

### With PostgreSQL

```bash
# Start with production settings
docker-compose up -d

# Run migrations (if needed)
docker-compose exec api alembic upgrade head
```

### Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: lumora-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: lumora-api
  template:
    metadata:
      labels:
        app: lumora-api
    spec:
      containers:
      - name: api
        image: lumora-backend:latest
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: lumora-secrets
              key: database-url
```

## Cloud Deployment

### AWS ECS
```bash
# Build and push to ECR
docker build -t lumora-backend .
docker tag lumora-backend:latest <account>.dkr.ecr.<region>.amazonaws.com/lumora-backend:latest
docker push <account>.dkr.ecr.<region>.amazonaws.com/lumora-backend:latest
```

### Google Cloud Run
```bash
# Build and deploy
gcloud builds submit --tag gcr.io/PROJECT_ID/lumora-backend
gcloud run deploy --image gcr.io/PROJECT_ID/lumora-backend --platform managed
```

### Heroku
```bash
# Create app
heroku create lumora-backend

# Set environment variables
heroku config:set SECRET_KEY=your-key

# Deploy
heroku container:push web
heroku container:release web
```

## Health Checks

The Docker image includes health checks:
```bash
docker ps  # Check health status
```

## Scaling

```bash
# Scale to 3 instances
docker-compose up -d --scale api=3
```

## Monitoring

```bash
# View resource usage
docker stats

# View logs
docker-compose logs -f api
```

## Backup Database

```bash
# Backup PostgreSQL
docker-compose exec db pg_dump -U lumora lumora_db > backup.sql

# Restore
docker-compose exec -T db psql -U lumora lumora_db < backup.sql
```

## Troubleshooting

### Container won't start
```bash
docker-compose logs api
```

### Database connection issues
```bash
docker-compose exec api ping db
```

### Reset everything
```bash
docker-compose down -v
docker-compose up -d
```
