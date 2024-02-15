from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db, Base
import pytest
from alembic import command

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<IPAddress/hostname>/<database name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# def overrid_get_db():
#     db = TestingSessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()
#
#
# app.dependency_overrides[get_db] = overrid_get_db

@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    print("hi under session")
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def client(session):
    # run our code before we run our test
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)
    # command.downgrade("base")
    # command.upgrade("head")
    print("hi under client")
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

    # run our code after our test finishes
    # Base.metadata.drop_all(bind=engine)