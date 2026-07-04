import json


def save_clean_recipes(clean_recipes: list[dict], path: str = "data/clean_data.json") -> None:
    if not isinstance(clean_recipes, list):
        raise TypeError("clean_recipes must be a list")
    for clean_recipe in clean_recipes:
        if not isinstance(clean_recipe, dict):
            raise TypeError("each clean_recipe must be a dict")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(clean_recipes, f, ensure_ascii=False, indent=2)

def load_clean_recipes(path: str = "data/clean_data.json") -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        clean_recipes = json.load(f)

    if not isinstance(clean_recipes, list):
        raise ValueError("clean data file must contain a list")

    for clean_recipe in clean_recipes:
        if not isinstance(clean_recipe, dict):
            raise ValueError("each clean recipe must be a dict")

    return clean_recipes