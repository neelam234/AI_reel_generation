from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import List
import uuid

router = APIRouter()

# In-memory storage for MVP POC (to be replaced by DB)
projects_db = {}

class ProjectCreate(BaseModel):
    title: str

class Project(BaseModel):
    id: str
    title: str
    status: str = "created"
    reference_video: str = None
    product_images: List[str] = []

@router.post("/", response_model=Project)
async def create_project(project_data: ProjectCreate):
    project_id = str(uuid.uuid4())
    project = Project(id=project_id, title=project_data.title)
    projects_db[project_id] = project
    return project

@router.get("/{project_id}", response_model=Project)
async def get_project(project_id: str):
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    return projects_db[project_id]

@router.post("/{project_id}/upload-reference")
async def upload_reference(project_id: str, file: UploadFile = File(...)):
    if project_id not in projects_db:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Logic to save file locally/S3 would go here
    filename = f"ref_{project_id}_{file.filename}"
    projects_db[project_id].reference_video = filename
    return {"message": f"Uploaded {file.filename}", "project_id": project_id}
