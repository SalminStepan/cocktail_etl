import json



def save_raw_recipes(raw_recipes: list[dict], path: str = "data/raw_data.json") -> None:
    if not isinstance(raw_recipes, list):
        raise TypeError("raw_recipes must be a list")
    for raw_recipe in raw_recipes:
        if not isinstance(raw_recipe, dict):
            raise TypeError("each raw_recipe must be a dict")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(raw_recipes, f, ensure_ascii=False, indent=2)