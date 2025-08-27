from fastapi import APIRouter
from app.api.v1.endpoints import states, workflows

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(states.router, prefix="/states", tags=["states"])
api_router.include_router(workflows.router, prefix="/workflows", tags=["workflows"])
