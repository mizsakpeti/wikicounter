"""Test cases for the word-frequency GET endpoint in the Wikicounter application."""

import pytest
from fastapi.testclient import TestClient

# MARK: Parameter Validation Tests


def test_word_frequency__with_negative_depth(client: TestClient):
    """Test that providing a negative depth returns a validation error."""
    response = client.get("/word-frequency?article=Python&depth=-1")
    assert response.status_code == 422  # Unprocessable Entity
    assert "depth" in response.json()["detail"][0]["loc"]


def test_word_frequency__with_no_parameters(client: TestClient):
    """Test that providing no parameters returns a validation error."""
    response = client.get("/word-frequency")
    assert response.status_code == 422  # Unprocessable Entity
    assert "article" in response.json()["detail"][0]["loc"]


# MARK: Endpoint Tests


def test_word_frequency_endpoint(mock_walk_pages, mock_create_frequency_dict, client: TestClient):
    """Test the word frequency endpoint returns the expected response structure."""
    response = client.get("/word-frequency?article=Python&depth=0")
    assert response.status_code == 200

    data = response.json()
    assert data["start_article"] == "Python"
    assert data["max_depth"] == 0
    assert "word_frequency" in data
    assert isinstance(data["time_elapsed"], float)

    # Verify the mock was called with correct parameters
    mock_walk_pages.assert_called_once_with("Python", 0)
    mock_create_frequency_dict.assert_called_once()


# MARK: Actual API Integration Tests


@pytest.mark.slow
def test_word_frequency__api_call(client: TestClient):
    """
    Test the word frequency endpoint with an actual Wikipedia API call.

    This test makes a real call to the Wikipedia API and validates the response.
    Skip this test if you want to avoid external API calls in your test suite.
    """
    article = "MSCI"
    response = client.get(f"/word-frequency?article={article}&depth=0")
    assert response.status_code == 200

    data = response.json()
    assert data["start_article"] == article
    assert data["max_depth"] == 0
    assert isinstance(data["word_frequency"], dict)
    assert len(data["word_frequency"]) > 0
    assert isinstance(data["time_elapsed"], float)

    # Check that common words you'd expect in the MSCI article exist
    common_words = ["msci", "index", "capital"]
    found_words = [word for word in common_words if word in data["word_frequency"]]
    assert len(found_words) > 0, f"None of the expected words {common_words} were found"
