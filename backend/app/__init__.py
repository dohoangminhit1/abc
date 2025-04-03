from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router as api_router
from app.redis import connect_to_redis, close_redis_connection

app = FastAPI(
    title="API",
    description="REST API for shop management system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
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

@app.on_event("startup")
async def startup_event():
    await connect_to_redis()  # Kết nối Redis khi ứng dụng khởi động

@app.on_event("shutdown")
async def shutdown_event():
    await close_redis_connection()  # Đóng kết nối Redis khi ứng dụng tắt

@app.get("/", tags=["health"])
def read_root():
    return {
        "status": "healthy",
        "message": "API is running"
    }

app.include_router(api_router)
