"""
Pytest configuration and shared fixtures for backend tests.
"""
import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
def test_user_data() -> dict:
    """Sample user data for testing."""
    return {
        "email": "test@example.com",
        "password": "TestPassword123!",
        "full_name": "Test User",
        "headline": "Test Headline",
    }


@pytest.fixture
def test_profile_data() -> dict:
    """Sample profile data for testing."""
    return {
        "target_role": "Software Engineer",
        "highest_education": "Bachelor",
        "years_experience": 2.0,
    }

