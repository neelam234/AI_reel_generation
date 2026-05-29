# AI Fashion Reel Generator (Non-AI MVP)

## Project Vision
Automate the creation of 9:16 Instagram reels for fashion boutiques using traditional Computer Vision (CV) and Digital Signal Processing (DSP) instead of heavy AI models.

## Tech Stack
- **Backend:** FastAPI (Python 3.14+)
- **Video Engine:** MoviePy (v2.x) + FFmpeg
- **CV Analysis:** OpenCV (Haar Cascades / Saliency)
- **Scene Detection:** PySceneDetect
- **Database:** PostgreSQL (Planned)
- **Task Queue:** Celery + Redis (Planned for async rendering)

## Architecture
- `backend/app/api`: FastAPI endpoints for uploads and project management.
- `backend/app/services`: Core logic for video processing, scene detection, and image manipulation.
- `backend/app/workers`: Background workers for heavy video rendering.

## Development Principles
1. **Prefer Math over Models:** Use traditional algorithms (Thresholding, FFT, Saliency) to keep the system fast and CPU-friendly.
2. **Surgical Edits:** Maintain a clean separation between API logic and video processing logic.
3. **Async First:** Video rendering is expensive; always handle it in background queues.

## Current Progress
- [x] POC for scene detection and image-to-video generation.
- [x] Smart-cropping using edge-based saliency.
- [x] Basic Ken Burns motion effects.
- [ ] FastAPI structure scaffolding.
- [ ] S3/Local storage integration.

## Future AI Enhancements (Roadmap)
While the MVP uses traditional CV for speed and cost, the following AI modules are planned for future integration:

### 1. Advanced Product Analysis (Object Detection)
- **Tool:** YOLOv8 or MediaPipe.
- **Goal:** Precisely locate garments, jewelry, and faces to ensure perfect 9:16 centering, even in complex photos.

### 2. High-Fidelity Background Removal
- **Tool:** Segment Anything Model (SAM) or RMBG-1.4.
- **Goal:** Automatically remove messy backgrounds and replace them with high-end "Studio" gradients.

### 3. Semantic Scene Matching
- **Tool:** CLIP (OpenAI).
- **Goal:** Analyze the "vibe" of a reference scene (e.g., "outdoor sunset") and automatically pick the best matching product image from the user's catalog.

### 4. Automated Captions & Scripting
- **Tool:** GPT-4o / Gemini 1.5 Pro.
- **Goal:** Generate trendy, fashion-specific captions and overlays based on the visual features of the product.

### 5. AI Beat Sync
- **Tool:** Demucs (Audio Source Separation).
- **Goal:** Isolate the drum/bass track of the reference audio to achieve frame-perfect transition timing.
