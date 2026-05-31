from fastapi import APIRouter, UploadFile, File, HTTPException, BackgroundTasks, Depends
from pydantic import BaseModel, ConfigDict
from typing import List, Optional
import uuid
import os
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from app.core.database import get_db
from app.models.project import Project as ProjectModel
from app.services.storage import storage_service
from app.services.video_engine import video_engine

router = APIRouter()

class ProjectCreate(BaseModel):
    title: str

class ProjectSchema(BaseModel):
    id: str
    title: str
    status: str
    reference_video: Optional[str] = None
    product_images: List[str] = []
    output_video: Optional[str] = None
    
    model_config = ConfigDict(from_attributes=True)

@router.post("/", response_model=ProjectSchema)
async def create_project(project_data: ProjectCreate, db: AsyncSession = Depends(get_db)):
    project = ProjectModel(
        id=str(uuid.uuid4()),
        title=project_data.title,
        status="created",
        product_images=[]
    )
    db.add(project)
    await db.commit()
    await db.refresh(project)
    return project

@router.get("/{project_id}", response_model=ProjectSchema)
async def get_project(project_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProjectModel).where(ProjectModel.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.post("/{project_id}/upload-reference")
async def upload_reference(project_id: str, file: UploadFile = File(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProjectModel).where(ProjectModel.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    file_path = await storage_service.save_reference_video(project_id, file)
    
    project.reference_video = str(file_path)
    await db.commit()
    
    return {"message": f"Uploaded {file.filename}", "path": str(file_path)}

@router.post("/{project_id}/upload-images")
async def upload_images(project_id: str, files: List[UploadFile] = File(...), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProjectModel).where(ProjectModel.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    uploaded_paths = []
    for file in files:
        file_path = await storage_service.save_product_image(project_id, file)
        uploaded_paths.append(str(file_path))
    
    # Update project product_images (SQLAlchemy JSON column)
    current_images = list(project.product_images) if project.product_images else []
    current_images.extend(uploaded_paths)
    project.product_images = current_images
    
    await db.commit()
        
    return {"message": f"Uploaded {len(files)} images", "paths": uploaded_paths}

from app.workers.celery_app import generate_reel_task

@router.post("/{project_id}/generate")
async def generate_reel(project_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ProjectModel).where(ProjectModel.id == project_id))
    project = result.scalar_one_or_none()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    if not project.reference_video or not project.product_images:
        raise HTTPException(status_code=400, detail="Missing reference video or product images")

    # Update status
    project.status = "processing"
    await db.commit()
    
    # Trigger Celery Task
    generate_reel_task.delay(project_id, project.reference_video, list(project.product_images))
    
    return {"message": "Reel generation queued via Celery", "project_id": project_id}
