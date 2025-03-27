@echo off
REM restart_docker.cmd for Windows CMD
docker stop pomodoro-app-container 2>NUL
docker rm pomodoro-app-container 2>NUL
docker build -t pomodoro-app .
if not exist logs mkdir logs

REM Run with only the necessary mounts for Supabase
docker run -d -p 8003:8003 ^
  -v %cd%\logs:/app/logs ^
  -v %cd%\backend\credentials\.env:/app/.env ^
  -e SUPABASE_URL=https://mysupabaseapi.cypher-arena.com/ ^
  -e SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZS1kZW1vIiwicm9sZSI6ImFub24iLCJleHAiOjE5ODM4MTI5OTZ9.CRXP1A7WOeoJeXxjNni43kdQwgnWNReilDMblYTn_I0 ^
  --name pomodoro-app-container pomodoro-app

REM Wait for container to start
echo Waiting for container to start...
ping -n 6 127.0.0.1 > nul

echo Container started with Supabase backend.
echo Check logs at ./logs/ directory for any issues.
