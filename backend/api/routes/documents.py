from fastapi import APIRouter, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from typing import Dict, Any, List
import logging
from ...services.document_service import DocumentService
from ...services.llm_service import LLMService

router = APIRouter()
logger = logging.getLogger(__name__)

# Global service instances
document_service = DocumentService()
llm_service = LLMService()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)) -> Dict[str, Any]:
    """Upload and process a document"""
    
    # Validate file
    is_valid, message = document_service.validate_file(file)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)
    
    try:
        # Save uploaded file
        file_path, file_id = await document_service.save_uploaded_file(file)
        
        # Process document
        processing_result = await document_service.process_document(file_path)
        
        if processing_result['processing_status'] == 'error':
            raise HTTPException(status_code=500, detail=processing_result.get('error_message'))
        
        return {
            "file_id": file_id,
            "filename": processing_result['filename'],
            "file_size": processing_result['file_size'],
            "file_type": processing_result['file_type'],
            "word_count": processing_result['word_count'],
            "char_count": processing_result['char_count'],
            "status": "uploaded_and_processed",
            "message": "Document uploaded and processed successfully"
        }
        
    except Exception as e:
        logger.error(f"Error uploading document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/supported-formats")
async def get_supported_formats() -> Dict[str, Any]:
    """Get list of supported document formats"""
    
    return {
        "supported_extensions": document_service.get_supported_extensions(),
        "max_file_size_mb": 50,
        "description": "Supported document formats for processing"
    }

@router.post("/process/{file_id}")
async def process_document_by_id(file_id: str) -> Dict[str, Any]:
    """Process a previously uploaded document by ID"""
    
    # This would typically involve database lookup
    # For now, we'll return an error as this requires database integration
    raise HTTPException(
        status_code=501, 
        detail="Document processing by ID requires database integration"
    )

@router.delete("/cleanup/{file_id}")
async def cleanup_document(file_id: str) -> Dict[str, Any]:
    """Clean up uploaded document"""
    
    try:
        # In a real implementation, you'd look up the file path from database
        # For now, we'll return a success message
        return {
            "file_id": file_id,
            "status": "cleanup_requested",
            "message": "Document cleanup requested"
        }
        
    except Exception as e:
        logger.error(f"Error cleaning up document: {e}")
        raise HTTPException(status_code=500, detail=str(e))