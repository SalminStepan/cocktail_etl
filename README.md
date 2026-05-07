
# Cocktail ETL

Cocktail ETL is a data pipeline for collecting and normalizing cocktail recipe data from structured web sources.

The project extracts recipe URLs from a sitemap, downloads recipe pages, reads structured JSON-LD Recipe data, stores raw source data, normalizes recipe fields, and prepares clean JSON output for future database import.

## Business Problem

Bars, restaurants, and beverage teams often store cocktail recipes in scattered formats: notes, spreadsheets, books, websites, or internal chat messages.

This makes it difficult to:

- build a searchable cocktail database
- standardize recipes across teams
- import recipes into internal tools
- analyze ingredients, methods, glassware, and garnishes
- keep recipe data structured and reusable

This project solves the data preparation layer: it turns external structured recipe pages into normalized data that can be used by a recipe database, Telegram bot, admin panel, or bar management system.

## Current Status

Implemented:

- sitemap reader
- recipe page fetcher
- JSON-LD Recipe extractor
- raw JSON storage
- recipe normalizer
- clean JSON storage
- MVP pipeline for the first 10 recipe URLs

## MVP v1

The first working version of the project:

- accepts a sitemap URL
- extracts the first 10 recipe URLs
- downloads recipe page HTML
- extracts JSON-LD Recipe data
- saves raw data to `data/raw_data.json`
- normalizes raw recipe data
- saves normalized data to `data/clean_data.json`

## Architecture

```text
sitemap_reader -> page_fetcher -> recipe_extractor -> raw_storage -> normalizer -> clean_storage
```

## Data Flow

```
sitemap URL
-> recipe URLs
-> HTML pages
-> JSON-LD Recipe data
-> raw recipes
-> normalized recipes
-> JSON output files
```

## Modules

| Module | Responsibility |
| --- | --- |
| `sitemap_reader` | Loads the sitemap and returns recipe page URLs. |
| `page_fetcher` | Downloads recipe page HTML. |
| `recipe_extractor` | Extracts raw recipe data from JSON-LD. |
| `raw_storage` | Saves raw recipes to `data/raw_data.json`. |
| `normalizer` | Converts raw recipe data into a normalized structure. |
| `clean_storage` | Saves normalized recipes to `data/clean_data.json`. |
| `main` | Orchestrates the full MVP pipeline. |
| `logging_config` | Reserved for application logging configuration. |

## Output Files

| File | Description |
| --- | --- |
| `data/raw_data.json` | Raw recipe data extracted from JSON-LD. |
| `data/clean_data.json` | Normalized recipe data prepared for future database import. |

## Clean Recipe Structure

Each normalized recipe contains:

```
source_url
name
glass
garnish
method
ingredients
parse_status
parse_errors
```

Each normalized ingredient contains:

```
raw
amount
unit
name
comment
unresolved
```

## Parse Status

| Status | Meaning |
| --- | --- |
| `ok` | Recipe was normalized without detected issues. |
| `partial` | Recipe was partially normalized, but some fields or ingredients could not be parsed. |
| `failed` | Recipe is missing critical data such as name or ingredients. |

## How to Run

Install dependencies:

```
pip install-e .
```

Run the MVP pipeline:

```
python-m app.main
```

Expected output:

```
Processed URLs: 10
Raw recipes saved: 10
Clean recipes saved: 10
```

## Tech Stack

- Python
- httpx
- BeautifulSoup
- XML sitemap parsing
- JSON-LD parsing
- JSON file storage

## v1 Limitations

- does not crawl the website recursively
- processes only the first 10 recipe URLs
- does not download images
- does not write directly to PostgreSQL
- does not guarantee perfect ingredient parsing
- does not parse visual HTML; only JSON-LD Recipe data is used
- does not yet provide CLI arguments
- uses `print` for MVP output instead of full logging

## Planned Improvements

- add CLI arguments for sitemap URL, limit, delay, and output paths
- add structured logging
- improve ingredient parsing for fractions and non-standard units
- add tests for parser and normalizer
- add PostgreSQL import
- add resume support for already processed URLs