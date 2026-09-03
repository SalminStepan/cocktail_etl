# Cocktail ETL

ETL pipeline for extracting, normalizing, validating, and importing cocktail recipe data into PostgreSQL.

The project discovers cocktail recipe pages through a sitemap, extracts structured JSON-LD `Recipe` data, stores raw snapshots, normalizes recipes into a clean internal representation, and imports the result into a relational PostgreSQL database.

It is the data ingestion layer of the larger Cocktail project:

```text
Cocktail ETL
    ↓
PostgreSQL
    ↑
Cocktail API
    ↑
Telegram Bot
```

Current dataset quality report:

[docs/data_quality.md](docs/data_quality.md)

---

## Status

The ETL pipeline is stable and has successfully produced the current production dataset used by the Cocktail API and Telegram bot.

Current automated test suite:

```text
19 passed
```

Implemented pipeline:

```text
sitemap
    ↓
recipe URLs
    ↓
HTTP fetch
    ↓
JSON-LD extraction
    ↓
raw_data.json
    ↓
normalization
    ↓
clean_data.json
    ↓
PostgreSQL
```

The pipeline is intentionally split into separate extraction, normalization, and import stages so parser changes can be tested without repeatedly downloading the full source dataset.

---

## Current Dataset

Latest full import:

```text
Cocktails:              6614
Ingredients:            30761

parse_status ok:        5619
parse_status partial:   995
parse_status failed:    0
```

Ingredient parsing quality:

```text
Unresolved ingredients: 11 / 30761
Parsed successfully:    ~99.96%
```

Image URL quality:

```text
Real image URLs:        6360
No image:               254
Bad image URLs:         0
```

Most `partial` recipes are caused by missing `glass` and/or `method` fields in the source JSON-LD data rather than failed ingredient parsing.

Difford's placeholder image is normalized to `NULL` and is not counted as a real cocktail image.

See [docs/data_quality.md](docs/data_quality.md) for detailed quality metrics.

---

## Features

* Reads cocktail recipe URLs from sitemap XML
* Fetches recipe pages over HTTP
* Applies a request delay during scraping
* Extracts structured JSON-LD `Recipe` objects
* Stores raw extracted data in JSON
* Supports offline re-normalization from existing raw data
* Normalizes cocktail metadata
* Normalizes ingredient amounts and units
* Preserves unresolved ingredient text
* Extracts method, glass, garnish, description, and image URLs
* Detects and removes placeholder image URLs
* Tracks recipe quality through `parse_status`
* Stores parse diagnostics
* Imports normalized data into PostgreSQL
* Uses idempotent cocktail upsert by `source_url`
* Replaces ingredient collections during re-import
* Supports complete database rebuild with `--clear`
* Provides CLI entrypoints for extraction, normalization, and import
* Includes automated normalization tests
* Includes a reproducible data quality report

---

## Pipeline Architecture

The ETL pipeline consists of three main stages.

### 1. Extract

```text
sitemap.xml
    ↓
recipe URLs
    ↓
HTML pages
    ↓
JSON-LD Recipe
    ↓
raw_data.json
```

This stage preserves extracted source data with minimal transformation.

### 2. Normalize

```text
raw_data.json
    ↓
normalizer
    ↓
validated internal models
    ↓
clean_data.json
```

This stage handles:

* ingredient parsing
* amount normalization
* unit normalization
* cocktail metadata extraction
* missing-field handling
* placeholder image detection
* parse quality classification

### 3. Import

```text
clean_data.json
    ↓
importer
    ↓
repository
    ↓
PostgreSQL
```

The import stage is idempotent for cocktails by `source_url`.

Ingredient rows for an existing cocktail are replaced during re-import, preventing duplicate ingredient collections.

---

## Development Workflow

The normal development cycle does not require downloading the entire source dataset again.

After changing normalization logic:

```bash
pytest -q

python -m app.normalize_raw_data \
  --input data/raw_data.json \
  --output data/clean_data.json

python -m app.import_clean_data \
  --input data/clean_data.json \
  --clear
```

This makes normalization development deterministic and significantly faster than performing a full network scrape for every parser change.

---

## Project Structure

```text
cocktail_etl/
├── app/
│   ├── db/
│   │   ├── connection.py
│   │   ├── importer.py
│   │   ├── repository.py
│   │   └── schema.sql
│   │
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
│
├── data/
│   ├── raw_data.json
│   └── clean_data.json
│
├── docs/
│   └── data_quality.md
│
├── tests/
├── pyproject.toml
└── README.md
```

Large raw and normalized dataset snapshots are local/generated artifacts and are not intended to be part of the main Git repository history.

---

## Tech Stack

* Python 3.12+
* PostgreSQL
* psycopg 3
* HTTPX
* Beautiful Soup
* Pydantic
* pytest

---

## Installation

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install the project with development dependencies:

```bash
python -m pip install -e ".[dev]"
```

---

## Database Setup

Create the PostgreSQL database:

```bash
sudo -u postgres createdb cocktail_etl
```

Apply the schema:

```bash
sudo -u postgres psql \
  -d cocktail_etl \
  -f app/db/schema.sql
```

Configure the database connection:

```bash
export DATABASE_URL="postgresql://cocktail_user:cocktail_password@localhost:5432/cocktail_etl"
```

Real database credentials must not be committed to Git.

Use environment variables or local environment configuration instead.

---

## Usage

### Run a limited ETL pipeline

For development:

```bash
python -m app.main --limit 10
```

Available CLI options:

```bash
python -m app.main --help
```

---

### Run a full scrape

```bash
python -m app.main \
  --raw-output data/raw_data.json \
  --clean-output data/clean_data.json
```

A full scrape performs network requests to the source website and should not be required for ordinary normalization development.

---

### Offline Normalization

Rebuild normalized data from an existing raw dataset:

```bash
python -m app.normalize_raw_data \
  --input data/raw_data.json \
  --output data/clean_data.json
```

This is the preferred workflow after modifying parsing or normalization logic.

---

### Import Clean Data

Import normalized recipes into PostgreSQL:

```bash
python -m app.import_clean_data \
  --input data/clean_data.json
```

Using the default path:

```bash
python -m app.import_clean_data
```

---

### Rebuild the Database

Clear the current cocktail and ingredient data and rebuild the database from normalized JSON:

```bash
python -m app.import_clean_data \
  --input data/clean_data.json \
  --clear
```

This mode is useful for development and data quality verification.

It should be used deliberately because it replaces the current imported dataset.

---

## Database Model

### `cocktails`

Stores normalized recipe-level information.

Important fields:

```text
source
source_url
name
description
image_url
glass
garnish
method
parse_status
created_at
updated_at
```

`source_url` is unique and acts as the stable source identifier used for idempotent imports.

---

### `ingredients`

Stores ordered ingredients associated with cocktails.

Important fields:

```text
cocktail_id
position
raw
amount
unit
name
comment
unresolved
```

The original ingredient text is always retained in `raw`.

If an ingredient cannot be reliably normalized, it is preserved and marked:

```text
unresolved = true
```

This prevents parser uncertainty from causing source data loss.

---

## Data Quality Strategy

The ETL pipeline prefers preserving incomplete information over silently producing incorrect normalized data.

Recipes are assigned a parsing status.

### `ok`

The recipe was normalized without known structural problems.

### `partial`

The recipe is usable but one or more optional or expected source fields could not be extracted.

Typical examples:

```text
glass missing
method missing
```

### `failed`

The recipe could not be normalized into a usable representation.

Current dataset:

```text
failed: 0
```

Unresolved ingredients are tracked separately from cocktail-level `parse_status`.

This allows the dataset to remain usable while making normalization uncertainty measurable.

---

## Quality Checks

Useful SQL checks after import:

```sql
SELECT COUNT(*)
FROM cocktails;
```

```sql
SELECT COUNT(*)
FROM ingredients;
```

Parse status distribution:

```sql
SELECT
    parse_status,
    COUNT(*)
FROM cocktails
GROUP BY parse_status
ORDER BY parse_status;
```

Missing cocktail metadata:

```sql
SELECT
    COUNT(*) FILTER (
        WHERE glass IS NULL
    ) AS glass_null,

    COUNT(*) FILTER (
        WHERE method IS NULL
    ) AS method_null,

    COUNT(*) FILTER (
        WHERE glass IS NULL
          AND method IS NULL
    ) AS both_null,

    COUNT(*) FILTER (
        WHERE image_url IS NOT NULL
    ) AS real_image_urls,

    COUNT(*) FILTER (
        WHERE image_url IS NULL
    ) AS no_image

FROM cocktails;
```

Invalid image URLs:

```sql
SELECT COUNT(*) AS bad_image_urls
FROM cocktails
WHERE image_url IS NOT NULL
  AND image_url !~* '^https?://[^/]+';
```

Unresolved ingredients:

```sql
SELECT COUNT(*)
FROM ingredients
WHERE unresolved = true;
```

Unit distribution:

```sql
SELECT
    unit,
    COUNT(*)
FROM ingredients
GROUP BY unit
ORDER BY COUNT(*) DESC;
```

Expected production metrics are documented in:

[docs/data_quality.md](docs/data_quality.md)

---

## Testing

Run the test suite:

```bash
pytest -q
```

Current result:

```text
19 passed
```

The tests primarily cover normalization behavior, including:

* ingredient parsing
* amount extraction
* unit normalization
* method extraction
* glass extraction
* garnish extraction
* image handling
* full recipe normalization

Repository and database integration tests against a dedicated PostgreSQL test database are planned as a separate stage.

---

## Current Status

Completed:

```text
Sitemap discovery                       ✅
HTTP page fetching                      ✅
JSON-LD Recipe extraction               ✅
Raw JSON storage                        ✅
Offline normalization                   ✅
Clean JSON storage                      ✅
Ingredient parsing                      ✅
Unit normalization                      ✅
Recipe metadata normalization           ✅
Image URL extraction                    ✅
Placeholder image handling              ✅
Parse quality tracking                  ✅
PostgreSQL schema                       ✅
Database connection                     ✅
Idempotent cocktail import              ✅
Ingredient replacement on re-import     ✅
Full database rebuild mode              ✅
Normalization test suite                ✅
Data quality reporting                  ✅
Full 6,614-cocktail dataset             ✅
FastAPI read layer                      ✅ separate project
Telegram read client                    ✅ separate project
```

The ETL layer itself is now considered stable.

New feature development should primarily happen in downstream services unless changes to data extraction or normalization are required.

---

## Roadmap

Next ETL-specific engineering stages:

```text
1. Repository/import integration tests      ⏳ planned
2. Dedicated PostgreSQL test database       ⏳ planned
3. GitHub Actions CI                        ⏳ planned
4. Schema migration strategy                ⏳ planned
5. Keep data quality metrics synchronized   ⏳ ongoing
6. Dataset refresh workflow                 ⏳ planned
```

Project-wide downstream development:

```text
Cocktail API
    ↓
pgvector semantic search
    ↓
retrieval
    ↓
RAG /ask
    ↓
Telegram integration
    ↓
Telegram Mini App
```

The ETL project may later provide data preparation or embedding backfill utilities if the semantic-search architecture requires them, but vector search and RAG request handling belong to the backend API layer rather than the scraping pipeline.

---

## Related Projects

### Cocktail API

Read-only FastAPI backend over the PostgreSQL dataset.

Responsibilities include:

* cocktail listing
* cocktail search
* cocktail lookup
* ingredient search
* dataset statistics
* health checks
* response validation
* backend error handling
* Dockerized API runtime

Repository:

```text
https://github.com/SalminStepan/cocktail_api
```

### Cocktail Recipe Telegram Bot

Telegram interface consuming the Cocktail API over HTTP.

Responsibilities include:

* recipe browsing
* search
* pagination
* cocktail cards
* API response validation
* Telegram interaction
* usage analytics

Repository:

```text
https://github.com/SalminStepan/cocktail_manager_bot_tg
```

---

## Attribution

This is a non-commercial educational portfolio project.

Recipe data is collected for educational and technical demonstration purposes.

The downstream applications preserve source attribution and links to the original recipe pages.

The project is not affiliated with or endorsed by Difford's Guide.

---

## Author

Stepan Salmin

Junior Python Backend Developer

Focus:

```text
Python
PostgreSQL
SQL
ETL
FastAPI
backend architecture
data quality
testing
Docker
AI / RAG systems
```
