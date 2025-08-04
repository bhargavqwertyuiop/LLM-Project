# DocuMind - AI-Powered Document Analysis System

![DocuMind Logo](https://img.shields.io/badge/DocuMind-AI%20Document%20Analysis-blue?style=for-the-badge&logo=brain&logoColor=white)

DocuMind is a comprehensive, professional-grade AI document analysis system that leverages multiple open-source Large Language Models (LLMs) to provide intelligent document processing, summarization, sentiment analysis, and comparison capabilities.

## 🚀 Features

### Multi-Format Document Support
- **PDF** - Extract and analyze PDF documents
- **DOCX/DOC** - Microsoft Word document processing
- **TXT** - Plain text file analysis
- **PPTX** - PowerPoint presentation content extraction
- **XLSX/XLS** - Excel spreadsheet data analysis
- **CSV** - Comma-separated values processing

### AI-Powered Analysis
- **Text Summarization** - Generate concise summaries using multiple LLM models
- **Sentiment Analysis** - Analyze emotional tone and sentiment
- **Topic Extraction** - Identify key topics and themes
- **Question Answering** - Interactive Q&A based on document content
- **Document Comparison** - Compare multiple documents for similarities and differences
- **Embedding Generation** - Create vector embeddings for semantic analysis

### Multiple LLM Integration
- **Ollama** - Local LLM models (Llama2, Mistral)
- **Hugging Face Transformers** - BART, RoBERTa, and other models
- **Sentence Transformers** - Semantic embeddings and similarity

### Modern Web Interface
- **React + TypeScript** - Modern, responsive frontend
- **Material-UI** - Professional design system
- **Drag & Drop** - Intuitive file upload
- **Real-time Processing** - Live analysis results
- **Interactive Results** - Expandable analysis sections

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React Frontend │    │  FastAPI Backend │    │  Ollama Service │
│   (Port 3000)   │◄──►│   (Port 8000)   │◄──►│   (Port 11434) │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                       ┌─────────────────┐
                       │  Redis Cache    │
                       │   (Port 6379)   │
                       └─────────────────┘
```

## 🛠️ Technology Stack

### Backend
- **FastAPI** - High-performance Python web framework
- **Ollama** - Local LLM model serving
- **Hugging Face Transformers** - Pre-trained model library
- **Sentence Transformers** - Semantic text embeddings
- **PyPDF2** - PDF text extraction
- **python-docx** - Word document processing
- **pandas** - Data manipulation and analysis
- **Redis** - Caching and task queue
- **SQLite** - Local database storage

### Frontend
- **React 18** - Modern UI library
- **TypeScript** - Type-safe JavaScript
- **Material-UI (MUI)** - React component library
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **React Dropzone** - File upload component

### Infrastructure
- **Docker & Docker Compose** - Containerization
- **Nginx** - Reverse proxy and static file serving
- **Multi-stage builds** - Optimized container images

## 📋 Prerequisites

- **Docker** and **Docker Compose**
- **8GB+ RAM** (recommended for LLM models)
- **10GB+ free disk space** (for models and data)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd documind
```

### 2. Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your configurations (optional)
nano .env
```

### 3. Start with Docker Compose
```bash
# Build and start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

### 4. Initialize LLM Models
The system will automatically pull required models on first startup. This may take 10-15 minutes depending on your internet connection.

```bash
# Monitor model download progress
docker-compose logs -f model-init
```

### 5. Access the Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/api/docs

## 📖 Usage Guide

### Document Analysis

1. **Upload a Document**
   - Navigate to the Analysis page
   - Drag and drop a file or click to select
   - Supported formats: PDF, DOCX, TXT, PPTX, XLSX, CSV

2. **Select Analysis Types**
   - ✅ Summarization - Generate text summaries
   - ✅ Sentiment Analysis - Analyze emotional tone
   - ✅ Topic Extraction - Identify key themes
   - ⬜ Embeddings - Generate vector representations

3. **View Results**
   - Multiple model results for comparison
   - Interactive expandable sections
   - Detailed analysis metrics

### Text Comparison

1. **Navigate to Compare Page**
2. **Enter Multiple Texts**
   - Add 2-5 texts to compare
   - Use the "Add Another Text" button
3. **Run Comparison**
   - Semantic similarity matrix
   - AI-generated comparative analysis
   - Visual similarity indicators

### Question Answering

1. **Upload or Enter Text**
2. **Ask Questions**
   - Use the Q&A endpoint via API
   - Get contextual answers based on document content

## 🔧 Configuration

### Environment Variables

```bash
# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
DEBUG=True

# Database
DATABASE_URL=sqlite:///./documind.db

# Redis
REDIS_URL=redis://localhost:6379

# Ollama Configuration
OLLAMA_BASE_URL=http://localhost:11434

# File Upload Settings
MAX_FILE_SIZE_MB=50
UPLOAD_DIR=./uploads

# Model Configuration
DEFAULT_SUMMARIZATION_MODEL=llama2:7b
DEFAULT_QA_MODEL=mistral:7b
DEFAULT_EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
```

### Custom Models

Add custom Ollama models by modifying the `model-init` service in `docker-compose.yml`:

```yaml
command: >
  sh -c "
    # ... existing commands ...
    curl -X POST http://ollama:11434/api/pull -d '{\"name\": \"your-custom-model\"}' &&
    echo 'Custom model pulled successfully!'
  "
```

## 🛡️ API Reference

### Health Check
```http
GET /api/v1/health
```

### Document Upload and Analysis
```http
POST /api/v1/analyze-document
Content-Type: multipart/form-data

file: <document-file>
analysis_types: "summary,sentiment,topics"
```

### Text Analysis
```http
POST /api/v1/analyze
Content-Type: application/json

{
  "text": "Your text here",
  "analysis_types": ["summary", "sentiment", "topics"],
  "max_summary_length": 150
}
```

### Text Comparison
```http
POST /api/v1/compare-texts
Content-Type: application/json

{
  "texts": ["Text 1", "Text 2"],
  "comparison_aspects": ["similarity", "key_differences"]
}
```

### Question Answering
```http
POST /api/v1/question-answer
Content-Type: application/json

{
  "text": "Context text",
  "question": "Your question"
}
```

## 🔍 Development

### Local Development Setup

1. **Backend Development**
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Start development server
cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

2. **Frontend Development**
```bash
# Install dependencies
npm install

# Start development server
npm start
```

3. **Start Supporting Services**
```bash
# Start only Ollama and Redis
docker-compose up ollama redis -d
```

### Testing

```bash
# Backend tests
pytest backend/tests/

# Frontend tests
npm test
```

## 🐳 Docker Services

| Service | Port | Description |
|---------|------|-------------|
| frontend | 3000 | React application |
| backend | 8000 | FastAPI server |
| ollama | 11434 | LLM model server |
| redis | 6379 | Cache and task queue |

## 📊 Performance Considerations

### Hardware Requirements
- **Minimum**: 4GB RAM, 2 CPU cores
- **Recommended**: 8GB+ RAM, 4+ CPU cores
- **Optimal**: 16GB+ RAM, 8+ CPU cores, GPU support

### Model Performance
- **Llama2 7B**: ~4GB VRAM, good general performance
- **Mistral 7B**: ~4GB VRAM, excellent for Q&A
- **BART Large**: ~1GB RAM, fast summarization
- **Sentence Transformers**: ~500MB RAM, quick embeddings

### Scaling Options
- Increase Docker resource limits
- Use GPU acceleration for models
- Implement horizontal scaling with load balancers
- Add model caching strategies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Ollama** - Local LLM serving
- **Hugging Face** - Pre-trained models and transformers
- **FastAPI** - High-performance web framework
- **React** - Frontend framework
- **Material-UI** - React components
- **Docker** - Containerization platform

## 📞 Support

For support, questions, or feature requests:
- Open an issue on GitHub
- Check the [API documentation](http://localhost:8000/api/docs)
- Review the logs: `docker-compose logs -f`

---

**Built with ❤️ using open-source AI technologies**