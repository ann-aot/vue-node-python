from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.schemas.user import UserCreate


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

