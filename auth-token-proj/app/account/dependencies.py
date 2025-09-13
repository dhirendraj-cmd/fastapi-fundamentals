from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from app.db.config import SessionDepends
from app.account.models import User, RefreshToken
from sqlmodel import select
from typing import Annotated
from app.account.helper import decode_token


oauth2_bearer = OAuth2PasswordBearer(tokenUrl="account/login")


def get_current_user(session: SessionDepends, token: Annotated[str, Depends(oauth2_bearer)]):
    payload = decode_token(token)
    print("payload>>>>>>>>>>>. ", payload)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    stmt = select(User).where(User.id == int(payload.get("sub")))
    user = session.exec(stmt).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


def get_all_users(session: SessionDepends):
    all_users = session.exec(select(User)).all()
    return all_users


