# main_supabase.py
"""
Main FastAPI application using Supabase for authentication and database operations.
"""
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import logging
from fastapi.responses import FileResponse

# Import routers
from .routers import auth_supabase, users_supabase, tasks_supabase, pomodoro_session_supabase, pomodoro_websocket

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

# Make supabase client available to routes via app.state
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

# Basic health check endpoint
@app.get("/api/ping")
async def ping():
    """Simple ping endpoint to verify API is running"""
    return {"status": "ok", "service": "running", "version": "2.0.0"}

@app.get("/api/supabase-diagnostic")
async def supabase_diagnostic():
    """Diagnostic endpoint to check Supabase configuration"""
    try:
        from .supabase import get_diagnostics
        return {
            "status": "success", 
            "config": get_diagnostics(),
            "environment": {
                "SUPABASE_URL": os.getenv("SUPABASE_URL", "not set"),
                "SUPABASE_KEY": "***" + os.getenv("ANON_KEY", "not set")[-4:] if os.getenv("ANON_KEY") else "not set"
            }
        }
    except Exception as e:
        logger.error(f"Diagnostic failed: {str(e)}")
        return {"status": "error", "message": str(e)}

# Full health check endpoint
@app.get("/api/health")
async def health_check():
    """Health check endpoint to verify API is running with database connection"""
    try:
        # Try to see if the database is accessible
        # Use the profiles table we created instead of users
        response = supabase.table("profiles").select("count", count="exact").execute()
        return {
            "status": "ok", 
            "service": "running", 
            "version": "2.0.0",
            "database": "connected",
            "user_count": response.count if hasattr(response, 'count') else 0
        }
    except Exception as e:
        # RLS is not properly configured yet, but the service is running
        logger.error(f"Health check failed: {str(e)}")
        return {
            "status": "ok", 
            "service": "running", 
            "version": "2.0.0",
            "database": "configured but permissions not setup",
            "error": str(e)
        }

# Include routers
app.include_router(auth_supabase.router, prefix="/api")
app.include_router(users_supabase.router, prefix="/api")
app.include_router(tasks_supabase.router, prefix="/api")
app.include_router(pomodoro_session_supabase.router, prefix="/api")
app.include_router(pomodoro_websocket.router, prefix="/api")

# Static file serving (excluding API paths)
@app.get("/{path:path}")
async def serve_frontend(path: str, request: Request):
    """Serve static files from the frontend build directory"""
    # Skip API paths - they should be handled by other routes
    if path.startswith("api/"):
        raise HTTPException(status_code=404, detail="API endpoint not found")
        
    file_path = os.path.join(STATIC_DIR, path)
    logging.info(f"Requested path: {path}, Checking: {file_path}")
    if os.path.exists(file_path) and os.path.isfile(file_path):
        logging.info(f"Serving file: {file_path}")
        return FileResponse(file_path)
    index_path = os.path.join(STATIC_DIR, "index.html")
    logging.info(f"Falling back to: {index_path}")
    return FileResponse(index_path)
