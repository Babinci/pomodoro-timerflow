# Stage 1: Build the React frontend
FROM node:16-alpine AS frontend-build
WORKDIR /app
COPY frontend-apps/web-app/package*.json ./
RUN npm install
COPY frontend-apps/web-app/ ./
ENV NODE_ENV=production
RUN npm run build

# Stage 2: Set up the FastAPI backend with Supabase
FROM python:3.9-slim
WORKDIR /app
COPY backend/requirements_supabase.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY backend/ ./
RUN mkdir -p /app/logs
COPY --from=frontend-build /app/build ./app/frontend-build

EXPOSE 8003
# Use the full Supabase implementation
CMD ["uvicorn", "app.main_supabase:app", "--host", "0.0.0.0", "--port", "8003"]