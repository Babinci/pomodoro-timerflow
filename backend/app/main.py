# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from . import models
import os
import logging
from fastapi.responses import FileResponse

# Import routers
from .routers import auth, users, tasks, pomodoro_websocket

# Setup logging
logging.basicConfig(level=logging.INFO, filename="/app/logs/error.log", format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Directory for frontend static files
STATIC_DIR = "/app/app/frontend-build"  # Absolute path in container

models.Base.metadata.create_all(bind=engine)

# Main FastAPI app
app = FastAPI()

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(tasks.router, prefix="/api")
app.include_router(pomodoro_websocket.router, prefix="/api")

@app.get("/{path:path}")
async def serve_frontend(path: str):
    file_path = os.path.join(STATIC_DIR, path)
    logging.info(f"Requested path: {path}, Checking: {file_path}")
    if os.path.exists(file_path) and os.path.isfile(file_path):
        logging.info(f"Serving file: {file_path}")
        return FileResponse(file_path)
    index_path = os.path.join(STATIC_DIR, "index.html")
    logging.info(f"Falling back to: {index_path}")
    return FileResponse(index_path)