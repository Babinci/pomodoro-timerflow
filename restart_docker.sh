#!/bin/bash
#  restart_docker.sh
docker stop pomodoro-app-container || true
docker rm pomodoro-app-container || true
docker build -t pomodoro-app .
mkdir -p logs
docker run -d -p 8003:8003 -v pomodoro-db:/app/db -v $(pwd)/logs:/app/logs -v $(pwd)/backend/credentials/.env:/app/.env --name pomodoro-app-container pomodoro-app