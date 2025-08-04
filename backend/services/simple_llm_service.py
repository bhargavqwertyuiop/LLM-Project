import logging
from typing import Dict, List, Optional, Any

logger = logging.getLogger(__name__)

class SimpleLLMService:
    """Simplified LLM service for local development without external dependencies"""
    
    def __init__(self):
        self.available_models = {
            'mock': ['simple-summarizer', 'simple-sentiment', 'simple-qa']
        }
        
    async def initialize(self):
        """Initialize the simple LLM service"""
        logger.info("Simple LLM service initialized (mock mode)")
    
    async def summarize_text(self, text: str, max_length: int = 150, method: str = "auto") -> Dict[str, Any]:
        """Mock text summarization"""
        words = text.split()
        if len(words) <= max_length // 5:  # Rough word count estimation
            summary = text
        else:
            # Take first and last parts of text
            first_part = ' '.join(words[:max_length//10])
            last_part = ' '.join(words[-max_length//10:])
            summary = f"{first_part}... {last_part}"
        
        return {
            'mock': {
                'summary': f"**Summary:** {summary}",
                'model': 'simple-summarizer'
            }
        }
    
    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """Mock sentiment analysis"""
        # Simple keyword-based sentiment
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'love', 'like']
        negative_words = ['bad', 'terrible', 'awful', 'hate', 'dislike', 'horrible', 'worst']
        
        text_lower = text.lower()
        positive_count = sum(1 for word in positive_words if word in text_lower)
        negative_count = sum(1 for word in negative_words if word in text_lower)
        
        if positive_count > negative_count:
            sentiment = 'POSITIVE'
            confidence = min(0.9, 0.6 + (positive_count - negative_count) * 0.1)
        elif negative_count > positive_count:
            sentiment = 'NEGATIVE'
            confidence = min(0.9, 0.6 + (negative_count - positive_count) * 0.1)
        else:
            sentiment = 'NEUTRAL'
            confidence = 0.5
        
        return {
            'overall_sentiment': sentiment,
            'confidence': confidence,
            'detailed_results': [
                {'label': sentiment, 'score': confidence}
            ]
        }
    
    async def question_answering(self, context: str, question: str) -> Dict[str, Any]:
        """Mock question answering"""
        # Simple keyword matching
        question_words = question.lower().split()
        context_sentences = context.split('.')
        
        # Find sentence with most question word matches
        best_sentence = ""
        max_matches = 0
        
        for sentence in context_sentences:
            sentence_lower = sentence.lower()
            matches = sum(1 for word in question_words if word in sentence_lower)
            if matches > max_matches:
                max_matches = matches
                best_sentence = sentence.strip()
        
        answer = best_sentence if best_sentence else "I couldn't find a specific answer in the provided context."
        
        return {
            'mock': {
                'answer': answer,
                'model': 'simple-qa'
            }
        }
    
    async def generate_embeddings(self, texts: List[str]) -> Optional[List[List[float]]]:
        """Mock embedding generation"""
        # Generate simple hash-based embeddings
        import hashlib
        
        embeddings = []
        for text in texts:
            # Create a simple 384-dimensional embedding based on text hash
            hash_obj = hashlib.md5(text.encode())
            hash_hex = hash_obj.hexdigest()
            
            # Convert hex to numbers and normalize
            embedding = []
            for i in range(0, len(hash_hex), 2):
                val = int(hash_hex[i:i+2], 16) / 255.0  # Normalize to 0-1
                embedding.extend([val] * 12)  # Repeat to get 384 dimensions
            
            embeddings.append(embedding[:384])  # Ensure exactly 384 dimensions
        
        return embeddings
    
    async def extract_key_topics(self, text: str, num_topics: int = 5) -> Dict[str, Any]:
        """Mock topic extraction"""
        words = text.lower().split()
        # Simple word frequency analysis
        word_freq = {}
        for word in words:
            if len(word) > 4:  # Only consider longer words
                word_freq[word] = word_freq.get(word, 0) + 1
        
        # Get top words
        top_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)[:num_topics]
        
        topics = []
        for i, (word, freq) in enumerate(top_words, 1):
            topics.append(f"{i}. **{word.title()}** - appears {freq} times")
        
        topics_text = "\n".join(topics) if topics else "No significant topics identified."
        
        return {
            'topics': f"**Key Topics Identified:**\n\n{topics_text}",
            'model': 'simple-topic-extractor'
        }
    
    def get_available_models(self) -> Dict[str, List[str]]:
        """Get list of available models"""
        return self.available_models
    
    def health_check(self) -> Dict[str, bool]:
        """Check health of services"""
        return {
            'mock_service': True,
            'huggingface_summarizer': False,
            'sentiment_analyzer': False,
            'sentence_transformer': False
        }