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
try:
    from .routers import auth_supabase as auth_router
    from .routers import users_supabase as users_router
    from .routers import tasks_supabase as tasks_router
    from .routers import pomodoro_session_supabase as pomodoro_router
    from .routers import pomodoro_websocket as websocket_router
except ImportError:
    # Fallback to non-supabase routers
    from .routers import auth, users, tasks, pomodoro_websocket
    auth_router = auth
    users_router = users
    tasks_router = tasks
    websocket_router = pomodoro_websocket
    pomodoro_router = None

# Import Supabase client
from .supabase import supabase, get_diagnostics

# Setup logging
# First check if we're running in Docker (logs directory exists)
if os.path.exists("/app/logs"):
    log_file = "/app/logs/error.log"
else:
    # Create a logs directory in the current working directory
    os.makedirs("logs", exist_ok=True)
    log_file = "logs/error.log"

logging.basicConfig(
    level=logging.INFO,
    filename=log_file,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Directory for frontend static files
# Check if we're running in Docker
if os.path.exists("/app/app/frontend-build"):
    STATIC_DIR = "/app/app/frontend-build" 
else:
    # Try to find the frontend build directory relative to this file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    possible_paths = [
        os.path.join(current_dir, "..", "frontend-build"),
        os.path.join(current_dir, "..", "..", "frontend-apps", "web-app", "build")
    ]
    STATIC_DIR = next((path for path in possible_paths if os.path.exists(path)), None)
    if not STATIC_DIR:
        logger.warning("Frontend build directory not found. Static file serving may not work.")
        STATIC_DIR = "frontend-build"  # Fallback to a default

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
        diagnostics = get_diagnostics()
        return {
            "status": "success", 
            "config": diagnostics,
            "environment": {
                "SUPABASE_URL": os.getenv("SUPABASE_URL", "not set"),
                "ANON_KEY_LENGTH": len(os.getenv("ANON_KEY", "")) if os.getenv("ANON_KEY") else 0,
                "SERVICE_ROLE_KEY_LENGTH": len(os.getenv("SERVICE_ROLE_KEY", "")) if os.getenv("SERVICE_ROLE_KEY") else 0
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
        # Try to access a table in the pomodoro schema
        response = supabase.table("profiles").select("count", count="exact").limit(1).execute()
        table_exists = True
        count = response.count if hasattr(response, 'count') else 0
    except Exception as db_error:
        logger.error(f"Database health check error: {str(db_error)}")
        table_exists = False
        count = 0
        
    return {
        "status": "ok", 
        "service": "running", 
        "version": "2.0.0",
        "database": "connected" if table_exists else "connection error",
        "table_access": table_exists,
        "profile_count": count,
        "diagnostics": get_diagnostics()
    }

# Include routers
app.include_router(auth_router.router, prefix="/api")
app.include_router(users_router.router, prefix="/api")
app.include_router(tasks_router.router, prefix="/api")
if pomodoro_router:
    app.include_router(pomodoro_router.router, prefix="/api")
app.include_router(websocket_router.router, prefix="/api")

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
