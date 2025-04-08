"""
Main FastAPI application for Obsidian Concierge.

This module sets up the FastAPI application with middleware and routes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import router

# Create FastAPI app
app = FastAPI(
    title="Obsidian Concierge",
    description="API for searching and querying Obsidian vault content",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"} 