# Cocktail ETL

ETL pipeline for extracting, normalizing, and importing cocktail recipe data from structured web sources into PostgreSQL.

The project collects cocktail recipe URLs from a sitemap, extracts structured JSON-LD `Recipe` data, normalizes it into a clean internal format, and imports the result into a relational PostgreSQL database.

Current dataset quality report: [docs/data_quality.md](docs/data_quality.md)

## Features

* Reads cocktail recipe URLs from sitemap XML
* Fetches recipe pages with request delay
* Extracts structured JSON-LD `Recipe` data
* Saves raw recipe data to JSON
* Normalizes ingredients, method, glass, garnish, image URL, placeholder images, and description
* Tracks parsing quality with `parse_status` and `parse_errors`
* Stores normalized cocktail data in PostgreSQL
* Uses idempotent cocktail upsert by `source_url`
* Replaces ingredient lists during re-import to avoid duplicates
* Supports offline normalization from existing `raw_data.json`
* Supports full database rebuild from `clean_data.json` with `--clear`
* Provides CLI commands for ETL, offline normalization, and database import
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

The pipeline is split into separate stages:

```text
fetch/extract  -> raw_data.json
normalize      -> clean_data.json
import         -> PostgreSQL
```

This allows parser and normalization changes to be tested without re-downloading all recipe pages.

## Current data metrics

Latest full import:

```text
Cocktails:    6614
Ingredients:  30761
```

Parse status:

```text
ok:       5619
partial:   995
failed:      0
```

Ingredient parsing quality:

```text
Unresolved ingredients: 11 / 30761
Parsed successfully:    ~99.96%
```

Image URL quality:

```text
Real image URLs: 6360
No image:        254
Bad image URLs:  0
```

Difford's placeholder image is normalized to `NULL` and is not counted as a real cocktail image.

Most `partial` recipes are caused by missing `glass` and/or `method` fields in the source JSON-LD data, not by failed ingredient parsing.

See [docs/data_quality.md](docs/data_quality.md) for the full quality report.

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
│   ├── normalize_raw_data.py
│   ├── normalizer.py
│   ├── page_fetcher.py
│   ├── raw_storage.py
│   ├── recipe_extractor.py
│   ├── schemas.py
│   └── sitemap_reader.py
├── data/
│   ├── raw_data.json
│   └── clean_data.json
├── docs/
│   └── data_quality.md
├── tests/
├── pyproject.toml
└── README.md
```

Large generated JSON files are not intended to be committed to GitHub.

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

### Run full ETL pipeline

Run the full ETL pipeline and generate both JSON files:

```bash
python -m app.main --limit 10
```

Custom input/output options are available:

```bash
python -m app.main --help
```

Full scrape output:

```bash
python -m app.main \
  --raw-output data/raw_data.json \
  --clean-output data/clean_data.json
```

### Offline normalization

Rebuild `clean_data.json` from an existing `raw_data.json` without network requests:

```bash
python -m app.normalize_raw_data \
  --input data/raw_data.json \
  --output data/clean_data.json
```

This is the preferred development workflow after parser or normalization changes.

### Import clean data into PostgreSQL

Import normalized data into PostgreSQL:

```bash
python -m app.import_clean_data --input data/clean_data.json
```

Default import path:

```bash
python -m app.import_clean_data
```

### Rebuild database from clean data

For development quality checks, clear existing tables and rebuild the database from `clean_data.json`:

```bash
python -m app.import_clean_data \
  --input data/clean_data.json \
  --clear
```

The default development cycle is:

```bash
pytest
python -m app.normalize_raw_data --input data/raw_data.json --output data/clean_data.json
python -m app.import_clean_data --input data/clean_data.json --clear
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

Unresolved ingredients preserve the original `raw` text and are marked with:

```text
unresolved = true
```

This allows application layers to safely fall back to the original ingredient string.

## Quality checks

Useful SQL checks after import:

```sql
SELECT COUNT(*) FROM cocktails;

SELECT COUNT(*) FROM ingredients;

SELECT parse_status, COUNT(*)
FROM cocktails
GROUP BY parse_status
ORDER BY parse_status;

SELECT
    COUNT(*) FILTER (WHERE glass IS NULL) AS glass_null,
    COUNT(*) FILTER (WHERE method IS NULL) AS method_null,
    COUNT(*) FILTER (WHERE glass IS NULL AND method IS NULL) AS both_null,
    COUNT(*) FILTER (WHERE image_url IS NOT NULL) AS real_image_urls,
    COUNT(*) FILTER (WHERE image_url IS NULL) AS no_image
FROM cocktails;

SELECT COUNT(*) AS bad_image_urls
FROM cocktails
WHERE image_url IS NOT NULL
  AND image_url !~* '^https?://[^/]+';

SELECT COUNT(*)
FROM ingredients
WHERE unresolved = true;

SELECT unit, COUNT(*)
FROM ingredients
GROUP BY unit
ORDER BY COUNT(*) DESC;
```

Current expected results are documented in [docs/data_quality.md](docs/data_quality.md).

## Testing

Run tests:

```bash
pytest
```

The test suite currently covers:

* ingredient parsing
* unit normalization
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
* offline raw-to-clean normalization command
* recipe normalization
* ingredient unit normalization
* image URL extraction
* placeholder image normalization to `NULL`
* parse status tracking
* PostgreSQL schema
* database connection
* cocktail upsert by `source_url`
* ingredient replacement on re-import
* clean JSON import command
* full database rebuild mode with `--clear`
* normalization tests
* data quality report

Current stable workflow:

```bash
pytest
python -m app.normalize_raw_data --input data/raw_data.json --output data/clean_data.json
python -m app.import_clean_data --input data/clean_data.json --clear
```

Next planned stages:

* keep ETL data quality report in sync with production metrics
* add repository/import tests
* add Docker setup
* add CI workflow
* expose data through a FastAPI read API
* add semantic search with `pgvector`
* add RAG endpoint for cocktail recommendations