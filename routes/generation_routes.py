# routes/generation_routes.py
from fastapi import APIRouter, UploadFile, Form, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Generation
from auth import get_current_user
import os, shutil, uuid

router = APIRouter(prefix="/generation", tags=["Generation"])

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/create")
def create_generation(
    file: UploadFile,
    prompt: str = Form(...),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user),
):
    filename = f"{uuid.uuid4()}_{file.filename}"
    filepath = os.path.join(UPLOAD_DIR, filename)
    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    filepath = filepath.replace("\\", "/")
    gen = Generation(user_id=current_user.id, prompt=prompt, image_path=filepath)
    db.add(gen)
    db.commit()
    db.refresh(gen)
    return {"message": "Generated successfully", "generation_id": gen.id}

@router.get("/recent")
def get_recent(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    gens = (
        db.query(Generation)
        .filter(Generation.user_id == current_user.id)
        .order_by(Generation.created_at.desc())
        .limit(5)
        .all()
    )
    return gens
