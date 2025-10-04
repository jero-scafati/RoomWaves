from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.routers import upload, plot, parameters, signal

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routers
app.include_router(upload.router, prefix="/api", tags=["upload"])
app.include_router(plot.router, prefix="/api", tags=["plot"])
app.include_router(parameters.router, prefix="/api", tags=["parameters"])
app.include_router(signal.router, prefix="/api", tags=["signal"])

@app.get("/")
def read_root():
    return {"message": f"Hi, welcome to {settings.APP_NAME} API! visit /docs for more information."}