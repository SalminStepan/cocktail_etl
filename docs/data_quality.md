# Data Quality Report

## Source

Cocktail recipe data was extracted from the Difford’s Guide cocktail sitemap:

```text
https://www.diffordsguide.com/sitemap/cocktail.xml
```

## Pipeline

Current ETL pipeline:

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

## Current database metrics

Latest full import results:

```text
Cocktails:    6614
Ingredients:  30761
```

## Parse status

```text
ok:       5619
partial:   995
failed:      0
```

There are no failed recipes in the current dataset.

`partial` recipes are still imported and can be used by the application. A recipe is marked as `partial` when some non-critical structured fields are missing, mostly `glass` or `method`.

## Ingredient parsing quality

Current unresolved ingredient count:

```text
Unresolved ingredients: 11 / 30761
```

Successful ingredient parse coverage:

```text
30750 / 30761
≈ 99.96%
```

Unresolved ingredients keep the original raw text and are marked with:

```text
unresolved = true
```

This makes them safe for application rendering. The Telegram bot or API can fall back to displaying the original `raw` ingredient string.

## Ingredient units

Detected normalized units include:

```text
ml
dash
drop
count
top_up
barspoon
slice
pinch
whole
grind
inch
wedge
swath
sprig
scoop
cube
pint
float
twist
ring
cupful
gram
segment
pea
disc
knob
unit
litre
splash
bottle
bag
```

`NULL` units are expected only for unresolved ingredient rows.

## Missing cocktail fields

Current missing field report:

```text
glass_null:      983
method_null:     992
both_null:       983
image_url_null:    0
```

Image URL coverage:

```text
image_url present: 6614 / 6614
image_url missing: 0 / 6614
```

## Main conclusion

The ETL pipeline is stable enough for application integration.

The main data quality limitation is not ingredient parsing. Ingredient parsing coverage is approximately 99.96%.

Most `partial` recipes are caused by missing `glass` and/or `method` fields in the source JSON-LD data, not by parser failure.

## Known limitations

Remaining unresolved ingredients are edge cases from source data, for example unusual ingredient phrasing, garnish-like ingredients, or mixed instruction/ingredient strings.

Examples include:

```text
1 candied Hibiscus flower in syrup
1&frasl;2 fill glass with Pilsner lager
2&frasl;3 fill glass with Stout beer
fresh Lemon peel
fresh Orange peel
```

These cases are safe to keep as unresolved because the original raw ingredient text is preserved.

## Current status

The current ETL output is ready for the next stage:

```text
PostgreSQL database
    ↓
Telegram bot read-only integration
    ↓
FastAPI API layer
```

Before moving to Telegram bot integration, the recommended final checks are:

```bash
pytest
python -m app.normalize_raw_data --input data/raw_data.json --output data/clean_data.json
python -m app.import_clean_data --input data/clean_data.json --clear
```

Then verify database metrics with SQL quality checks.
