@echo off
REM restart_docker.cmd for Windows CMD
docker stop pomodoro-app-container 2>NUL
docker rm pomodoro-app-container 2>NUL
docker build -t pomodoro-app .
if not exist logs mkdir logs

REM Run with the .env file from the project root mounted to /app/.env
docker run -d -p 8003:8003 ^
  -v %cd%\logs:/app/logs ^
  -v %cd%\.env:/app/.env ^
  --name pomodoro-app-container pomodoro-app

REM Wait for container to start
echo Waiting for container to start...
ping -n 6 127.0.0.1 > nul

echo Container started with Supabase backend.
echo Check logs at ./logs/ directory for any issues.
