from bs4 import BeautifulSoup
import json

def extract_json_ld_blocks(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    json_ld_blocks = soup.find_all("script", type="application/ld+json")
    return [json_ld_block.text.strip() for json_ld_block in json_ld_blocks]

def parse_json_ld_block(json_text: str) -> dict:
    json_block = json.loads(json_text)
    return json_block

def find_recipe_data(json_ld_blocks: list[str]) -> dict:
    for json_ld_block in json_ld_blocks:
        parsed_data = parse_json_ld_block(json_ld_block)
        if parsed_data.get("@type") == "Recipe":
            return parsed_data
    raise ValueError("Recipe JSON-LD block not found")
    
def build_raw_recipe(recipe_data: dict) -> dict:
    image = recipe_data.get("image")
    image_url = None
    if isinstance(image, dict):
        image_url = image.get("url")
    raw_recipe = {
        "source": "diffordsguide",
        "source_url": recipe_data["url"],
        "name": recipe_data["name"],
        "description": recipe_data.get("description"),
        "image_url": image_url,
        "ingredients_raw": recipe_data["recipeIngredient"],
        "instructions_raw": recipe_data["recipeInstructions"],
        "keywords": recipe_data.get("keywords", []),
        "rating": recipe_data.get("aggregateRating"),
        "published_at": recipe_data.get("datePublished")
    }
    return raw_recipe

def extract_raw_recipe(html: str) -> dict:
    json_ld_blocks = extract_json_ld_blocks(html)
    recipe_data = find_recipe_data(json_ld_blocks)
    raw_recipe = build_raw_recipe(recipe_data)
    return raw_recipe