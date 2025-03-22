import os
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, declarative_base, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")


def check_if_db_exists(name):
    url = "/".join(DATABASE_URL.split("/")[:-1])
    temp_engine = create_engine(url + "/postgres")

    with temp_engine.connect() as connection:
        result = connection.execute(
            text(f"SELECT 1 FROM pg_database WHERE datname = '{name}';")
        )
        return result.fetchone() is not None


def create_database(name):
    url = "/".join(DATABASE_URL.split("/")[:-1])
    temp_engine = create_engine(url + "/postgres")

    with temp_engine.connect().execution_options(
        isolation_level="AUTOCOMMIT"
    ) as connection:
        connection.execute(text(f"CREATE DATABASE {name};"))


db_name = DATABASE_URL.split("/")[-1]

if not check_if_db_exists(db_name):
    create_database(db_name)

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
