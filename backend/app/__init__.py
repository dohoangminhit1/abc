from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as api_router

# Create FastAPI application with metadata
app = FastAPI(
    title="API",
    description="REST API for shop management system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

origins = [
    "http://localhost:5173",  
    "https://abc-at61.onrender.com",  
    "https://www.abc-at61.onrender.com",
    "https://abc-uwkq.onrender.com",
    "https://www.abc-uwkq.onrender.com" 
]

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

# Include routers with appropriate prefixes and tags
app.include_router(api_router)