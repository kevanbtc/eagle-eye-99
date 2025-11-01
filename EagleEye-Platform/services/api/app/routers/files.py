from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from pathlib import Path
import os
from ..db import get_db
from ..models import File as FileModel

router = APIRouter(prefix="/files", tags=["files"])
STORAGE_DIR = Path(os.getenv("STORAGE_DIR", "/app/storage"))

@router.post("/{project_id}")
async def upload_file(project_id: str, f: UploadFile = File(...), db: Session = Depends(get_db)):
    proj_dir = STORAGE_DIR / project_id
    proj_dir.mkdir(parents=True, exist_ok=True)
    dest = proj_dir / f.filename
    with open(dest, "wb") as out:
        out.write(await f.read())
    rec = FileModel(project_id=project_id, name=f.filename, mime=f.content_type, path=str(dest))
    db.add(rec); db.commit();
    return {"file_id": str(rec.id), "path": str(dest)}
