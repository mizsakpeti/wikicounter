"""
Counting logic for the wikicounter project.

@author: MizsakPeti
"""

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
    limit_percent: float = 0,
    *,
    ordered: bool = True,
) -> dict[str, WordFrequency]:
    """
    Creates a frequency dictionary from a Counter object.

    Args:
        word_counter (Counter): A Counter object containing word counts.
        limit_percent (float): The percentage of the total count to consider for frequency calculation.
        ordered (bool): If True, the dictionary will be sorted by word count in descending order.

    Returns:
        dict[str, WordFrequency]: A dictionary mapping words to their WordFrequency.
    """
    total_count = sum(word_counter.values())
    limit_count = (total_count * limit_percent) / 100

    frequency_dict = {}
    for word, count in word_counter.items():
        if count >= limit_count:
            frequency_dict[word] = WordFrequency(
                word_count=count,
                frequency_percent=(count / total_count) * 100,
            )

    if ordered:
        frequency_dict = dict(
            sorted(frequency_dict.items(), key=lambda item: item[1].word_count, reverse=True),
        )

    return frequency_dict
