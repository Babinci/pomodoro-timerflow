#!/bin/bash
#  restart_docker.sh
docker stop pomodoro-app-container || true
docker rm pomodoro-app-container || true
docker build -t pomodoro-app .
mkdir -p logs

# Run with the .env file from the project root
docker run -d -p 8003:8003 \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/.env:/app/.env \
  --name pomodoro-app-container pomodoro-app

# Wait for container to start
echo "Waiting for container to start..."
sleep 5

echo "Container started with Supabase backend."
echo "Check logs at ./logs/ directory for any issues."