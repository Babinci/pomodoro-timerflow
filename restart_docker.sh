#!/bin/bash
#  restart_docker.sh
docker stop pomodoro-app-container || true
docker rm pomodoro-app-container || true
docker build -t pomodoro-app .
mkdir -p logs
mkdir -p db_local  # Ensure database directory exists

# Use bind mount for the database instead of volume
docker run -d -p 8003:8003 \
  -v $(pwd)/db_local:/app/db \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/backend/credentials/.env:/app/.env \
  --name pomodoro-app-container pomodoro-app

# Wait for container to start
echo "Waiting for container to start..."
sleep 5

# NOTE: We're not automatically applying migrations here anymore
# to match Django's workflow where you manually run migrate after making changes
echo "Container started. You can now run:"
echo "  ./backend/db_migrate.sh migrate"
echo "to apply any pending migrations"