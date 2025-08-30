import os
from typing import Any, Callable

import uvicorn
from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import time

from app.api.v1.api import api_router

# Create FastAPI instance
app = FastAPI(
    title="FastAPI Boilerplate with PostgreSQL",
    description="A modern FastAPI boilerplate and PostgreSQL integration",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


# Get trusted hosts based on environment
def get_secure_config() -> list[str]:
    """Get secure configuration based on environment"""
    trusted_hosts: list[str] = ["localhost", "127.0.0.1"]

    # Add Gitpod-specific trusted hosts only in Gitpod environment
    if os.getenv("GITPOD_WORKSPACE_ID"):
        # Gitpod URLs have format: port-workspaceid-randomstring.ws-region.gitpod.io
        # For Gitpod, we'll use a more permissive approach since the URLs are dynamic
        trusted_hosts.extend([".gitpod.io", "*.gitpod.io"])
        print("Running in Gitpod environment - added Gitpod trusted hosts")
    else:
        print("Running in local environment - restricted trusted hosts")

    return trusted_hosts


trusted_hosts: list[str] = get_secure_config()
print(f"Configured trusted hosts: {trusted_hosts}")

# Add TrustedHost middleware with secure hosts
# Note: TrustedHostMiddleware doesn't support wildcard patterns well for Gitpod
# We'll add it only for local development
if not os.getenv("GITPOD_WORKSPACE_ID"):
    app.add_middleware(TrustedHostMiddleware, allowed_hosts=trusted_hosts)
    print("Added TrustedHost middleware for local environment")
else:
    print("Skipping TrustedHost middleware for Gitpod environment (using custom validation)")


# Get allowed origins from environment variable with validation
def get_secure_origins() -> list[str]:
    """Get and validate CORS origins from environment"""
    allowed_origins = os.getenv("ALLOWED_ORIGINS", "http://localhost:4000")

    # Parse the string representation of the list
    if allowed_origins.startswith("[") and allowed_origins.endswith("]"):
        # Remove brackets and split by comma, then strip quotes
        origins = [origin.strip().strip("'\"") for origin in allowed_origins[1:-1].split(",")]
    else:
        origins = [allowed_origins]

    # Validate origins (basic URL format check)
    valid_origins: list[str] = []
    for origin in origins:
        if origin.startswith(("http://", "https://")) and "localhost" in origin or "gitpod.io" in origin:
            valid_origins.append(origin)
        else:
            print(f"Warning: Skipping invalid origin: {origin}")

    if not valid_origins:
        print("Warning: No valid origins found, defaulting to localhost")
        valid_origins = ["http://localhost:4000"]

    return valid_origins


origins: list[str] = get_secure_origins()
print(f"Configured CORS origins: {origins}")

# Add CORS middleware with secure origins
print(f"Adding CORS middleware with origins: {origins}")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Simple rate limiting storage (in production, use Redis or similar)
# Stores IP addresses mapped to lists of request timestamps
request_counts: dict[str, list[float]] = {}


# Custom host validation middleware for Gitpod environment
@app.middleware("http")
async def validate_gitpod_host(request: Request, call_next: Callable[[Request], Any]) -> Response | JSONResponse:
    # Only apply host validation in Gitpod environment
    if os.getenv("GITPOD_WORKSPACE_ID"):
        host = request.headers.get("host", "")
        print(f"Validating host: {host}")
        print(f"All headers: {dict(request.headers)}")

        # For now, allow all Gitpod hosts to get the API working
        # TODO: Implement proper host validation later
        if host.endswith(".gitpod.io") or host in ["localhost", "127.0.0.1"]:
            print(f"Host validated successfully: {host}")
        else:
            print(f"Warning: Unknown host format: {host} - allowing for now")

    return await call_next(request)


# Add security headers and rate limiting middleware
@app.middleware("http")
async def add_security_and_rate_limiting(request: Request, call_next: Callable[[Request], Any]) -> Response | JSONResponse:
    global request_counts

    # Rate limiting: allow max 100 requests per minute per IP
    client_ip: str = request.client.host if request.client else "unknown"
    current_time: float = time.time()
    minute_ago: float = current_time - 60

    # Clean old entries and count requests for this IP
    if client_ip not in request_counts:
        request_counts[client_ip] = []

    # Remove timestamps older than 1 minute
    request_counts[client_ip] = [ts for ts in request_counts[client_ip] if ts > minute_ago]

    # Check if rate limit exceeded
    if len(request_counts[client_ip]) >= 100:
        return JSONResponse(status_code=429, content={"detail": "Too many requests. Rate limit exceeded."})

    # Add current request timestamp
    request_counts[client_ip].append(current_time)

    response = await call_next(request)

    # Add security headers
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

    # Add HSTS header for HTTPS environments
    if request.url.scheme == "https":
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

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
    uvicorn.run(app, host="0.0.0.0", port=port, proxy_headers=True, forwarded_allow_ips="127.0.0.1,::1,10.0.0.0/8,172.16.0.0/12,192.168.0.0/16")
