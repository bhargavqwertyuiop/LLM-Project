import asyncio
import logging
from typing import Dict, List, Optional, Any
import httpx
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
from sentence_transformers import SentenceTransformer
import torch
import ollama
from ..core.config import settings

logger = logging.getLogger(__name__)

class LLMService:
    """Service for managing multiple open-source LLM integrations"""
    
    def __init__(self):
        self.ollama_client = None
        self.hf_summarizer = None
        self.hf_qa_pipeline = None
        self.sentence_transformer = None
        self.sentiment_analyzer = None
        self.available_models = {}
        
    async def initialize(self):
        """Initialize all LLM services"""
        logger.info("Initializing LLM services...")
        
        # Initialize Ollama client
        await self._initialize_ollama()
        
        # Initialize Hugging Face models
        await self._initialize_huggingface_models()
        
        # Initialize sentence transformer for embeddings
        await self._initialize_sentence_transformer()
        
        logger.info("LLM services initialized successfully")
    
    async def _initialize_ollama(self):
        """Initialize Ollama client and check available models"""
        try:
            self.ollama_client = ollama.AsyncClient(host=settings.OLLAMA_BASE_URL)
            
            # Check if Ollama is running and get available models
            models = await self.ollama_client.list()
            self.available_models['ollama'] = [model['name'] for model in models.get('models', [])]
            
            logger.info(f"Ollama initialized with models: {self.available_models['ollama']}")
            
            # Pull default models if not available
            await self._ensure_ollama_models()
            
        except Exception as e:
            logger.warning(f"Ollama initialization failed: {e}")
            self.ollama_client = None
    
    async def _ensure_ollama_models(self):
        """Ensure required Ollama models are available"""
        required_models = [
            settings.DEFAULT_SUMMARIZATION_MODEL,
            settings.DEFAULT_QA_MODEL
        ]
        
        for model in required_models:
            if model not in self.available_models.get('ollama', []):
                try:
                    logger.info(f"Pulling Ollama model: {model}")
                    await self.ollama_client.pull(model)
                    logger.info(f"Successfully pulled model: {model}")
                except Exception as e:
                    logger.error(f"Failed to pull model {model}: {e}")
    
    async def _initialize_huggingface_models(self):
        """Initialize Hugging Face models"""
        try:
            # Initialize summarization pipeline
            self.hf_summarizer = pipeline(
                "summarization",
                model="facebook/bart-large-cnn",
                device=0 if torch.cuda.is_available() else -1
            )
            
            # Initialize sentiment analysis
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                device=0 if torch.cuda.is_available() else -1
            )
            
            logger.info("Hugging Face models initialized successfully")
            
        except Exception as e:
            logger.error(f"Hugging Face models initialization failed: {e}")
    
    async def _initialize_sentence_transformer(self):
        """Initialize sentence transformer for embeddings"""
        try:
            self.sentence_transformer = SentenceTransformer(settings.DEFAULT_EMBEDDING_MODEL)
            logger.info("Sentence transformer initialized successfully")
        except Exception as e:
            logger.error(f"Sentence transformer initialization failed: {e}")
    
    async def summarize_text(self, text: str, max_length: int = 150, method: str = "auto") -> Dict[str, Any]:
        """Summarize text using available models"""
        results = {}
        
        # Try Ollama first
        if self.ollama_client and method in ["auto", "ollama"]:
            try:
                prompt = f"Please provide a concise summary of the following text in about {max_length} words:\n\n{text}"
                response = await self.ollama_client.generate(
                    model=settings.DEFAULT_SUMMARIZATION_MODEL,
                    prompt=prompt
                )
                results['ollama'] = {
                    'summary': response['response'],
                    'model': settings.DEFAULT_SUMMARIZATION_MODEL
                }
            except Exception as e:
                logger.error(f"Ollama summarization failed: {e}")
        
        # Try Hugging Face BART
        if self.hf_summarizer and method in ["auto", "huggingface"]:
            try:
                # Split text into chunks if too long
                max_chunk_length = 1024
                chunks = [text[i:i+max_chunk_length] for i in range(0, len(text), max_chunk_length)]
                
                summaries = []
                for chunk in chunks:
                    if len(chunk.strip()) > 50:  # Only process meaningful chunks
                        summary = self.hf_summarizer(chunk, max_length=max_length, min_length=30, do_sample=False)
                        summaries.append(summary[0]['summary_text'])
                
                results['huggingface'] = {
                    'summary': ' '.join(summaries),
                    'model': 'facebook/bart-large-cnn'
                }
            except Exception as e:
                logger.error(f"Hugging Face summarization failed: {e}")
        
        return results
    
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Analyze sentiment of text"""
        if not self.sentiment_analyzer:
            return {"error": "Sentiment analyzer not available"}
        
        try:
            # Split text into chunks for analysis
            max_length = 512
            chunks = [text[i:i+max_length] for i in range(0, len(text), max_length)]
            
            results = []
            for chunk in chunks:
                if len(chunk.strip()) > 10:
                    result = self.sentiment_analyzer(chunk)
                    results.append(result[0])
            
            # Aggregate results
            if results:
                avg_score = sum(r['score'] for r in results) / len(results)
                most_common_label = max(set(r['label'] for r in results), 
                                      key=[r['label'] for r in results].count)
                
                return {
                    'overall_sentiment': most_common_label,
                    'confidence': avg_score,
                    'detailed_results': results
                }
            
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            return {"error": str(e)}
    
    async def question_answering(self, context: str, question: str) -> Dict[str, Any]:
        """Answer questions based on context using available models"""
        results = {}
        
        # Try Ollama
        if self.ollama_client:
            try:
                prompt = f"""Context: {context}

Question: {question}

Please provide a detailed answer based on the context above:"""
                
                response = await self.ollama_client.generate(
                    model=settings.DEFAULT_QA_MODEL,
                    prompt=prompt
                )
                
                results['ollama'] = {
                    'answer': response['response'],
                    'model': settings.DEFAULT_QA_MODEL
                }
            except Exception as e:
                logger.error(f"Ollama Q&A failed: {e}")
        
        return results
    
    async def generate_embeddings(self, texts: List[str]) -> Optional[List[List[float]]]:
        """Generate embeddings for texts"""
        if not self.sentence_transformer:
            return None
        
        try:
            embeddings = self.sentence_transformer.encode(texts)
            return embeddings.tolist()
        except Exception as e:
            logger.error(f"Embedding generation failed: {e}")
            return None
    
    async def extract_key_topics(self, text: str, num_topics: int = 5) -> Dict[str, Any]:
        """Extract key topics from text using LLM"""
        if not self.ollama_client:
            return {"error": "No LLM available for topic extraction"}
        
        try:
            prompt = f"""Analyze the following text and extract the {num_topics} most important topics or themes. 
Provide them as a numbered list with brief explanations:

Text: {text}

Key Topics:"""
            
            response = await self.ollama_client.generate(
                model=settings.DEFAULT_QA_MODEL,
                prompt=prompt
            )
            
            return {
                'topics': response['response'],
                'model': settings.DEFAULT_QA_MODEL
            }
        except Exception as e:
            logger.error(f"Topic extraction failed: {e}")
            return {"error": str(e)}
    
    def get_available_models(self) -> Dict[str, List[str]]:
        """Get list of available models"""
        return self.available_models
    
    def health_check(self) -> Dict[str, bool]:
        """Check health of all services"""
        return {
            'ollama': self.ollama_client is not None,
            'huggingface_summarizer': self.hf_summarizer is not None,
            'sentiment_analyzer': self.sentiment_analyzer is not None,
            'sentence_transformer': self.sentence_transformer is not None
        }