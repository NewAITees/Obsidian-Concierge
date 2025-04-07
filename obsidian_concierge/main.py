"""
Main application entry point.

This module initializes and configures the FastAPI application, sets up middleware,
and includes all API routes.
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .utils.config import AppConfig, load_config
from .utils.logging import LogConfig, setup_logging

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

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


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