# Testing imports
import os
import sys
import pytest

# Adjust the path to import app
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from app import app


@pytest.fixture
def client():
    """
    Creates a test client for the Flask app with testing mode enabled.

    Returns:
        FlaskClient: The test client for the Flask app.
    """
    app.config["TESTING"] = True
    yield app.test_client()


def test_main_route(client):
    """Test the home route."""
    response = client.get("/")

    # Assert the response status code and the title in the response
    assert response.status_code == 200
    assert b"PeekText" in response.data  # Check if the title is in the response


def test_generate_success(client):
    """Test the generate endpoint with a valid URL."""
    response = client.post("/generate", json={"url": "https://example.com"})

    # Assert the response status code and the response message
    assert response.status_code == 200
    assert response.json["status"] == "success"
    assert (
        response.json["response"]
        == "Example Domain\n\nThis domain is for use in illustrative examples in documents. You may use this domain in literature without prior coordination or asking for permission.\nMore information..."
    )
