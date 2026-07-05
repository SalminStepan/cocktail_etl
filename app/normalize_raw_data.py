import argparse
import logging

from app.raw_storage import load_raw_recipes
from app.clean_storage import save_clean_recipes
from app.normalizer import normalize_recipe
from app.logging_config import setup_logging


logger = logging.getLogger(__name__)

#1. разобрать CLI-аргументы
def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Normalize raw recipe data into clean recipe data"
    )

    parser.add_argument(
        "--input",
        type=str,
        default="data/raw_data.json",
        help="Path to raw_data.json",
    )

    parser.add_argument(
        "--output",
        type=str,
        default="data/clean_data.json",
        help="Path to clean_data.json",
    )

    return parser.parse_args()

def normalize_pipeline(
        raw_input_path: str,
        clean_output_path: str
) -> None:
    #2. включить logging
    setup_logging()
    logger.info("normalize pipeline started")

    raw_recipes = load_raw_recipes(raw_input_path)
#3. загрузить raw recipes через load_raw_recipes()
    clean_recipes = []
#4. прогнать каждый raw_recipe через normalize_recipe()
    for raw_recipe in raw_recipes:
        try:
            clean_recipe = normalize_recipe(raw_recipe)
            clean_recipes.append(clean_recipe)
        except Exception as error:    
            logger.error("Failed to normalize recipe: %s. Error: %s", raw_recipe.get('name'), error)
            continue
#5. сохранить clean recipes через save_clean_recipes()
    save_clean_recipes(clean_recipes, clean_output_path)

#6. вывести короткий отчёт
    logger.info("Raw recipes input: %s", len(raw_recipes))
    logger.info("Clean recipes saved: %s", len(clean_recipes))

if __name__ == "__main__":
    args = parse_args()
    normalize_pipeline(
        raw_input_path=args.input,
        clean_output_path=args.output,
    )