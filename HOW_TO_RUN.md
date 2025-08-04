# 🚀 How to Run DocuMind - Complete Guide

This guide provides multiple ways to run the DocuMind application, from simple local development to full Docker deployment.

## 📋 Prerequisites

### For Local Development (Simple Mode)
- **Python 3.8+**
- **Node.js 16+** and **npm**
- **4GB+ RAM**

### For Full Docker Deployment
- **Docker** and **Docker Compose**
- **8GB+ RAM** (for LLM models)
- **10GB+ free disk space**

## 🎯 Method 1: Simple Local Development (Recommended for Testing)

This method runs the application without Docker and uses simplified AI models for quick testing.

### Step 1: Setup Environment
```bash
# Navigate to project directory
cd /workspace

# Make setup script executable
chmod +x run-local.sh

# Run setup (creates virtual environment and installs minimal dependencies)
./run-local.sh
```

### Step 2: Start Backend (Terminal 1)
```bash
# Activate virtual environment
source venv/bin/activate

# Install minimal dependencies
pip install -r requirements-minimal.txt

# Create uploads directory
mkdir -p uploads

# Copy environment file
cp .env.example .env

# Start the simplified backend
cd backend
python -m uvicorn main_simple:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Start Frontend (Terminal 2)
```bash
# In a new terminal, navigate to project root
cd /workspace

# Start React development server
npm start
```

### Step 4: Access Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs

### Features Available in Simple Mode:
✅ Document upload and processing (PDF, DOCX, TXT, etc.)  
✅ Basic text summarization  
✅ Simple sentiment analysis  
✅ Topic extraction  
✅ Document comparison (basic)  
⚠️ Uses simplified AI models (not full LLMs)  

---

## 🐳 Method 2: Full Docker Deployment (Production-Ready)

This method provides the complete DocuMind experience with multiple LLM models.

### Prerequisites Check
```bash
# Check if Docker is installed
docker --version
docker-compose --version

# If not installed, install Docker first:
# Ubuntu/Debian: sudo apt update && sudo apt install docker.io docker-compose
# macOS: Install Docker Desktop
# Windows: Install Docker Desktop
```

### Step 1: Fix Frontend Build Issue
The error you encountered was due to missing `package-lock.json`. This has been fixed in the updated Dockerfile.

### Step 2: Build and Start Services
```bash
# Navigate to project directory
cd /workspace

# Copy environment configuration
cp .env.example .env

# Build all services (this may take 10-15 minutes first time)
docker-compose build

# Start all services
docker-compose up -d

# Monitor logs
docker-compose logs -f
```

### Step 3: Wait for Model Downloads
```bash
# Monitor model initialization (first time only, ~10-15 minutes)
docker-compose logs -f model-init

# Check service status
docker-compose ps
```

### Step 4: Access Full Application
- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/api/docs
- **Ollama**: http://localhost:11434

### Features Available in Full Mode:
✅ All document processing features  
✅ Multiple LLM models (Llama2, Mistral)  
✅ Advanced AI analysis  
✅ Hugging Face transformers  
✅ Sentence transformers for embeddings  
✅ Redis caching  
✅ Production-ready deployment  

---

## 🔧 Method 3: Hybrid Development

Run supporting services in Docker but develop locally.

### Step 1: Start Supporting Services
```bash
# Start only Ollama and Redis
docker-compose up ollama redis -d
```

### Step 2: Run Backend Locally
```bash
# Use the full backend with external services
source venv/bin/activate
pip install -r requirements.txt

cd backend
python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Step 3: Run Frontend Locally
```bash
npm start
```

---

## 🛠️ Troubleshooting

### Common Issues and Solutions

#### 1. "npm ci" Error (Fixed)
**Error**: `npm ci` command fails  
**Solution**: Updated Dockerfile to use `npm install` instead

#### 2. Docker Not Found
**Error**: `docker: command not found`  
**Solution**: Install Docker:
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install docker.io docker-compose

# Add user to docker group
sudo usermod -aG docker $USER
# Log out and back in
```

#### 3. Port Already in Use
**Error**: Port 3000 or 8000 already in use  
**Solution**: 
```bash
# Find and kill processes using the ports
sudo lsof -i :3000
sudo lsof -i :8000
# Kill the processes or change ports in configuration
```

#### 4. Memory Issues
**Error**: Container killed due to memory  
**Solution**: 
- Increase Docker memory limit to 8GB+
- Close other applications
- Use simple mode for development

#### 5. Module Import Errors
**Error**: Python import errors  
**Solution**: 
```bash
# Ensure you're in virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements-minimal.txt  # for simple mode
# OR
pip install -r requirements.txt  # for full mode
```

### Checking Service Status

```bash
# Docker mode
docker-compose ps
docker-compose logs -f [service-name]

# Local mode
# Check if services are running on expected ports
curl http://localhost:8000/api/v1/health
curl http://localhost:3000
```

---

## 🎮 Testing the Application

### 1. Basic Functionality Test
1. Open http://localhost:3000
2. Navigate to "Analysis" page
3. Enter some sample text: "This is a great application for document analysis!"
4. Select analysis types and click "Analyze"
5. Verify results appear

### 2. Document Upload Test
1. Go to Analysis page
2. Upload a PDF or text file
3. Wait for processing
4. Check analysis results

### 3. Comparison Test
1. Navigate to "Compare" page
2. Enter two different texts
3. Click "Compare Texts"
4. Review similarity matrix

### 4. API Test
```bash
# Test health endpoint
curl http://localhost:8000/api/v1/health

# Test text analysis
curl -X POST "http://localhost:8000/api/v1/analyze" \
  -H "Content-Type: application/json" \
  -d '{"text": "This is a test", "analysis_types": ["summary", "sentiment"]}'
```

---

## 📊 Performance Comparison

| Mode | Setup Time | Memory Usage | AI Quality | Use Case |
|------|------------|--------------|------------|----------|
| Simple Local | 2-5 minutes | ~1GB | Basic | Development/Testing |
| Hybrid | 5-10 minutes | ~4GB | Good | Development with AI |
| Full Docker | 15-30 minutes | ~8GB | Excellent | Production/Demo |

---

## 🆘 Getting Help

If you encounter issues:

1. **Check Prerequisites**: Ensure Python, Node.js, or Docker are properly installed
2. **Review Logs**: Use `docker-compose logs -f` or check terminal output
3. **Try Simple Mode**: Start with Method 1 for basic functionality
4. **Check Ports**: Ensure ports 3000 and 8000 are available
5. **Memory**: Ensure sufficient RAM is available

### Quick Commands Reference

```bash
# Simple Mode
source venv/bin/activate
cd backend && python -m uvicorn main_simple:app --reload --host 0.0.0.0 --port 8000
# In new terminal: npm start

# Docker Mode  
docker-compose up -d
docker-compose logs -f

# Stop Services
# Simple: Ctrl+C in terminals
# Docker: docker-compose down

# Rebuild
docker-compose down && docker-compose build && docker-compose up -d
```

---

**Choose the method that best fits your needs and system capabilities!** 🎉