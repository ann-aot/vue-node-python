from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    @staticmethod
    def get_by_google_sub(db: Session, google_sub: str) -> User | None:
        stmt = select(User).where(User.google_sub == google_sub)
        return db.execute(stmt).scalars().first()

    @staticmethod
    def create_or_update_by_google(db: Session, payload: UserCreate) -> User:
        user = UserService.get_by_google_sub(db, payload.google_sub)
        if user is None:
            user = User(
                google_sub=payload.google_sub,
                email=payload.email,
                name=payload.name,
                avatar_url=payload.avatar_url,
                dob=payload.dob,
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            return user

        # Update existing record if any field changed
        changed = False
        if user.email != payload.email:
            user.email = payload.email
            changed = True
        if user.name != payload.name:
            user.name = payload.name
            changed = True
        if user.avatar_url != payload.avatar_url:
            user.avatar_url = payload.avatar_url
            changed = True
        if user.dob != payload.dob:
            user.dob = payload.dob
            changed = True
        if changed:
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

    @staticmethod
    def update_by_google_sub(db: Session, google_sub: str, payload: UserUpdate) -> User | None:
        user = UserService.get_by_google_sub(db, google_sub)
        if user is None:
            return None
        changed = False
        if payload.email is not None and payload.email != user.email:
            user.email = payload.email
            changed = True
        if payload.name is not None and payload.name != user.name:
            user.name = payload.name
            changed = True
        if payload.avatar_url is not None and payload.avatar_url != user.avatar_url:
            user.avatar_url = payload.avatar_url
            changed = True
        if payload.dob is not None and payload.dob != user.dob:
            user.dob = payload.dob
            changed = True
        if changed:
            db.add(user)
            db.commit()
            db.refresh(user)
        return user

