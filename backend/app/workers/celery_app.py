from celery import Celery
from app.core.config import settings
import os
import asyncio
from sqlalchemy import update
from app.core.database import SessionLocal
from app.models.project import Project as ProjectModel
from app.services.video_engine import video_engine

celery_app = Celery(
    "worker",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

celery_app.conf.task_routes = {
    "app.workers.celery_app.generate_reel_task": "main-queue",
}

@celery_app.task(name="app.workers.celery_app.generate_reel_task", bind=True, max_retries=3)
def generate_reel_task(self, project_id: str, ref_video: str, product_images: list):
    """
    Celery task to generate a reel.
    """
    print(f"Starting Celery task for project {project_id}")
    output_path = os.path.join("data", "uploads", project_id, "output_reel.mp4")
    
    try:
        # Run the blocking video generation
        video_engine.generate_reel(ref_video, product_images, output_path)
        
        # Update database status (using sync-over-async or a sync session if needed)
        # Since this is a worker, we can run a small event loop to handle the async DB update
        async def update_db():
            async with SessionLocal() as db:
                await db.execute(
                    update(ProjectModel)
                    .where(ProjectModel.id == project_id)
                    .values(status="completed", output_video=output_path)
                )
                await db.commit()
        
        asyncio.run(update_db())
        return {"status": "completed", "output_path": output_path}

    except Exception as e:
        print(f"Error in Celery task for {project_id}: {e}")
        
        # Update status to failed in DB
        async def mark_failed():
            async with SessionLocal() as db:
                await db.execute(
                    update(ProjectModel)
                    .where(ProjectModel.id == project_id)
                    .values(status="failed")
                )
                await db.commit()
        
        asyncio.run(mark_failed())
        
        # Retry logic
        raise self.retry(exc=e, countdown=60) # Retry after 1 minute
