#!/bin/bash

echo "🚀 Quick Fix for DocuMind Container Issues"
echo "=========================================="

# Stop all services
echo "1. Stopping all services..."
docker-compose down

# Remove problematic containers and images
echo "2. Cleaning up containers and images..."
docker-compose rm -f
docker rmi llm-project_backend llm-project_frontend 2>/dev/null || true

# Rebuild only the problematic services
echo "3. Rebuilding backend and frontend..."
docker-compose build --no-cache backend frontend

# Start services in the right order
echo "4. Starting services in order..."

echo "   Starting Redis..."
docker-compose up -d redis
sleep 5

echo "   Starting Ollama..."
docker-compose up -d ollama
sleep 15

echo "   Starting Backend..."
docker-compose up -d backend
sleep 10

echo "   Starting Frontend..."
docker-compose up -d frontend
sleep 5

# Check status
echo "5. Checking service status..."
docker-compose ps

echo ""
echo "6. Testing services..."
echo "   Testing backend health..."
timeout 10 bash -c 'until curl -f http://localhost:8000/api/v1/health; do sleep 2; done' && echo "✅ Backend is healthy!" || echo "❌ Backend not responding"

echo "   Testing frontend..."
timeout 10 bash -c 'until curl -f http://localhost:3000; do sleep 2; done' && echo "✅ Frontend is healthy!" || echo "❌ Frontend not responding"

echo ""
echo "🎉 Quick fix complete!"
echo "If services are still restarting, run: docker-compose logs [service-name]"