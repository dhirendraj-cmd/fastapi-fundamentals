from typing import List, Optional
from datetime import datetime, timezone
from sqlmodel import SQLModel, Field, UniqueConstraint, Relationship


# def now_utc():
#     return datetime.now(timezone.utc)

class UserBase(SQLModel):
    email: str
    name: str
    is_active: bool = True
    is_admin: bool = False


class UserCreate(UserBase):
    password: str


class UserOut(UserBase):
    id: int


class RefreshToken(SQLModel, table=True):
    # __tablename__ = "refresh_tokens"

    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    token: str
    expires_at: datetime
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    revoked: bool = False

    # relationship back to User
    user: "User" = Relationship(back_populates="refresh_tokens")


class User(UserBase, table=True):
    # __tablename__ = "users"
    __table_args__ = (UniqueConstraint("email"),)
    id: int = Field(primary_key=True)
    hashed_password: str
    is_verified: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    upated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    # relationship to RefreshToken
    refresh_tokens: List[RefreshToken] = Relationship(back_populates="user")

    # back_populates link refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")

    # back_populates link user = relationship("Users", back_populates="refresh_tokens")

    





