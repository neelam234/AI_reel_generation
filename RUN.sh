#!/bin/bash

# AI Fashion Reel Generator - Execution Reference
# This file serves as a quick reference for the commands needed to run the application.

echo "-------------------------------------------------------"
echo "AI Fashion Reel Generator - Startup Commands"
echo "-------------------------------------------------------"

echo "1. INFRASTRUCTURE (Redis)"
echo "Command: docker-compose up -d"
echo ""

echo "2. BACKEND API (FastAPI)"
echo "Commands:"
echo "cd backend"
echo "uvicorn main:app --port 8001"
echo ""

echo "3. BACKGROUND WORKER (Celery)"
echo "Commands:"
echo "cd backend"
echo "celery -A app.workers.celery_app.celery_app worker --loglevel=info"
echo ""

echo "4. FRONTEND DASHBOARD (React)"
echo "Commands:"
echo "cd frontend"
echo "npm run dev -- --port 3001"
echo ""

echo "-------------------------------------------------------"
echo "Access points:"
echo "Frontend: http://localhost:3001"
echo "Backend API: http://localhost:8001"
echo "-------------------------------------------------------"
