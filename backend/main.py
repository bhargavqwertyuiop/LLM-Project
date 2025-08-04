from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import uvicorn
import os
from dotenv import load_dotenv
from pathlib import Path
import logging
from typing import List, Optional
import asyncio

from .core.config import settings
from .api.routes import documents, analysis, health
from .services.llm_service import LLMService
from .services.document_service import DocumentService
from .database.database import engine, Base

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="DocuMind - AI Document Analysis System",
    description="An intelligent document analysis system using multiple open-source LLMs",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create upload directory
upload_dir = Path(settings.UPLOAD_DIR)
upload_dir.mkdir(exist_ok=True)

# Mount static files
app.mount("/uploads", StaticFiles(directory=str(upload_dir)), name="uploads")

# Include routers
app.include_router(health.router, prefix="/api/v1", tags=["health"])
app.include_router(documents.router, prefix="/api/v1", tags=["documents"])
app.include_router(analysis.router, prefix="/api/v1", tags=["analysis"])

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting DocuMind API...")
    
    # Initialize LLM service
    try:
        llm_service = LLMService()
        await llm_service.initialize()
        logger.info("LLM services initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize LLM services: {e}")
    
    logger.info("DocuMind API started successfully!")

@app.get("/")
async def root():
    return {
        "message": "Welcome to DocuMind - AI Document Analysis System",
        "version": "1.0.0",
        "docs": "/api/docs"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG
    )