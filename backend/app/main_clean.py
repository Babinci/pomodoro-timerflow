# main_clean.py
"""
Clean implementation of the FastAPI application using Supabase for authentication and database operations.
This version does not rely on the SQLAlchemy models or database.
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from fastapi.responses import FileResponse

# Import Supabase client
from .supabase import supabase

# Setup logging
logging.basicConfig(level=logging.INFO, filename="/app/logs/error.log", format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Directory for frontend static files
STATIC_DIR = "/app/app/frontend-build"  # Absolute path in container

# Main FastAPI app
app = FastAPI(
    title="Pomodoro TimerFlow API",
    description="API for Pomodoro TimerFlow application using Supabase",
    version="2.0.0"
)

# Create app state for supabase client
app.state.supabase = supabase

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests to the API"""
    logger.info(f"Request: {request.method} {request.url.path}")
    try:
        response = await call_next(request)
        return response
    except Exception as e:
        logger.error(f"Request error: {str(e)}")
        raise

# Health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint to verify API is running"""
    try:
        # Test Supabase connection
        response = supabase.table("users").select("count", count="exact").execute()
        return {"status": "ok", "database": "connected", "user_count": response.count if hasattr(response, 'count') else 0}
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return {"status": "ok", "database": "error connecting", "error": str(e)}

# Static file serving
@app.get("/{path:path}")
async def serve_frontend(path: str):
    """Serve static files from the frontend build directory"""
    file_path = os.path.join(STATIC_DIR, path)
    logging.info(f"Requested path: {path}, Checking: {file_path}")
    if os.path.exists(file_path) and os.path.isfile(file_path):
        logging.info(f"Serving file: {file_path}")
        return FileResponse(file_path)
    index_path = os.path.join(STATIC_DIR, "index.html")
    logging.info(f"Falling back to: {index_path}")
    return FileResponse(index_path)