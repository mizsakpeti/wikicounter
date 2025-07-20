# WikiCounter 🧮

A Python FastAPI service to analyze word frequencies from Wikipedia articles, with options to traverse linked pages up to a specified depth.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Running the API - Development Mode](#running-the-api---development-mode)
  - [API Endpoints](#api-endpoints)
- [Features](#features)
- [License](#license)
- [Contact](#contact)

## Installation

### From Source

```bash
git clone https://github.com/mizsakpeti/wikicounter.git
cd wikicounter
python -m venv .venv
source .venv/bin/activate  # On Windows use .venv\Scripts\Activate.Ps1
pip install --upgrade pip
pip install -e .
```

## Usage

### Running the API - Development Mode

Start the FastAPI server in development mode:

```bash
# Start the server
fastapi dev src/wikicounter/main.py
```

Once running, you can access:

- API documentation: [http://localhost:8000/docs](http://localhost:8000/docs)
- Alternative documentation: [http://localhost:8000/redoc](http://localhost:8000/redoc)

### API Endpoints

#### 1. Word Frequency Endpoint 📝

Get word frequencies from a Wikipedia article with optional depth traversal.

**Endpoint:** `GET /word-frequency`

**Parameters:**

- `article` (string, required): Title of the Wikipedia article
- `depth` (integer, optional, default=0): Depth of article traversal. 0 means only the specified article, 1 means the article and its direct links, etc.

**Example Request:**

```bash
curl -X 'GET' \
  'http://localhost:8000/word-frequency?article=MSCI&depth=0'
```

**Example Response:**

The response includes the word frequency (count, percentage), the time taken for processing, the article title and the maximum depth reached.

```json
{
  "start_article": "MSCI",
  "max_depth": 0,
  "word_frequency": {
    "the": [
        42,
        5.1345
    ],
    "msci": [
        39,
        4.7677
    ],
    "// ... more words": {}
  },
  "time_elapsed": 0.67
}
```

#### 2. Keywords Filtering Endpoint 🔍

Get filtered keywords from a Wikipedia article with options for ignoring common words and limiting to top percentile.

**Endpoint:** `POST /keywords`

**Request Body:**

```json
{
  "article": "MSCI",
  "depth": 0,
  "ignore_list": ["the", "end", "to", "of", "in", "and", "a", "an"],
  "percentile": 99
}
```

**Example with curl:**

```bash
curl -X 'POST' \
  'http://localhost:8000/keywords' \
  -H 'Content-Type: application/json' \
  -d '{
    "article": "MSCI",
    "depth": 0,
    "ignore_list": ["the", "end", "to", "of", "in", "and", "a", "an"],
    "percentile": 99
  }'
```

**Example Response:**

```json
{
  "start_article": "MSCI",
  "max_depth": 0,
  "word_frequency": {
    "msci": [
      39,
      5.8122
    ],
    "indices": [
      15,
      2.2355
    ],
    "index": [
      11,
      1.6393
    ]
  },
  "time_elapsed": 0.53
}
```

## Features

- 📊 **Word Frequency Analysis:** Count occurrences of words in Wikipedia articles
- 🌐 **Page Traversal:** Follow links to discover related content up to a specified depth
- ⚡ **Fast API:** Built with FastAPI for high performance and easy-to-use API documentation
- 🔍 **Filtering Options:**
  - Ignore common words with custom ignore lists
  - Focus on most relevant words with percentile-based filtering
- 📈 **Performance Metrics:** Includes time elapsed for each request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

Maintainer - [Peter Mizsak](https://github.com/mizsakpeti)
