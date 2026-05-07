import time

from app.sitemap_reader import get_recipe_urls
from app.page_fetcher import fetch_page_html
from app.recipe_extractor import extract_raw_recipe
from app.raw_storage import save_raw_recipes
from app.normalizer import normalize_recipe
from app.clean_storage import save_clean_recipes

SITEMAP_URL = "https://www.diffordsguide.com/sitemap/cocktail.xml"
LIMIT = 10
REQUEST_DELAY_SECONDS = 1


def run_pipeline() -> None:
    recipe_urls = get_recipe_urls(SITEMAP_URL, LIMIT)
    raw_recipes = []
    for url in recipe_urls:
        try:
            html = fetch_page_html(url)
            raw_recipe = extract_raw_recipe(html)
            raw_recipes.append(raw_recipe)
        except Exception as error:    
            print(f"Failed to process URL: {url}. Error: {error}")
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
            print(f"Failed to normalize recipe: {raw_recipe.get('name')}. Error: {error}")
            continue
    save_clean_recipes(clean_recipes)
    print(
        f"Processed URLs: {len(recipe_urls)}\n"
        f"Raw recipes saved: {len(raw_recipes)}\n"
        f"Clean recipes saved: {len(clean_recipes)}"
    )

if __name__ == "__main__":
    run_pipeline()