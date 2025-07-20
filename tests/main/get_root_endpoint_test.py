"""Test for the root endpoint of the FastAPI application."""

from fastapi.testclient import TestClient


def test_forward_to_docs(client: TestClient):
    """Test that the root endpoint redirects to /docs."""
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/docs"
