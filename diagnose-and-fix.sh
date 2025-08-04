#!/bin/bash

echo "🔍 DocuMind Container Diagnostic and Fix Script"
echo "==============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}1. Checking container status...${NC}"
docker-compose ps

echo -e "\n${BLUE}2. Checking backend logs...${NC}"
echo -e "${YELLOW}Backend container logs (last 20 lines):${NC}"
docker-compose logs --tail=20 backend

echo -e "\n${BLUE}3. Checking frontend logs...${NC}"
echo -e "${YELLOW}Frontend container logs (last 20 lines):${NC}"
docker-compose logs --tail=20 frontend

echo -e "\n${BLUE}4. Checking model-init logs...${NC}"
echo -e "${YELLOW}Model-init container logs:${NC}"
docker-compose logs model-init

echo -e "\n${BLUE}5. Checking Ollama logs...${NC}"
echo -e "${YELLOW}Ollama container logs (last 10 lines):${NC}"
docker-compose logs --tail=10 ollama

echo -e "\n${RED}🔧 FIXING ISSUES...${NC}"

echo -e "\n${YELLOW}Step 1: Stopping all services...${NC}"
docker-compose down

echo -e "\n${YELLOW}Step 2: Removing problematic images...${NC}"
docker rmi llm-project_backend llm-project_frontend || true

echo -e "\n${YELLOW}Step 3: Cleaning up volumes (optional - comment out if you want to keep data)...${NC}"
# docker-compose down --volumes

echo -e "\n${YELLOW}Step 4: Rebuilding all services...${NC}"
docker-compose build --no-cache

echo -e "\n${YELLOW}Step 5: Starting services in order...${NC}"
echo "Starting Redis first..."
docker-compose up -d redis

echo "Waiting for Redis to be ready..."
sleep 10

echo "Starting Ollama..."
docker-compose up -d ollama

echo "Waiting for Ollama to be ready..."
sleep 30

echo "Starting backend..."
docker-compose up -d backend

echo "Waiting for backend to be ready..."
sleep 20

echo "Starting frontend..."
docker-compose up -d frontend

echo -e "\n${GREEN}✅ Services started! Checking status...${NC}"
sleep 10
docker-compose ps

echo -e "\n${BLUE}Checking service health...${NC}"
echo "Testing backend health..."
curl -f http://localhost:8000/api/v1/health || echo "Backend not ready yet"

echo -e "\nTesting frontend..."
curl -f http://localhost:3000 || echo "Frontend not ready yet"

echo -e "\n${GREEN}🎉 Fix attempt complete!${NC}"
echo -e "${YELLOW}If issues persist, check the logs above for specific errors.${NC}"