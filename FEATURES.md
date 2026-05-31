# AI Fashion Reel Generator - Features & Technical Specification

## 1. Project Overview
The AI Fashion Reel Generator is a specialized tool designed for fashion boutiques to automate the creation of high-quality, 9:16 Instagram Reels. It uses traditional Computer Vision (CV) and Digital Signal Processing (DSP) to achieve professional results without the high cost and latency of generative AI models.

## 2. Core Features

### 🎞️ Intelligent Scene Matching
- **Reference Video Analysis:** Automatically detects scene changes and transition timings in a reference "vibe" video.
- **Dynamic Pacing:** Matches the duration of product images to the rhythm of the reference video.

### ✂️ Smart Visual Processing
- **Saliency-Based Cropping:** Uses OpenCV Canny edge detection and moment analysis to identify the "center of interest" in product photos.
- **Auto-9:16 Reframing:** Automatically crops and scales horizontal or square photos into a vertical 9:16 format while keeping the product centered.
- **Ken Burns Effect:** Adds subtle, automated zoom and pan animations to static images to make them feel cinematic.

### 🏗️ Robust Backend Architecture
- **Asynchronous Processing:** Heavy video rendering is offloaded to a background task queue to keep the user interface responsive.
- **Persistent Storage:** All project data, asset paths, and rendering statuses are saved in a structured database.
- **Scalable Workers:** The system is designed to handle multiple concurrent rendering jobs by scaling worker processes.

## 3. Tech Stack

### Backend & API
- **FastAPI:** High-performance Python web framework for the API layer.
- **SQLAlchemy:** SQL Toolkit and ORM for database interactions.
- **Aiosqlite:** Asynchronous bridge for SQLite (used for MVP persistence).
- **Pydantic:** Data validation and settings management.

### Video & Image Engine
- **MoviePy (v2.x):** Core library for video editing, compositing, and rendering.
- **OpenCV:** Used for traditional CV tasks like edge detection and saliency analysis.
- **PySceneDetect:** Automates the analysis of reference videos to find perfect transition points.
- **FFmpeg:** The underlying engine for high-efficiency video encoding (H.264/AAC).

### Task Management
- **Celery:** Distributed task queue for managing long-running video renders.
- **Redis:** In-memory data structure store used as the message broker for Celery.
- **Docker:** Provides a consistent environment for running Redis and other infrastructure.

## 4. Technical Workflows

### The Rendering Pipeline
1. **Ingestion:** User uploads a reference video and a set of product images.
2. **Analysis:** `PySceneDetect` identifies timestamps for every cut in the reference video.
3. **Framing:** `OpenCV` analyzes each product image to find the optimal crop coordinates.
4. **Assembly:** `MoviePy` creates individual clips, applies motion effects, and stitches them together matching the reference timings.
5. **Encoding:** The final reel is rendered using FFmpeg with optimized settings for Instagram/TikTok.

## 5. Quality Assurance (Testing)
The project includes a comprehensive test suite to ensure architectural stability:
- **Backend (Pytest):** 
    - Unit tests for `VideoEngine` (Smart Cropping logic verification).
    - API Integration tests using in-memory SQLite (`aiosqlite`) to verify project lifecycles.
    - Mocked task queueing to test API responses without full rendering overhead.
- **Frontend (Vitest):**
    - Component rendering tests for the main Dashboard.
    - Integration checks for API service communication.

## 6. Roadmap
- [x] **Web Dashboard:** A modern React-based interface for project management and asset uploads.
- [ ] **AI Virtual Try-On (VTON):** 
    *   **Goal:** Allow users to upload a flat-lay product image and have it realistically "worn" by the model in the reference video.
    *   **Technology:** IDM-VTON (High fidelity) or CatVTON (Efficiency).
    *   **Implementation Strategy:** A hybrid approach using Cloud APIs (e.g., Fashn.ai, Replicate) for initial scale, or a dedicated GPU-accelerated Celery worker for local processing.
    *   **Challenges:** Maintaining temporal consistency in video to prevent garment flickering during motion.
- [ ] **S3 Integration:** Move from local storage to cloud-based object storage.
- [ ] **AI Background Removal:** Integrate SAM or RMBG-1.4 for cleaner studio looks.
- [ ] **Beat Sync:** Add audio analysis to sync transitions precisely with drum hits.
