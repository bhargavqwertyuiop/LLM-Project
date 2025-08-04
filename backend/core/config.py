from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = True
    
    # Database
    DATABASE_URL: str = "sqlite:///./documind.db"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # External APIs
    HUGGINGFACE_API_TOKEN: Optional[str] = None
    OPENAI_API_KEY: Optional[str] = None
    
    # Ollama Configuration
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    
    # File Upload Settings
    MAX_FILE_SIZE_MB: int = 50
    UPLOAD_DIR: str = "./uploads"
    
    # Security
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # LLM Models Configuration
    DEFAULT_SUMMARIZATION_MODEL: str = "llama2:7b"
    DEFAULT_QA_MODEL: str = "mistral:7b"
    DEFAULT_EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"
    
    model_config = {"env_file": ".env", "case_sensitive": True}

# Create global settings instance
settings = Settings()