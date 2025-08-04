from fastapi import APIRouter, HTTPException, BackgroundTasks, File, UploadFile
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import logging
from ...services.document_service import DocumentService
from ...services.llm_service import LLMService

router = APIRouter()
logger = logging.getLogger(__name__)

# Global service instances
document_service = DocumentService()
llm_service = LLMService()

# Pydantic models for request/response
class AnalysisRequest(BaseModel):
    text: str
    analysis_types: List[str] = ["summary", "sentiment", "topics"]
    max_summary_length: int = 150

class QuestionRequest(BaseModel):
    text: str
    question: str

class ComparisonRequest(BaseModel):
    texts: List[str]
    comparison_aspects: List[str] = ["similarity", "key_differences"]

@router.post("/analyze")
async def analyze_text(request: AnalysisRequest) -> Dict[str, Any]:
    """Analyze text using multiple AI models"""
    
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text content is required")
    
    results = {}
    
    try:
        # Summarization
        if "summary" in request.analysis_types:
            summary_results = await llm_service.summarize_text(
                request.text, 
                max_length=request.max_summary_length
            )
            results["summary"] = summary_results
        
        # Sentiment Analysis
        if "sentiment" in request.analysis_types:
            sentiment_results = await llm_service.analyze_sentiment(request.text)
            results["sentiment"] = sentiment_results
        
        # Topic Extraction
        if "topics" in request.analysis_types:
            topic_results = await llm_service.extract_key_topics(request.text)
            results["topics"] = topic_results
        
        # Generate embeddings for similarity analysis
        if "embeddings" in request.analysis_types:
            embeddings = await llm_service.generate_embeddings([request.text])
            results["embeddings"] = {
                "vector_length": len(embeddings[0]) if embeddings else 0,
                "available": embeddings is not None
            }
        
        return {
            "analysis_results": results,
            "text_stats": {
                "word_count": len(request.text.split()),
                "char_count": len(request.text),
                "estimated_reading_time_minutes": len(request.text.split()) / 200  # Average reading speed
            },
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error analyzing text: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze-document")
async def analyze_document(
    file: UploadFile = File(...),
    analysis_types: str = "summary,sentiment,topics"
) -> Dict[str, Any]:
    """Upload and analyze a document in one step"""
    
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
        
        # Parse analysis types
        analysis_list = [t.strip() for t in analysis_types.split(',')]
        
        # Perform analysis
        analysis_request = AnalysisRequest(
            text=text_content,
            analysis_types=analysis_list
        )
        
        analysis_results = await analyze_text(analysis_request)
        
        # Clean up uploaded file
        await document_service.cleanup_file(file_path)
        
        return {
            "document_info": {
                "filename": processing_result['filename'],
                "file_type": processing_result['file_type'],
                "word_count": processing_result['word_count'],
                "char_count": processing_result['char_count']
            },
            "analysis": analysis_results["analysis_results"],
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error analyzing document: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/question-answer")
async def question_answering(request: QuestionRequest) -> Dict[str, Any]:
    """Answer questions based on provided text context"""
    
    if not request.text.strip() or not request.question.strip():
        raise HTTPException(status_code=400, detail="Both text and question are required")
    
    try:
        qa_results = await llm_service.question_answering(request.text, request.question)
        
        return {
            "question": request.question,
            "answers": qa_results,
            "context_stats": {
                "word_count": len(request.text.split()),
                "char_count": len(request.text)
            },
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error in question answering: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/compare-texts")
async def compare_texts(request: ComparisonRequest) -> Dict[str, Any]:
    """Compare multiple texts using AI analysis"""
    
    if len(request.texts) < 2:
        raise HTTPException(status_code=400, detail="At least 2 texts are required for comparison")
    
    try:
        results = {}
        
        # Generate embeddings for similarity analysis
        if "similarity" in request.comparison_aspects:
            embeddings = await llm_service.generate_embeddings(request.texts)
            if embeddings:
                # Calculate cosine similarity between texts
                import numpy as np
                from sklearn.metrics.pairwise import cosine_similarity
                
                similarity_matrix = cosine_similarity(embeddings)
                results["similarity_matrix"] = similarity_matrix.tolist()
                results["average_similarity"] = float(np.mean(similarity_matrix[np.triu_indices_from(similarity_matrix, k=1)]))
        
        # Generate comparative analysis using LLM
        if "key_differences" in request.comparison_aspects and llm_service.ollama_client:
            comparison_prompt = f"""Compare the following texts and identify the key differences and similarities:

Text 1: {request.texts[0][:1000]}...

Text 2: {request.texts[1][:1000]}...

Please provide:
1. Key similarities
2. Key differences  
3. Overall comparison summary
"""
            
            response = await llm_service.ollama_client.generate(
                model="mistral:7b",
                prompt=comparison_prompt
            )
            
            results["comparative_analysis"] = response['response']
        
        return {
            "comparison_results": results,
            "texts_info": [
                {
                    "index": i,
                    "word_count": len(text.split()),
                    "char_count": len(text)
                }
                for i, text in enumerate(request.texts)
            ],
            "status": "success"
        }
        
    except Exception as e:
        logger.error(f"Error comparing texts: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/analysis-types")
async def get_analysis_types() -> Dict[str, Any]:
    """Get available analysis types"""
    
    return {
        "available_analysis_types": [
            {
                "type": "summary",
                "description": "Generate text summaries using multiple LLM models",
                "models": ["Ollama (Llama2)", "Hugging Face (BART)"]
            },
            {
                "type": "sentiment",
                "description": "Analyze sentiment and emotional tone",
                "models": ["Hugging Face (RoBERTa)"]
            },
            {
                "type": "topics",
                "description": "Extract key topics and themes",
                "models": ["Ollama (Mistral)"]
            },
            {
                "type": "embeddings",
                "description": "Generate text embeddings for similarity analysis",
                "models": ["Sentence Transformers"]
            }
        ],
        "comparison_aspects": [
            "similarity",
            "key_differences"
        ]
    }