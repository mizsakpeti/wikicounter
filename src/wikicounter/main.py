"""
Main file for the Wikicounter FastAPI application.

This module sets up the FastAPI application, defines the API endpoints,
and handles requests to retrieve word frequency data from Wikipedia articles.
"""

from time import time
from typing import Annotated

from fastapi import FastAPI, Query
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, Field

from wikicounter import __version__
from wikicounter.counting import WordFrequency, create_frequency_dict
from wikicounter.wiki_connection import walk_pages

app = FastAPI(
    title="WikiCounter API",
    description="API for counting word frequencies in Wikipedia articles",
    version=__version__,
)

# MARK: API Models


class KeywordsRequest(BaseModel):
    """Request model for keywords endpoint."""

    article: str = Field(..., description="Title of the Wikipedia article")
    depth: int = Field(default=0, ge=0, description="Depth of the articles to traverse")
    ignore_list: list[str] | None = Field(None, description="List of words to ignore")
    percentile: int = Field(
        default=0,
        ge=0,
        le=100,
        description="Percentile threshold for word frequency",
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "article": "MSCI",
                    "depth": 1,
                    "ignore_list": ["the", "and", "to"],
                    "percentile": 50,
                },
            ],
        },
    }


class BaseResponse(BaseModel):
    """Base response model for API endpoints."""

    start_article: str
    max_depth: int
    word_frequency: dict[str, WordFrequency]
    time_elapsed: float


class WordFrequencyResponse(BaseResponse):
    """Response model for word frequency endpoint."""


class KeywordsResponse(BaseResponse):
    """Response model for keywords endpoint."""


# MARK: API Endpoints


@app.get("/", include_in_schema=False)
def forward_to_docs() -> RedirectResponse:
    """Redirect to the api documentation."""
    return RedirectResponse(url="/docs", status_code=307)


@app.get("/word-frequency", summary="Get word frequency from a Wikipedia article(s)")
def get_word_frequency(
    article: Annotated[str, Query(description="Title of the Wikipedia article")],
    depth: Annotated[int, Query(description="Depth of the articles to traverse", ge=0)] = 0,
) -> WordFrequencyResponse:
    """Get the word frequency from a Wikipedia article."""
    start_time = time()
    word_counter = walk_pages(article, depth)
    frequency_dict = create_frequency_dict(word_counter)
    elapsed_time = round(time() - start_time, 2)
    return WordFrequencyResponse(
        start_article=article,
        max_depth=depth,
        word_frequency=frequency_dict,
        time_elapsed=elapsed_time,
    )


@app.post("/keywords", summary="Get keywords from a Wikipedia article(s) by filtering")
def get_keywords(request: KeywordsRequest) -> KeywordsResponse:
    """Get the keywords from a Wikipedia article."""
    start_time = time()
    word_counter = walk_pages(request.article, request.depth, ignore_words=request.ignore_list)
    frequency_dict = create_frequency_dict(word_counter, percentile=request.percentile)
    elapsed_time = round(time() - start_time, 2)
    return KeywordsResponse(
        start_article=request.article,
        max_depth=request.depth,
        word_frequency=frequency_dict,
        time_elapsed=elapsed_time,
    )
