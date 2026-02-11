from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import url_routes

app = FastAPI(title="PhishGuard API")

# Allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include URL routes
app.include_router(url_routes.router, prefix="/api")

@app.get("/")
def root():
    return {"message": "PhishGuard backend running"}
