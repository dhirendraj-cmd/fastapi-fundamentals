import secrets, uuid
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import JWTError, jwt
from sqlmodel import Session, select
from app.account.models import RefreshToken, User


SECRET_KEY = secrets.token_hex(32)
ALGORITHM = "HS256"
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated='auto')


def now_utc():
    return datetime.now(timezone.utc)


def hash_password(password: str):
    return bcrypt_context.hash(password)


def verify_password(plain_password, hashed_password):
    return bcrypt_context.verify(plain_password, hashed_password)


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = now_utc() + (expires_delta or timedelta(minutes=15))
    to_encode.update({
        "exp": expire
    })
    print("SECRET_KEY >>>> ", SECRET_KEY)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)



def create_tokens(session: Session, user: User):
    access_token = create_access_token(data={
        "sub": str(user.id)
    })
    refresh_token_str = str(uuid.uuid4())
    expires_at = now_utc() + timedelta(days=7)
    refresh_token = RefreshToken(
        user_id = user.id,
        token = refresh_token_str,
        expires_at=expires_at
    )
    session.add(refresh_token)
    session.commit()
    return {
        'access_token': access_token,
        'refresh_token': refresh_token_str,
        'token_type': "bearer"
    }

def verify_refresh_token(session: Session, token: str):
    stmt = select(RefreshToken).where(RefreshToken.token == token)
    db_token = session.exec(stmt).first()
    if db_token and not db_token.revoked:
        expires_at = db_token.expires_at
        if expires_at.tzinfo is None:
            expires_at = expires_at.replace(tzinfo=timezone.utc)
        if expires_at > now_utc():
            stmt = select(User).where(User.id == db_token.user_id)
            return session.exec(stmt).first()
    return None


def decode_token(token: str):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except JWTError:
        return None






