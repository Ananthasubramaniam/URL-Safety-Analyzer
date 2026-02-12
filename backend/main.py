from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from backend.routers import url_routes, email_routes

from backend.database import engine, Base


Base.metadata.create_all(bind=engine)


app = FastAPI(title="PhishGuard API")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(url_routes.router, prefix="/api")
app.include_router(email_routes.router, prefix="/api")


@app.get("/")
def root():
    return {"message": "PhishGuard backend running"}


