from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.services.user_service import UserService


router = APIRouter()


@router.post("/google", response_model=UserResponse, status_code=201, summary="Upsert Google user")
async def upsert_google_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = UserService.create_or_update_by_google(db, payload)
    return user


@router.put("/{google_sub}", response_model=UserResponse, summary="Update user by google_sub")
async def update_user(google_sub: str, payload: UserUpdate, db: Session = Depends(get_db)):
    user = UserService.update_by_google_sub(db, google_sub, payload)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

