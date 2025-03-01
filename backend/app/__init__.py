from fastapi import FastAPI
from app.routes import router

# Create FastAPI application with metadata
app = FastAPI(
    title="Shop API",
    description="REST API for shop management system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
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

# Include router with prefix and tags
app.include_router(
    router,
    prefix="",
    tags=["accounts operations"]
)
