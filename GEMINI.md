# AI Fashion Reel Generator (Non-AI MVP)

Automate the creation of 9:16 Instagram reels for fashion boutiques using traditional Computer Vision and DSP.

## 📄 Documentation
- **[FEATURES.md](./FEATURES.md):** Detailed feature list, technical specification, and workflow diagrams.

## 🚀 Launch Instructions

To run the full application, you need to start four separate components. Open a new terminal tab for each:

### 1. Infrastructure (Redis)
Ensure Docker Desktop is running, then start the message broker:
```bash
docker-compose up -d
```

### 2. Backend API (FastAPI)
Starts the web server that handles requests and manages the database:
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --port 8001
```
*API will be available at: http://localhost:8001*

### 3. Background Worker (Celery)
Starts the process that performs the actual video rendering:
```bash
cd backend
celery -A app.workers.celery_app.celery_app worker --loglevel=info
```

### 5. Run Tests
Ensure all dependencies are installed, then:

**Backend:**
```bash
cd backend
PYTHONPATH=. pytest tests/
```

**Frontend:**
```bash
cd frontend
npx vitest run
```

---

## 🏗️ Project Structure
- `backend/app/api`: FastAPI endpoints.
- `backend/app/services`: Core CV and Video logic (OpenCV/MoviePy).
- `backend/app/workers`: Celery task definitions.
- `frontend/src`: React components and API integration.

## ✅ Current Progress
- [x] POC for scene detection and image-to-video generation.
- [x] Smart-cropping using edge-based saliency.
- [x] Asynchronous Task Queue (Celery/Redis).
- [x] Persistent Database (SQLite/SQLAlchemy).
- [x] Web Dashboard (Frontend).
- [ ] AI Virtual Try-On (VTON Roadmap).
- [ ] S3/Cloud storage integration (Currently uses local storage).
- [ ] AI Background Removal (Roadmap).
