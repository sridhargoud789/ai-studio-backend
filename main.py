# main.py
from fastapi import FastAPI
from database import Base, engine
from routes import auth, generation

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Studio Backend")

app.include_router(auth.router)
app.include_router(generation.router)
