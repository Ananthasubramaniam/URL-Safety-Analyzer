from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Routers
from routers import url_routes
from routers import email_routes

# Database
from backend.database import engine, Base
from backend.db_models.threat_log import ThreatLog

# ---------- INIT DB ----------
Base.metadata.create_all(bind=engine)

# ---------- APP ----------
app = FastAPI(title="PhishGuard API")

# ---------- CORS ----------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # change to frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- ROUTERS ----------
app.include_router(url_routes.router, prefix="/api")
app.include_router(email_routes.router, prefix="/api")

# ---------- ROOT ----------
@app.get("/")
def root():
    return {"message": "PhishGuard backend running"}

