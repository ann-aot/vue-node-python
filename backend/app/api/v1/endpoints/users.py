from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services.user_service import UserService


router = APIRouter()


@router.post("/google", response_model=UserResponse, status_code=201, summary="Upsert Google user")
async def upsert_google_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = UserService.create_or_update_by_google(db, payload)
    return user

