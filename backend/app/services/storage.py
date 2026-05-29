import os
import shutil
from pathlib import Path
from fastapi import UploadFile
import uuid

BASE_UPLOAD_DIR = Path("data/uploads")

class StorageService:
    def __init__(self):
        os.makedirs(BASE_UPLOAD_DIR, exist_ok=True)

    def get_project_dir(self, project_id: str) -> Path:
        project_dir = BASE_UPLOAD_DIR / project_id
        os.makedirs(project_dir, exist_ok=True)
        os.makedirs(project_dir / "images", exist_ok=True)
        os.makedirs(project_dir / "videos", exist_ok=True)
        return project_dir

    async def save_reference_video(self, project_id: str, file: UploadFile) -> str:
        project_dir = self.get_project_dir(project_id)
        file_ext = os.path.splitext(file.filename)[1]
        file_path = project_dir / "videos" / f"reference{file_ext}"
        
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return str(file_path)

    async def save_product_image(self, project_id: str, file: UploadFile) -> str:
        project_dir = self.get_project_dir(project_id)
        unique_name = f"{uuid.uuid4()}_{file.filename}"
        file_path = project_dir / "images" / unique_name
        
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        return str(file_path)

storage_service = StorageService()
