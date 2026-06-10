import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from backend.app.database import engine, Base
from backend.app.models import Scheme
from backend.app.routes import auth, chat, schemes
from backend.app.agents.coordinator import get_all_schemes_list
from backend.app.database import SessionLocal

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="JanMitra AI Backend",
    description="Agentic AI + RAG Government Scheme Eligibility Assistant API",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for local dev/testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Seed database on startup
@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        # Loading schemes lists triggers database check & seed from JSON file
        schemes_list = get_all_schemes_list(db)
        print(f"Loaded {len(schemes_list)} schemes into JanMitra database.")
    except Exception as e:
        print(f"Startup database seeding error: {e}")
    finally:
        db.close()

# Include routes
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(schemes.router)

# Mount static files folder (for serving reports and static assets)
static_dir = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    return {"message": "Welcome to JanMitra AI API. Refer to /docs for Swagger UI documentation."}

if __name__ == "__main__":
    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)
