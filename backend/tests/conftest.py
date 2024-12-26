import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from app.database import Base
from app.main import app
from app.models import User
from app.auth import get_password_hash, create_access_token
import uuid

# Create test database
TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def engine():
    """Create a test database engine that will be used for all tests"""
    engine = create_engine(
        TEST_SQLALCHEMY_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db(engine):
    """Create a fresh database session for each test"""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()

@pytest.fixture(scope="function")
def client(db):
    """Create a test client with a database dependency override"""
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides["get_db"] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture(scope="function")
def test_user(db):
    """Create a test user and return their credentials"""
    # Generate unique username and email for each test
    unique_id = str(uuid.uuid4())[:8]
    user = User(
        email=f"test_{unique_id}@example.com",
        username=f"testuser_{unique_id}",
        hashed_password=get_password_hash("testpass")
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "password": "testpass"  # Store plain password for test usage
    }

@pytest.fixture(scope="function")
def test_user_token(test_user):
    """Create an authentication token for the test user"""
    access_token = create_access_token(data={"sub": test_user["email"]})
    return {"Authorization": f"Bearer {access_token}"}

@pytest.fixture(autouse=True)
def cleanup_db(db):
    """Cleanup the database after each test"""
    yield
    db.query(User).delete()
    db.commit()