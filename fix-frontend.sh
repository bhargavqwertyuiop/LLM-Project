#!/bin/bash

echo "🔧 Fixing DocuMind Frontend Container Issues..."

# Stop and remove the problematic container
echo "Stopping frontend container..."
docker-compose stop frontend
docker-compose rm -f frontend

# Remove the frontend image to force rebuild
echo "Removing frontend image to force rebuild..."
docker rmi llm-project_frontend || true

# Rebuild and start the frontend
echo "Rebuilding frontend container..."
docker-compose build frontend

echo "Starting frontend container..."
docker-compose up -d frontend

# Wait a moment and check status
sleep 10
echo "Checking container status..."
docker-compose ps frontend

echo "Checking logs..."
docker-compose logs --tail=20 frontend

echo "✅ Frontend container fix complete!"
echo "If still having issues, check the logs above for specific errors."