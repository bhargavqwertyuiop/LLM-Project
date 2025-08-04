from fastapi import APIRouter, Depends
from typing import Dict, Any
import asyncio
from ...services.llm_service import LLMService

router = APIRouter()

# Global LLM service instance
llm_service = LLMService()

@router.get("/health")
async def health_check() -> Dict[str, Any]:
    """Health check endpoint"""
    
    # Check LLM services
    llm_health = llm_service.health_check()
    
    # Overall health status
    all_healthy = any(llm_health.values())  # At least one LLM service should be working
    
    return {
        "status": "healthy" if all_healthy else "degraded",
        "services": {
            "llm": llm_health,
            "api": True
        },
        "message": "DocuMind API is running"
    }

@router.get("/models")
async def get_available_models() -> Dict[str, Any]:
    """Get available LLM models"""
    
    try:
        models = llm_service.get_available_models()
        return {
            "available_models": models,
            "status": "success"
        }
    except Exception as e:
        return {
            "error": str(e),
            "status": "error"
        }