from datetime import datetime
import uuid
from clients import cloud_storage
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.client import Base
from api.rate_limiter import limiter
from database.models.team import Team
from database.models.user import User
from database.models.api_key import ApiKey


@pytest.fixture(scope="function")
def db_session(admin_api_key):
    # Use a unique database URL for testing
    SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        team = Team(
            id=uuid.uuid4(),
            name="Admin Test Team",
            active=True,
            created_at=datetime.now(),
        )
        db.add(team)
        db.flush()  # So team.id is available

        user = User(
            id=uuid.uuid4(),
            team_id=team.id,
            email="admin@test.com",
            name="Admin Test User",
            active=True,
            is_admin=True,
            created_at=datetime.now(),
        )
        db.add(user)
        db.flush()

        api_key = ApiKey(
            id=uuid.uuid4(),
            key=admin_api_key,
            user_id=user.id,
            active=True,
            created_at=datetime.now(),
        )
        db.add(api_key)

        db.commit()
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function", autouse=True)
def mock_cloud_storage(monkeypatch):
    def upload_file_to_bucket(**_):
        pass

    def get_bucket_file_url(path):
        return f"https://mock-cloud-storage.com/{path}"

    monkeypatch.setattr(cloud_storage, "upload_file_to_bucket", upload_file_to_bucket)
    monkeypatch.setattr(cloud_storage, "get_bucket_file_url", get_bucket_file_url)


@pytest.fixture(scope="function")
def client(db_session):
    from main import app
    from database.client import get_db

    # Disable rate limiting for tests
    limiter.reset()

    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db

    from fastapi.testclient import TestClient

    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def admin_api_key():
    return "ADMIN_ACCESS_KEY"


@pytest.fixture()
def admin_headers(admin_api_key):
    return {"X-API-Key": admin_api_key}


@pytest.fixture()
def new_team(client, admin_headers):
    def _create_team(team_name):
        create_team_response = client.post(
            "/api/v1/team", json={"name": team_name}, headers=admin_headers
        )
        assert create_team_response.status_code == 201
        team = create_team_response.json()
        assert "id" in team
        return team

    return _create_team


@pytest.fixture()
def new_user(client, admin_headers):
    def _create_user(email, team_id):
        response = client.post(
            f"/api/v1/team/{team_id}/user",
            json={"email": email, "name": "Test User"},
            headers=admin_headers,
        )
        user = response.json()
        return user

    return _create_user


@pytest.fixture()
def new_team_and_user(new_team, new_user):
    def _create_team_and_user(team_name, user_email="mail@test.com"):
        team = new_team(team_name)
        user = new_user(user_email, team["id"])
        return team, user

    return _create_team_and_user
