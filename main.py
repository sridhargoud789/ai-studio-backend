# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from database import Base, engine
from routes.auth_routes import router as auth_router
from routes.generation_routes import router as gen_router
from fastapi.staticfiles import StaticFiles



# 👇 Add this
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Studio Backend")

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(gen_router)
