from collections import Counter
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from wikicounter.counting import WordFrequency
from wikicounter.main import app


@pytest.fixture(name="client")
def fixture_client() -> TestClient:
    """Fixture to create a FastAPI test client."""
    return TestClient(app)


# MARK: Mocking Fixtures


@pytest.fixture
def mock_walk_pages():
    """Mock the walk_pages function to avoid actual Wikipedia API calls."""
    with patch("wikicounter.main.walk_pages") as mock:
        # Return a predefined counter for any call
        mock.return_value = Counter({"python": 10, "programming": 8, "language": 5})
        yield mock


@pytest.fixture
def mock_create_frequency_dict():
    """Mock the create_frequency_dict function."""
    with patch("wikicounter.main.create_frequency_dict") as mock:
        # Return a predefined dictionary for any call
        mock.return_value = {
            "python": WordFrequency(word_count=10, frequency_percent=43.48),
            "programming": WordFrequency(word_count=8, frequency_percent=34.78),
            "language": WordFrequency(word_count=5, frequency_percent=21.74),
        }
        yield mock
