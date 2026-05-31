# AI Fashion Reel Generator 🎞️✨

Summary:

The AI Fashion Reel Generator is an automated video production tool designed for fashion boutiques to transform static product photos into professional 9:16 Instagram Reels.

The Core Problem
Creating engaging social media content usually requires manual video editing or expensive generative AI models with high latency. This project uses traditional Computer Vision (CV) and Digital Signal Processing
(DSP) to provide a fast, cost-effective alternative.

How it Works
1. Rhythm Mapping: It analyzes a "reference video" to detect scene changes and transitions, creating a timing template.
2. Smart Cropping: It uses OpenCV (Canny edge detection) to find the "center of interest" in a photo and automatically crops horizontal or square images into a vertical 9:16 format without losing the product.
3. Automated Animation: It applies "Ken Burns" effects (slow zooms/pans) to static images to make them feel cinematic.
4. Async Rendering: Heavy video processing is offloaded to background workers (Celery/Redis) so the web interface remains fast and responsive.

Tech Stack
* Backend: FastAPI (Python), SQLAlchemy, Celery, Redis.
* Frontend: React 19, TypeScript, Vite.
* Engine: MoviePy (Video Compositing), OpenCV (Image Analysis), PySceneDetect.

Current Status
The project is currently a functional MVP with a full web dashboard, asynchronous task management, and a persistent database. The roadmap includes upgrading to AI Virtual Try-On (VTON) and automated background
removal.
---

##  Technical Approach

Unlike standard video editors, this project uses an automated "Match-and-Frame" pipeline:

1.  **Intelligent Scene Matching:** 
    *   **PySceneDetect** analyzes the reference video to identify exact timestamps for every cut and transition.
    *   The system creates a "rhythm map" that dictates the duration and placement of each product image.
2.  **Smart Visual Processing (Saliency-Based Cropping):**
    *   Fashion photos are often horizontal or square, while Reels are strictly 9:16.
    *   Using **OpenCV Canny Edge Detection** and **Moment Analysis**, the system identifies the "center of interest" (the garment or model) and performs an automated smart-crop to ensure the product is never cut off.
3.  **Cinematic Motion (Ken Burns Effect):**
    *   To make static images feel like video, the engine applies automated slow-zoom and pan effects centered on the detected saliency point.
4.  **Asynchronous Rendering Pipeline:**
    *   Video encoding is CPU-intensive. The architecture uses **Celery** and **Redis** to handle rendering in the background, allowing the user to continue managing other projects.

---

##  Tech Stack

### Frontend
- **Framework:** React 19 (TypeScript)
- **Build Tool:** Vite
- **Styling:** Vanilla CSS (Modern CSS Variables)
- **Icons:** Lucide React
- **API Client:** Axios

### Backend
- **Framework:** FastAPI (Python)
- **Database:** SQLAlchemy (Asynchronous) with SQLite
- **Task Queue:** Celery
- **Message Broker:** Redis

### Video & CV Engine
- **MoviePy (v2.x):** Video compositing and effects.
- **OpenCV:** Image analysis and saliency detection.
- **PySceneDetect:** Automated video scene analysis.
- **FFmpeg:** Underlying high-efficiency video encoding.

---

## Project Structure

```text
├── backend/            # FastAPI, SQLAlchemy, and Business Logic
│   ├── app/
│   │   ├── api/        # REST Endpoints
│   │   ├── services/   # CV & Video Engines
│   │   ├── models/     # Database Schemas
│   │   └── workers/    # Celery Task Definitions
│   └── tests/          # Pytest Suite
├── frontend/           # React + Vite Dashboard
│   ├── src/
│   │   ├── components/ # UI Components
│   │   ├── api/        # Axios Integration
│   │   └── types/      # TypeScript Definitions
│   └── __tests__/      # Vitest Suite
├── docker-compose.yml  # Infrastructure (Redis)
└── FEATURES.md         # Detailed Technical Specs
```

---

## Getting Started

### 1. Prerequisites
- Python 3.10+
- Node.js 18+
- Docker (for Redis)

### 2. Infrastructure Setup
Start the message broker:
```bash
docker-compose up -d
```

### 3. Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --port 8001
```

### 4. Background Worker Setup
In a new terminal (with venv activated):
```bash
cd backend
celery -A app.workers.celery_app.celery_app worker --loglevel=info
```

### 5. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```
*The dashboard will be available at: http://localhost:5173*

---

## ✅ Validation & Testing

### Backend Tests
```bash
cd backend
PYTHONPATH=. pytest tests/
```

### Frontend Tests
```bash
cd frontend
npm test
```

---

## 🗺️ Roadmap
 **Smart-cropping** using saliency maps.
 **Asynchronous Task Queue** for video rendering.
 **Web Dashboard** for project management.
 **AI Virtual Try-On (VTON):** Allow users to "dress" models in the reference video with uploaded product images.
 **AI Background Removal:** Integration with SAM/RMBG for cleaner product looks.
 **S3 Integration:** Move from local storage to cloud-based object storage.
 **Audio Beat Sync:** Precise transition timing based on audio transients.


