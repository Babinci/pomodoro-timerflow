#!/bin/bash
#  restart_docker.sh
docker stop pomodoro-app-container || true
docker rm pomodoro-app-container || true
docker build -t pomodoro-app .
mkdir -p logs

# Use bind mount for the database instead of volume
docker run -d -p 8003:8003 \
  -v $(pwd)/db_local:/app/db \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/backend/credentials/.env:/app/.env \
  --name pomodoro-app-container pomodoro-app

# Wait for container to start
echo "Waiting for container to start..."
sleep 5

# Apply migrations automatically
echo "Applying database migrations..."
./backend/db_migrate.sh migrate