# filepath: /home/minh/codeproject/abc/backend/app/__init__.py
from fastapi import FastAPI
from app.routes import router
from fastapi.middleware.cors import CORSMiddleware

# Create FastAPI application with metadata
app = FastAPI(
    title="API",
    description="REST API for shop management system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

origins = ["http://localhost:5173"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint for API health check
@app.get("/", tags=["health"])
def read_root():
    """
    Root endpoint to check API health
    """
    return {
        "status": "healthy",
        "message": "API is running"
    }

# Include router with /api prefix and tags
app.include_router(
    router,
    prefix="",
    tags=["accounts operations"]
)