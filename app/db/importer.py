from app.db.repository import upsert_cocktail, replace_ingredients

def import_recipe(conn, clean_recipe:dict) -> int:
    cocktail_id = upsert_cocktail(conn, clean_recipe)
    ingredients = clean_recipe.get("ingredients")

    replace_ingredients(conn, cocktail_id, ingredients)

    return cocktail_id
    
def import_recipes(conn, clean_recipes: list[dict]) -> int:
    importer_count = 0
    for clean_recipe in clean_recipes:
        import_recipe(conn, clean_recipe)
        importer_count += 1
    
    return importer_count