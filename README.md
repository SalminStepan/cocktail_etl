# Cocktail ETL

Educational ETL project for extracting cocktail recipes from the Difford's Guide sitemap.

## MVP v1

The first version of the project should:

- accept a sitemap URL
- extract the first 10 recipe URLs
- download recipe page HTML
- extract JSON-LD Recipe data
- save raw data to `raw_data.json`
- normalize raw recipe data
- save normalized data to `clean_data.json`

## Architecture

```

sitemap_reader 
page_fetcher
recipe_extractor
raw_storage
normalizer
clean_storage

```

## Modules

```

Module	Responsibility
sitemap_reader	    Loads the sitemap and returns recipe page URLs.
page_fetcher	    Downloads recipe page HTML.
recipe_extractor	Extracts raw recipe data from JSON-LD.
raw_storage	        Saves raw recipes to raw_data.json.
normalizer	        Converts raw recipe data into a normalized structure.
clean_storage	    Saves normalized recipes to clean_data.json.
logging_config	    Configures application logging.

```

## v1 Limitations
- does not crawl the website recursively
- does not download images
- does not write directly to PostgreSQL
- does not guarantee perfect ingredient parsing
- does not parse visual HTML; only JSON-LD Recipe data is used
