# Stage 1: Build the React frontend
FROM node:14-alpine AS frontend-build
WORKDIR /app
COPY frontend-apps/web-app/package*.json ./
RUN npm install
COPY frontend-apps/web-app/ ./
ENV NODE_ENV=production
RUN npm run build

# Stage 2: Set up the FastAPI backend
FROM python:3.9-slim
WORKDIR /app
COPY backend/requirements.txt ./
RUN pip install -r requirements.txt
COPY backend/ ./
RUN mkdir -p /app/db
COPY --from=frontend-build /app/build ./app/frontend-build

EXPOSE 8003
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003"]