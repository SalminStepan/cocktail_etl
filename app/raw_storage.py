import json


def save_raw_recipes(raw_recipes: list[dict], path: str = "data/raw_data.json") -> None:
    if not isinstance(raw_recipes, list):
        raise TypeError("raw_recipes must be a list")
    for raw_recipe in raw_recipes:
        if not isinstance(raw_recipe, dict):
            raise TypeError("each raw_recipe must be a dict")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(raw_recipes, f, ensure_ascii=False, indent=2)

def load_raw_recipes(path: str = "data/raw_data.json") -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        raw_recipes = json.load(f)
        if not isinstance(raw_recipes, list):
            raise ValueError("raw data file must contain a list")
        for raw_recipe in raw_recipes:
            if not isinstance(raw_recipe, dict):
                raise ValueError("raw recipe must be a dict")
        
    return raw_recipes