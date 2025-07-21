"""Counting logic for the wikicounter project."""

from collections import Counter
from collections.abc import Iterable
from typing import NamedTuple


class WordFrequency(NamedTuple):
    """A named tuple to represent word occurrences and their frequency."""

    word_count: int
    frequency_percent: float

    def __str__(self) -> str:
        """String representation of the WordFrequency for display."""
        return f"{self.word_count} ({self.frequency_percent:.2f}%)"


def count_words(text: str, ignore_words: Iterable[str] | None = None) -> Counter:
    """
    Counts the number of words in a given text.

    The function normalizes the words by converting them to lowercase and stripping punctuation.
    Ignored words can be specified to exclude them from the count.

    Args:
        text (str): The input text to count words from.
        ignore_words (Iterable[str] | None): A list of words to ignore in the count.

    Returns:
        Counter: A Counter object containing words and their counts.
    """
    if ignore_words is None:
        ignore_words = set()

    return Counter(
        _normalize_word(word) for word in text.split() if _normalize_word(word) not in ignore_words
    )


def _normalize_word(text: str) -> str:
    """Normalizes a word by converting it to lowercase and stripping punctuation."""
    return text.lower().strip(".,!?()[]{}\"'")
    # TODO: DEFINE WORD! How to handle special characters from Wikipedia?
    # - \\lambda
    # - \\times
    # - ===
    # NLTK?


def create_frequency_dict(
    word_counter: Counter,
    percentile: float = 0,
) -> dict[str, WordFrequency]:
    """
    Creates a frequency dictionary from a word counter.

    If `percentile` is specified, only words in the top X percentile by frequency are included.
    If `percentile` is set to 90, only the top 10% of words by frequency will be included.

    Args:
        word_counter (Counter): Counter object with word counts.
        percentile (float): Only include words in the top X percentile by frequency.

    Returns:
        dict[str, WordFrequency]: A dictionary mapping words to their frequency information.
    """
    total_words = sum(word_counter.values())
    sorted_words = word_counter.most_common()

    # Calculate how many words to keep based on percentile
    if percentile > 0:
        # Convert percentile to actual number of items to keep
        num_unique_words = len(sorted_words)
        keep_count = _calculate_keep_count(num_unique_words, percentile)
        sorted_words = sorted_words[:keep_count]

    return {
        word: WordFrequency(count, round((count / total_words) * 100, 4))
        for word, count in sorted_words
    }


def _calculate_keep_count(item_count: int, percentile: float) -> int:
    """Calculate the number of items to keep based on the specified percentile."""
    return max(1, int((item_count + 1) * (100 - percentile) / 100))
