import hmac

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.api import api_router
from app.core.config import settings
from app.core.seed import init_db

app = FastAPI(
    title="AI Personal Trainer API",
    description="Backend API for AI-powered personal trainer application",
    version="1.0.0"
)


@app.on_event("startup")
def on_startup():
    # Create tables and seed the Gahan user.
    init_db()


# Shared-secret gate. Protects /api/* when ACCESS_PASSWORD is set. CORS
# preflight (OPTIONS) and public routes (/, /health) always pass through.
@app.middleware("http")
async def access_gate(request: Request, call_next):
    if (
        settings.ACCESS_PASSWORD
        and request.method != "OPTIONS"
        and request.url.path.startswith("/api/")
    ):
        provided = request.headers.get("x-app-password", "")
        if not hmac.compare_digest(provided, settings.ACCESS_PASSWORD):
            return JSONResponse(status_code=401, content={"detail": "Invalid or missing access password."})
    return await call_next(request)


# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_origin_regex=settings.ALLOWED_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "AI Personal Trainer API is running!"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
