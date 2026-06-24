import time
import logging

from app.sitemap_reader import get_recipe_urls
from app.page_fetcher import fetch_page_html
from app.recipe_extractor import extract_raw_recipe
from app.raw_storage import save_raw_recipes
from app.normalizer import normalize_recipe
from app.clean_storage import save_clean_recipes
from app.logging_config import setup_logging

logger = logging.getLogger(__name__)


SITEMAP_URL = "https://www.diffordsguide.com/sitemap/cocktail.xml"
LIMIT = 10
REQUEST_DELAY_SECONDS = 1


def run_pipeline() -> None:

    setup_logging()
    logger.info("Pipelane started")

    recipe_urls = get_recipe_urls(SITEMAP_URL, LIMIT)
    logger.info("Recipe URLs found: %s", len(recipe_urls))
    raw_recipes = []
    for url in recipe_urls:
        try:
            html = fetch_page_html(url)
            logger.info("Processing URL: %s", url)
            raw_recipe = extract_raw_recipe(html)
            raw_recipes.append(raw_recipe)
        except Exception as error:
            logger.error("Failed to process URL: %s. Error: %s", url, error)
            continue
        finally:
            time.sleep(REQUEST_DELAY_SECONDS)

    save_raw_recipes(raw_recipes)

    clean_recipes = []
    for raw_recipe in raw_recipes:
        try:
            clean_recipe = normalize_recipe(raw_recipe)
            clean_recipes.append(clean_recipe)
        except Exception as error:    
            logger.error("Failed to normalize recipe: %s. Error: %s", raw_recipe.get('name'), error)
            continue
    save_clean_recipes(clean_recipes)
    logger.info("Processed URLs: %s", len(recipe_urls))
    logger.info("Raw recipes saved: %s", len(raw_recipes))
    logger.info("Clean recipes saved: %s", len(clean_recipes))

if __name__ == "__main__":
    run_pipeline()