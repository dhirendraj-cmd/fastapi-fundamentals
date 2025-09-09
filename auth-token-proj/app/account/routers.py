from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Request
from app.db.config import SessionDepends
from app.account.services import create_user, authenticate_user
from app.account.models import UserCreate, UserOut
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.account.helper import create_tokens, verify_refresh_token
from fastapi.responses import JSONResponse

router = APIRouter(prefix="/account", tags=["Account"])


@router.post("/register", response_model=UserOut)
def register(session: SessionDepends, user: UserCreate):
    return create_user(session, user)


@router.post("/login")
def user_login(session: SessionDepends, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid Credentials")
    tokens = create_tokens(session, user)
    response = JSONResponse(content={
        "access_token": tokens["access_token"]
    })
    response.set_cookie("refresh_token", tokens['refresh_token'], httponly=True, secure=True, samesite="Lax", max_age=60*60*24*7)
    return response


@router.post("/refresh")
def refresh_token(session: SessionDepends, request: Request):
    token = request.cookies.get('refresh_token')
    if not token:
        raise HTTPException(status_code=401, detail="Refresh Token is missing")
    user = verify_refresh_token(session, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    return create_tokens(session, user)








