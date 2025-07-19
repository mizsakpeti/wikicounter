"""

Module to connect to a wikipedia API and retrieve page content.

`Wikipedia-API <https://pypi.org/project/wikipedia-api/>`_ is used to connect to the MediaWiki API.
"""

import logging
from collections import Counter
from typing import NamedTuple

from wikipediaapi import Wikipedia

from wikicounter.counting import count_words

wiki_wiki = Wikipedia(user_agent="WikiCounterBot (peter@mizsak.hu)", language="en")

__logger = logging.getLogger(__name__)


class PageContent(NamedTuple):
    """NamedTuple to represent the content and links of a Wikipedia page."""

    page_text: str
    links: list[str]


def get_page_content(page_title: str) -> PageContent:
    """
    Fetches the content of a Wikipedia page by its title.

    Args:
        page_title (str): The title of the Wikipedia page.

    Returns:
        PageContent: A named tuple containing the page content and a list of links found on the page.
    """
    page = wiki_wiki.page(page_title)

    if not page.exists():
        __logger.warning("Page '%s' does not exist or is not unique.", page_title)
        return PageContent("", [])

    # Only keep links where namespace == 0 (wikipedia articles)
    article_links = [title for title, link in page.links.items() if link.namespace == 0]
    return PageContent(page.text, article_links)


def walk_pages(
    page_title: str,
    max_depth: int,
    depth: int = 0,
    word_counter: Counter | None = None,
    visited: set[str] | None = None,
) -> Counter:
    """
    Recursively walks through Wikipedia pages starting from a given page title.

    Args:
        page_title (str): The title of the starting Wikipedia page.
        max_depth (int): The maximum depth to traverse.
        depth (int, optional): The current depth in the traversal. Defaults to 0.
        word_counter (Counter | None, optional): A Counter object to accumulate word counts. Defaults to None.
        visited (set[str] | None, optional): A set of visited page titles to avoid cycles. Defaults to None.

    Returns:
        Counter: A Counter object containing the word counts from all visited pages.
    """
    if visited is None:
        visited = set()

    if word_counter is None:
        word_counter = Counter()

    visited.add(page_title)
    content, links = get_page_content(page_title)
    word_counter += count_words(content, ignore_words=set())
    __logger.debug("Visited: '%s' (depth: %d)", page_title, depth)
    __logger.debug("Number of links found: %d", len(links))

    # TODO: parallelize this to speed up the process
    for link in links:
        if link not in visited and (depth + 1) <= max_depth:
            word_counter = walk_pages(link, max_depth, depth + 1, word_counter, visited)
    return word_counter
