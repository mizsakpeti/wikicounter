"""Tests for the counting module."""

from collections import Counter

import pytest

from wikicounter.counting import (
    WordFrequency,
    _normalize_word,
    count_words,
    create_frequency_dict,
)


@pytest.fixture(name="word_counter")
def fixture_word_counter() -> Counter:
    """Fixture for a sample word counter."""
    return Counter({"hello": 5, "world": 3, "test": 2})


def test_count_words__basic() -> None:
    """Test basic word counting functionality with cases, our punctuation, and duplicates."""
    text = "Hello, HELLO world! This is a test. Is it working??"
    result = count_words(text)
    expected = Counter(
        {"hello": 2, "world": 1, "this": 1, "is": 2, "a": 1, "test": 1, "it": 1, "working": 1},
    )
    assert result == expected


def test_count_words__with_excludes():
    """Test word counting with ignored words."""
    text = "Hello, world! This is a test. Is it working??"
    ignore_words = {"hello", "world", "is"}
    result = count_words(text, ignore_words=ignore_words)
    expected = Counter({"this": 1, "a": 1, "test": 1, "it": 1, "working": 1})
    assert result == expected


def test_count_words__empty_string():
    """Test counting words in an empty string."""
    text = ""
    result = count_words(text)
    expected = Counter()
    assert result == expected


@pytest.mark.parametrize(
    ("input_word", "expected"),
    [
        # Lowercase tests
        ("Hello", "hello"),
        ("WORLD", "world"),
        ("TeSt", "test"),
        # Strip punctuation tests
        ("hello,", "hello"),
        ("world!", "world"),
        ("(test)", "test"),
        ('"quote"', "quote"),
        ("[bracket]", "bracket"),
        ("{brace}", "brace"),
        # Complex cases
        ("Hello!", "hello"),
        ("WORLD.", "world"),
        ("(TeSt)", "test"),
    ],
)
def test_normalize_word_various_cases(input_word, expected):
    """Test normalization of words: lowercase, strip punctuation, complex cases."""
    assert _normalize_word(input_word) == expected


@pytest.mark.skip(reason="Wikipedia-specific normalization not implemented yet")
def test_normalize_word_wikipedia_specific():
    """Test handling of specific Wikipedia formatting patterns."""

    # LaTeX-style math notation
    assert _normalize_word("\\\\lambda") == "lambda"
    assert _normalize_word("\\\\times") == "times"

    # Section markers
    assert _normalize_word("===Section===") == "section"

    # Math formula
    assert _normalize_word("$E=mc^2$") == "emc2"


def test_create_frequency_dict__basic(word_counter):
    """Test creating frequency dictionary with basic input and no limit."""
    result = create_frequency_dict(word_counter)
    expected = {
        "hello": WordFrequency(word_count=5, frequency_percent=50),
        "world": WordFrequency(word_count=3, frequency_percent=30),
        "test": WordFrequency(word_count=2, frequency_percent=20),
    }
    assert result == expected


def test_create_frequency_dict__empty_counter():
    """Test creating a frequency dictionary from an empty counter."""
    word_counter = Counter()
    result = create_frequency_dict(word_counter)
    expected = {}
    assert result == expected


def test_create_frequency_dict__with_limit(word_counter):
    """Test that percentile filtering works correctly."""

    # With a limit of 30 percentile, 'test' should be filtered out
    result = create_frequency_dict(word_counter, percentile=30)

    assert "test" not in result
    # The percentage is still calculated based on the total count
    assert result["hello"] == WordFrequency(word_count=5, frequency_percent=50.0)
    assert result["world"] == WordFrequency(word_count=3, frequency_percent=30.0)


def test_create_frequency_dict__with_high_limit(word_counter):
    """Test with a limit that filters out all words."""

    # With a limit of 99, only the most frequent word should remain
    result = create_frequency_dict(word_counter, percentile=99)
    expected = {
        "hello": WordFrequency(word_count=5, frequency_percent=50),
    }

    assert result == expected


def test_create_frequency_dict__with_low_limit(word_counter):
    """Test with a limit that filters out all words."""

    # With a limit of 1, all words should remain
    result = create_frequency_dict(word_counter, percentile=1)
    expected = {
        "hello": WordFrequency(word_count=5, frequency_percent=50),
        "world": WordFrequency(word_count=3, frequency_percent=30),
        "test": WordFrequency(word_count=2, frequency_percent=20),
    }
    assert result == expected
