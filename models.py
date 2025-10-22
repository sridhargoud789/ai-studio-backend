# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import Base, engine
from routes import auth, generation

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Studio Backend")

# Allow frontend (local + deployed)
origins = [
    "http://localhost:3000",       # local Next.js
    "https://your-frontend.vercel.app",  # replace with your deployed frontend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(auth.router)
app.include_router(generation.router)
