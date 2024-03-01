from fastapi.testclient import TestClient
from app.main import app
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app.database import get_db
import pytest

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine)

#we are fixing the scope of the fixture to module is because by default it is function which means that the fixture will
#for each function but in case of module the fixture will be executed only once the test file get executed.
#we can even use package of session
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
#here when we are trying to create a data multiple times it will run into issues to resolve this we use fixtures
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