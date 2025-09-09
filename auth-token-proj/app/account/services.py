from fastapi import HTTPException
from sqlmodel import select, Session
from app.account.helper import hash_password, verify_password
from app.account.models import User, UserCreate, RefreshToken
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer




def create_user(session: Session, user: UserCreate):
    stmt = select(User).where(User.email == user.email)

    if not session.exec(stmt).first():
        new_user = User(
            email = user.email,
            name = user.name,
            hashed_password=hash_password(user.password),
            is_verified=False
        )

        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user
    else:
        raise HTTPException(status_code=400, detail="This Email is already registered")


def authenticate_user(session: Session, email: str, password: str):
    stmt = select(User).where(User.email == email)
    user = session.exec(stmt).first()
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
