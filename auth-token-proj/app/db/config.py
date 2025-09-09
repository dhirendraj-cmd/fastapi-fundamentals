import os
from fastapi import Depends
from typing import Annotated
from sqlmodel import SQLModel, Session, create_engine


BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

db_path = os.path.join(BASE_DIR, "authcheck.db")

DATABASE_URL = f"sqlite:///{db_path}"

engine = create_engine(DATABASE_URL, echo=True)  #keep echo=false in prod


def create_tables():
    print("Table created, check in db")
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


SessionDepends = Annotated[Session, Depends(get_session)]

