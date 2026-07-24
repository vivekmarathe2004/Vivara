import fastapi
import fastapi.middleware.cors as cors
from fastapi.staticfiles import StaticFiles
import pathlib
import sys

_root = pathlib.Path(__file__).parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

from backend.database import engine, Base
from backend.config import settings
from backend.api import projects, generate, jobs, settings as settings_api, media, setup, clip

Base.metadata.create_all(bind=engine)

# Create storage dirs
storage_path = pathlib.Path(__file__).parent.parent / "storage"
storage_path.mkdir(parents=True, exist_ok=True)
(storage_path / "projects").mkdir(exist_ok=True)
(storage_path / "media").mkdir(exist_ok=True)
(storage_path / "output").mkdir(exist_ok=True)
(storage_path / "temp").mkdir(exist_ok=True)
(storage_path / "music").mkdir(exist_ok=True)

app = fastapi.FastAPI(
    title="Vivara API",
    description="Free, open-source AI video studio backend",
    version="2.0.0",
)

app.add_middleware(
    cors.CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve rendered video output as static files
output_dir = storage_path / "output"
output_dir.mkdir(parents=True, exist_ok=True)
app.mount("/output", StaticFiles(directory=str(output_dir)), name="output")

app.include_router(projects.router)
app.include_router(generate.router)
app.include_router(jobs.router)
app.include_router(settings_api.router)
app.include_router(media.router)
app.include_router(setup.router)
app.include_router(clip.router)

@app.on_event("startup")
async def startup_event():
    first_run = not (storage_path / ".setup_complete").exists()
    if first_run:
        print("⚡ Vivara: First run detected — open http://localhost:5173 to complete setup.")
    else:
        print("✓ Vivara backend ready at http://localhost:8000")

@app.get("/api/health")
async def health():
    return {"status": "ok", "version": "2.0.0", "app": "Vivara Studio"}
