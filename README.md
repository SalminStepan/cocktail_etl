# Cocktail ETL

ETL pipeline for extracting, normalizing, and importing cocktail recipe data from structured web sources into PostgreSQL.

The project collects cocktail recipe URLs from a sitemap, extracts structured JSON-LD recipe data, normalizes it into a clean internal format, and imports the result into a relational PostgreSQL database.

## Features

* Reads cocktail recipe URLs from sitemap XML
* Fetches recipe pages with request delay
* Extracts structured JSON-LD `Recipe` data
* Saves raw recipe data to JSON
* Normalizes ingredients, method, glass, garnish, image URL, and description
* Tracks parsing quality with `parse_status` and `parse_errors`
* Stores normalized cocktail data in PostgreSQL
* Uses idempotent cocktail upsert by `source_url`
* Replaces ingredient lists during re-import to avoid duplicates
* Provides CLI commands for ETL and database import
* Includes pytest coverage for normalization logic

## Pipeline

```text
sitemap.xml
    ↓
recipe URLs
    ↓
HTML pages
    ↓
JSON-LD Recipe blocks
    ↓
raw_data.json
    ↓
clean_data.json
    ↓
PostgreSQL
```

## Project structure

```text
cocktail_etl/
├── app/
│   ├── db/
│   │   ├── connection.py
│   │   ├── importer.py
│   │   ├── repository.py
│   │   └── schema.sql
│   ├── clean_storage.py
│   ├── import_clean_data.py
│   ├── logging_config.py
│   ├── main.py
│   ├── normalizer.py
│   ├── page_fetcher.py
│   ├── raw_storage.py
│   ├── recipe_extractor.py
│   ├── schemas.py
│   └── sitemap_reader.py
├── data/
│   ├── raw_data.json
│   └── clean_data.json
├── tests/
├── pyproject.toml
└── README.md
```

## Requirements

* Python 3.12+
* PostgreSQL
* `httpx`
* `beautifulsoup4`
* `psycopg`
* `pytest` for development/testing

## Installation

```bash
python -m venv .venv
source .venv/bin/activate

pip install -e ".[dev]"
```

## Database setup

Create PostgreSQL database:

```bash
sudo -u postgres createdb cocktail_etl
```

Apply schema:

```bash
sudo -u postgres psql -d cocktail_etl -f app/db/schema.sql
```

Create a database user for the application and set `DATABASE_URL`:

```bash
export DATABASE_URL="postgresql://cocktail_user:cocktail_password@localhost:5432/cocktail_etl"
```

Do not commit real database credentials. Use environment variables or a local `.env` file.

## Usage

Run the ETL pipeline and generate JSON files:

```bash
python -m app.main --limit 10
```

Custom input/output options are available:

```bash
python -m app.main --help
```

Import normalized data into PostgreSQL:

```bash
python -m app.import_clean_data --input data/clean_data.json
```

Default import path:

```bash
python -m app.import_clean_data
```

## Database model

### `cocktails`

Stores normalized cocktail-level data:

* source
* source_url
* name
* description
* image_url
* glass
* garnish
* method
* parse_status
* created_at
* updated_at

`source_url` is unique and is used for idempotent imports.

### `ingredients`

Stores ordered ingredients for each cocktail:

* cocktail_id
* position
* raw
* amount
* unit
* name
* comment
* unresolved

Ingredients are replaced on each import for a cocktail, so repeated imports do not create duplicate ingredient rows.

## Testing

Run tests:

```bash
pytest
```

The test suite currently covers:

* ingredient parsing
* method extraction
* glass extraction
* garnish extraction
* full recipe normalization

## Current status

Implemented:

* sitemap reading
* page fetching
* JSON-LD recipe extraction
* raw and clean JSON storage
* recipe normalization
* PostgreSQL schema
* database connection
* cocktail upsert
* ingredient replacement
* clean JSON import command
* normalization tests

Planned:

* import logging improvements
* repository tests
* search queries for bot integration
* bot database adapter
* optional FastAPI layer
