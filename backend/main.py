import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.api.v1.api import api_router

# Create FastAPI instance
app = FastAPI(
    title="FastAPI Boilerplate with PostgreSQL",
    description="A modern FastAPI boilerplate and PostgreSQL integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    # Trust proxy headers for Gitpod environment
    root_path_in_servers=True,
)


# Get allowed origins from environment variable
def get_secure_origins() -> list[str]:
    """Get and validate CORS origins from environment"""
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:4000")

    # Parse the string representation of the list
    if allowed_origins.startswith("[") and allowed_origins.endswith("]"):
        # Remove brackets and split by comma, then strip quotes
        origins = [
            origin.strip().strip("'\"") for origin in allowed_origins[1:-1].split(",")
        ]
    else:
        origins = [allowed_origins]

    # Validate origins (basic URL format check)
    valid_origins = []
    for origin in origins:
        if origin.startswith(("http://", "https://")) and (
            "localhost" in origin or "gitpod.io" in origin
        ):
            valid_origins.append(origin)
        else:
            print(f"Warning: Skipping invalid origin: {origin}")

    if not valid_origins:
        print("Warning: No valid origins found, defaulting to localhost")
        valid_origins = ["http://localhost:4000"]

    return valid_origins


origins = get_secure_origins()
print(f"Configured CORS origins: {origins}")

# Add CORS middleware with secure origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


# Add middleware to handle HTTPS scheme for Gitpod environment
@app.middleware("http")
async def handle_https_scheme(request: Request, call_next):
    # Check if we're running in Gitpod environment
    if os.getenv("GITPOD_WORKSPACE_ID"):
        # Log headers for debugging
        print(f"Request headers: {dict(request.headers)}")
        print(f"Request scheme: {request.scope['scheme']}")
        print(f"Request URL: {request.url}")

        # Check for X-Forwarded-Proto header
        forwarded_proto = request.headers.get("x-forwarded-proto")
        if forwarded_proto == "https":
            # Force HTTPS scheme for Gitpod environment
            request.scope["scheme"] = "https"
            print(f"HTTPS scheme enforced for request to: {request.url.path}")

    response = await call_next(request)

    # Force HTTPS URLs in response headers for Gitpod environment
    if os.getenv("GITPOD_WORKSPACE_ID"):
        # Check if there are any Location headers that need to be converted to HTTPS
        if "location" in response.headers:
            location = response.headers["location"]
            if location.startswith("http://") and "gitpod.io" in location:
                https_location = location.replace("http://", "https://")
                response.headers["location"] = https_location
                print(f"Converted Location header from {location} to {https_location}")

    return response


# Include API router
app.include_router(api_router, prefix="/api/v1")


@app.get("/")
async def root():
    return {
        "message": "Welcome to FastAPI Boilerplate with PostgreSQL!",
        "status": "running",
        "docs": "/docs",
        "api": "/api/v1",
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "FastAPI Boilerplate with PostgreSQL",
        "database": "connected (migrations handled by Alembic)",
    }


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8300))
    # Configure uvicorn for Gitpod environment with proxy headers
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        proxy_headers=True,
        forwarded_allow_ips="127.0.0.1,::1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16",
    )
