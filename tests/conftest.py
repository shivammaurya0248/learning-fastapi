from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db, Base
import pytest
from app import models
from app.oauth2 import create_access_token
from alembic import command

# SQLALCHEMY_DATABASE_URL = 'postgresql://<username>:<password>@<IPAddress/hostname>/<database name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:5433/{settings.database_name}_test'

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
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

    # run our code after our test finishes
    # Base.metadata.drop_all(bind=engine)

@pytest.fixture
def test_user2(client):
    user_data = {
        'email': "hello1234@gmail.com",
        'password': "password123"
    }
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    data = res.json()
    data['password'] = user_data['password']
    return data


@pytest.fixture
def test_user(client):
    user_data = {
        'email': "hello123@gmail.com",
        'password': "password123"
    }
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    data = res.json()
    data['password'] = user_data['password']
    return data


@pytest.fixture
def token(test_user):
    return create_access_token(data={'user_id': test_user['id']})


@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        'Authorization': f'Bearer {token}',
    }
    return client


@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [
        {
            "title": "first title",
            "content": "first content",
            "owner_id": test_user['id'],
        }, {
            "title": "second title",
            "content": "second content",
            "owner_id": test_user['id'],
        }, {
            "title": "third title",
            "content": "third content",
            "owner_id": test_user['id'],
        },
        {
            "title": "fourth title",
            "content": "fourth content",
            "owner_id": test_user2['id'],
        },
    ]

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)
    session.add_all(posts)
    session.commit()
    posts = session.query(models.Post).all()
    return posts
