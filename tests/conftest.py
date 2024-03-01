# it is a special file used by pytest which allows us to define fixtures which will be accessible to any of the files
# inside the package

from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse
from app.database import Base
from app.database import get_db
import pytest
from app.oauth2 import create_access_token
from app import models

# encoded_password = urllib.parse.quote_plus('abhidharsh@1999')
# databasename = settings.database_name+'_test'
# SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{encoded_password}@{
#     settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
# SQLALCHEMY_DATABASE_URL='postgresql://postgres:{encoded_password}@localhost:5432/fastapi_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

# we are fixing the scope of the fixture to module is because by default it is function which means that the fixture will
# for each function but in case of module the fixture will be executed only once the test file get executed.
# we can even use package of session
# @pytest.fixture(scope="module")


@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
# here when we are trying to create a data multiple times it will run into issues to resolve this we use fixtures
# @pytest.fixture(scope="module")


@pytest.fixture()
def client(session):
    # Base.metadata.drop_all(bind=engine)
    # Base.metadata.create_all(bind=engine)
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)

# create a fixture to create a test user for us to test the login functionality


@pytest.fixture
def test_user(client):
    user_data = {'email': 'abhi@gmail.com', 'password': 'abhi123'}
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {'email': 'abhi1@gmail.com', 'password': 'abhi123'}
    res = client.post('/users/', json=user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user['password'] = user_data['password']
    return new_user

# fixture to generate an access token to test the api's that need authentication


@pytest.fixture
def token(test_user):
    return create_access_token({'user_id': test_user['id']})

# its actually taking the original client and adding the data from the token fixture

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        'Authorization': f'Bearer {token}'
    }
    return client

@pytest.fixture
def test_posts(test_user,test_user2,session):
    posts_data=[{
        'title':'first title',
        'content':'first content',
        'owner_id': test_user['id']
    },{
        'title':'2nd title',
        'content':'2nd content',
        'owner_id': test_user['id']
    },{
        'title':'3rd title',
        'content':'3rd content',
        'owner_id': test_user['id']
    },{
        'title':'4th title',
        'content':'4th content',
        'owner_id': test_user2['id']
    }]
    def create_post_model(posts):
        return models.Post(**posts)
    map_data=map(create_post_model,posts_data)
    create_posts=list(map_data)
    session.add_all(create_posts)
    # session.add_all([models.Post(title='first title',content='first content',owner_id=test_user['id'])],
    #                 [models.Post(title='2nd title',content='2nd content',owner_id=test_user['id'])])
    session.commit()
    posts=session.query(models.Post).all()
    return posts