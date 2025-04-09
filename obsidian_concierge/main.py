"""
Main application entry point.

This module initializes and configures the FastAPI application, sets up middleware,
and includes all API routes.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

from .utils.config import AppConfig, load_config
from .utils.logging import LogConfig, setup_logging
from .api.routes import router as api_router

# Load configuration
config = load_config()

# Setup logging
log_config = LogConfig(
    LOG_LEVEL=config.LOG_LEVEL,
    LOG_FILE=config.LOG_FILE
)
logger = setup_logging(log_config)

# Create FastAPI application
app = FastAPI(
    title="Obsidian Concierge",
    description="Knowledge management assistant for Obsidian users",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Configure this properly in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Mount static files
static_dir = Path(__file__).parent / "static"
static_dir.mkdir(parents=True, exist_ok=True)  # 静的ファイルディレクトリを作成
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# Root endpoint to serve index.html
@app.get("/")
async def root():
    """Serve the main application page."""
    index_path = static_dir / "index.html"
    if not index_path.exists():
        return {"message": "Welcome to Obsidian Concierge API"}
    return FileResponse(index_path)

def start():
    """Start the application server."""
    uvicorn.run(
        "obsidian_concierge.main:app",
        host=config.HOST,
        port=config.PORT,
        reload=True  # Enable auto-reload during development
    )

if __name__ == "__main__":
    start() 