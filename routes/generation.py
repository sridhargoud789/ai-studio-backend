# routes/generation.py
from fastapi import APIRouter, Depends, File, UploadFile, Form
from sqlalchemy.orm import Session
from database import get_db
from models import Generation
from routes.deps import get_current_user
import shutil, os, random, time

router = APIRouter(prefix="/generation", tags=["Generation"])

UPLOAD_DIR = "static/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/create")
async def create_generation(
    prompt: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Simulate "AI generation"
    time.sleep(2)
    simulated_result = f"{UPLOAD_DIR}/result_{random.randint(1,3)}.jpg"

    generation = Generation(
        prompt=prompt, image_path=simulated_result, owner_id=current_user.id
    )
    db.add(generation)
    db.commit()
    db.refresh(generation)

    return {"message": "Generation completed", "result": simulated_result}

@router.get("/recent")
def recent_generations(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    gens = (
        db.query(Generation)
        .filter(Generation.owner_id == current_user.id)
        .order_by(Generation.created_at.desc())
        .limit(5)
        .all()
    )
    return gens
