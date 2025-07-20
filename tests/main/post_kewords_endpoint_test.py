"""Tests for the keywords - POST endpoint in the Wikicounter application."""

import pytest
from fastapi.testclient import TestClient

# MARK: Parameter Validation Tests


def test_keywords__invalid_percentile(client: TestClient):
    """Test that providing an invalid percentile returns a validation error."""
    request_data = {
        "article": "Python",
        "depth": 0,
        "percentile": 101,  # Invalid: should be 0-100
    }
    response = client.post("/keywords", json=request_data)
    assert response.status_code == 422
    error_detail = response.json()["detail"]
    assert any("percentile" in err["loc"] for err in error_detail)


def test_keywords__missing_article(client: TestClient):
    """Test that omitting the required article field returns a validation error."""
    request_data = {
        "depth": 0,
        "percentile": 50,
    }
    response = client.post("/keywords", json=request_data)
    assert response.status_code == 422
    error_detail = response.json()["detail"]
    assert any("article" in err["loc"] for err in error_detail)


# MARK: Endpoint Tests


def test_keywords_endpoint(mock_walk_pages, mock_create_frequency_dict, client: TestClient):
    """Test the keywords endpoint returns the expected response structure."""
    request_data = {
        "article": "Python",
        "depth": 0,
        "ignore_list": ["the", "and", "to"],
        "percentile": 50,
    }
    response = client.post("/keywords", json=request_data)
    assert response.status_code == 200

    data = response.json()
    assert data["start_article"] == "Python"
    assert data["max_depth"] == 0
    assert "word_frequency" in data
    assert isinstance(data["time_elapsed"], float)

    # Verify the mocks were called with correct parameters
    mock_walk_pages.assert_called_once_with("Python", 0, ignore_words=["the", "and", "to"])
    mock_create_frequency_dict.assert_called_once_with(mock_walk_pages.return_value, percentile=50)


def test_keywords_endpoint__minimal_body(
    mock_walk_pages,
    mock_create_frequency_dict,
    client: TestClient,
):
    """Test the keywords endpoint with minimal body (only required fields)."""
    request_data = {
        "article": "Python",
    }
    response = client.post("/keywords", json=request_data)
    assert response.status_code == 200

    data = response.json()
    assert data["start_article"] == "Python"
    assert data["max_depth"] == 0
    assert "word_frequency" in data
    assert isinstance(data["time_elapsed"], float)

    # Verify the mocks were called with correct parameters
    # Defaults: depth is 0, ignore list is None, percentile is 0
    mock_walk_pages.assert_called_once_with("Python", 0, ignore_words=None)
    mock_create_frequency_dict.assert_called_once_with(mock_walk_pages.return_value, percentile=0)


# MARK: Actual API Integration Tests


@pytest.mark.slow
def test_real_keywords_endpoint(client: TestClient):
    """
    Test the keywords endpoint with an actual Wikipedia API call.

    This test makes a real call to the Wikipedia API and validates the response,
    including the 'percentile' and 'ignore list' filtering functionality.
    """
    to_ignore = ["the", "and", "to"]
    request_data = {
        "article": "MSCI",
        "depth": 0,
        "ignore_list": to_ignore,
        "percentile": 90,  # Only keep top 10% most frequent words
    }
    response = client.post("/keywords", json=request_data)
    assert response.status_code == 200

    data = response.json()
    assert data["start_article"] == request_data["article"]
    assert data["max_depth"] == request_data["depth"]
    assert isinstance(data["word_frequency"], dict)
    assert isinstance(data["time_elapsed"], float)

    # Check that the ignore list was applied
    assert all(ignored not in data["word_frequency"] for ignored in to_ignore)

    # Check that the percentile filtering was applied
    assert len(data["word_frequency"]) > 0
    # The last word in the frequency dict have a frequency greater than 1
    assert data["word_frequency"][list(data["word_frequency"].keys())[-1]][0] > 1
