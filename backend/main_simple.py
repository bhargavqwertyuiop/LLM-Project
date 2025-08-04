from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os
from dotenv import load_dotenv
from pathlib import Path
import logging

# Import simplified services
from services.simple_llm_service import SimpleLLMService
from services.document_service_simple import SimpleDocumentService

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="DocuMind - AI Document Analysis System (Simple Mode)",
    description="A simplified version for local development",
    version="1.0.0-simple",
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
upload_dir = Path("./uploads")
upload_dir.mkdir(exist_ok=True)

# Mount static files
app.mount("/uploads", StaticFiles(directory=str(upload_dir)), name="uploads")

# Initialize services
llm_service = SimpleLLMService()
document_service = SimpleDocumentService()

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    logger.info("Starting DocuMind API (Simple Mode)...")
    await llm_service.initialize()
    logger.info("DocuMind API started successfully!")

@app.get("/")
async def root():
    return {
        "message": "Welcome to DocuMind - AI Document Analysis System (Simple Mode)",
        "version": "1.0.0-simple",
        "docs": "/api/docs",
        "note": "This is a simplified version for local development"
    }

@app.get("/api/v1/health")
async def health_check():
    """Health check endpoint"""
    llm_health = llm_service.health_check()
    
    return {
        "status": "healthy",
        "services": {
            "llm": llm_health,
            "api": True
        },
        "message": "DocuMind API is running (Simple Mode)"
    }

@app.get("/api/v1/models")
async def get_available_models():
    """Get available models"""
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

@app.post("/api/v1/analyze")
async def analyze_text(request: dict):
    """Analyze text using simple AI models"""
    text = request.get('text', '')
    analysis_types = request.get('analysis_types', ['summary', 'sentiment', 'topics'])
    
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text content is required")
    
    results = {}
    
    try:
        # Summarization
        if "summary" in analysis_types:
            summary_results = await llm_service.summarize_text(text)
            results["summary"] = summary_results
        
        # Sentiment Analysis
        if "sentiment" in analysis_types:
            sentiment_results = await llm_service.analyze_sentiment(text)
            results["sentiment"] = sentiment_results
        
        # Topic Extraction
        if "topics" in analysis_types:
            topic_results = await llm_service.extract_key_topics(text)
            results["topics"] = topic_results
        
        # Generate embeddings
        if "embeddings" in analysis_types:
            embeddings = await llm_service.generate_embeddings([text])
            results["embeddings"] = {
                "vector_length": len(embeddings[0]) if embeddings else 0,
                "available": embeddings is not None
            }
        
        return {
            "analysis_results": results,
            "text_stats": {
                "word_count": len(text.split()),
                "char_count": len(text),
                "estimated_reading_time_minutes": len(text.split()) / 200
            },
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error analyzing text: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/analyze-document")
async def analyze_document(file: UploadFile = File(...)):
    """Upload and analyze a document"""
    
    # Validate file
    is_valid, message = document_service.validate_file(file)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)
    
    try:
        # Save and process document
        file_path, file_id = await document_service.save_uploaded_file(file)
        processing_result = await document_service.process_document(file_path)
        
        if processing_result['processing_status'] == 'error':
            raise HTTPException(status_code=500, detail=processing_result.get('error_message'))
        
        # Extract text content
        text_content = processing_result['text_content']
        
        if not text_content.strip():
            raise HTTPException(status_code=400, detail="No text content found in document")
        
        # Perform analysis using simple models
        analysis_results = {}
        
        # Summarization
        summary_results = await llm_service.summarize_text(text_content)
        analysis_results["summary"] = summary_results
        
        # Sentiment Analysis
        sentiment_results = await llm_service.analyze_sentiment(text_content)
        analysis_results["sentiment"] = sentiment_results
        
        # Topic Extraction
        topic_results = await llm_service.extract_key_topics(text_content)
        analysis_results["topics"] = topic_results
        
        # Clean up uploaded file
        await document_service.cleanup_file(file_path)
        
        return {
            "document_info": {
                "filename": processing_result['filename'],
                "file_type": processing_result['file_type'],
                "word_count": processing_result['word_count'],
                "char_count": processing_result['char_count']
            },
            "analysis": analysis_results,
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error analyzing document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/compare-texts")
async def compare_texts(request: dict):
    """Compare multiple texts"""
    texts = request.get('texts', [])
    
    if len(texts) < 2:
        raise HTTPException(status_code=400, detail="At least 2 texts are required for comparison")
    
    try:
        results = {}
        
        # Generate embeddings for similarity analysis
        embeddings = await llm_service.generate_embeddings(texts)
        if embeddings:
            # Calculate simple similarity (mock)
            import random
            similarity_matrix = []
            for i in range(len(texts)):
                row = []
                for j in range(len(texts)):
                    if i == j:
                        row.append(1.0)
                    else:
                        # Mock similarity based on text length similarity
                        len_diff = abs(len(texts[i]) - len(texts[j]))
                        similarity = max(0.1, 1.0 - (len_diff / max(len(texts[i]), len(texts[j]))))
                        row.append(similarity)
                similarity_matrix.append(row)
            
            results["similarity_matrix"] = similarity_matrix
            
            # Calculate average similarity
            total_sim = 0
            count = 0
            for i in range(len(similarity_matrix)):
                for j in range(i+1, len(similarity_matrix[i])):
                    total_sim += similarity_matrix[i][j]
                    count += 1
            
            results["average_similarity"] = total_sim / count if count > 0 else 0
        
        # Simple comparative analysis
        results["comparative_analysis"] = f"""**Comparative Analysis:**

**Text Lengths:**
- Text 1: {len(texts[0])} characters
- Text 2: {len(texts[1])} characters

**Key Observations:**
- Length difference: {abs(len(texts[0]) - len(texts[1]))} characters
- Both texts are {"similar" if abs(len(texts[0]) - len(texts[1])) < 100 else "different"} in length

*Note: This is a simplified analysis. For advanced AI comparison, use the full Docker version.*
"""
        
        return {
            "comparison_results": results,
            "texts_info": [
                {
                    "index": i,
                    "word_count": len(text.split()),
                    "char_count": len(text)
                }
                for i, text in enumerate(texts)
            ],
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error comparing texts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/supported-formats")
async def get_supported_formats():
    """Get supported document formats"""
    return {
        "supported_extensions": document_service.get_supported_extensions(),
        "max_file_size_mb": 50,
        "description": "Supported document formats for processing"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )