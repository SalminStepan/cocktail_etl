def parse_ingredient(ingredient_raw: str) -> dict:
    units = ["ml", "dash", "barspoon", "drop"]
    unresolved = {
        "raw": ingredient_raw,
        "amount": None,
        "unit": None,
        "name": None,
        "comment": None,
        "unresolved": True
    }

    parts = ingredient_raw.split()
    if len(parts) < 3:
        return unresolved
    
    try:
        amount =  float(parts[0])
    except ValueError:
        return unresolved
    
    if parts[1] not in units:
        return unresolved

    unit = parts[1]
    name = " ".join(parts[2:])

    parsed_ingredient = {
        "raw": ingredient_raw,
        "amount": amount,
        "unit": unit,
        "name": name,
        "comment": None,
        "unresolved": False
    }
    return parsed_ingredient

def parse_ingredients(ingredients_raw: list[str]) -> list[dict]:
    clean_parsed_ingredients = [parse_ingredient(ingredient_raw) for ingredient_raw in ingredients_raw]
    return clean_parsed_ingredients

def extract_method(instructions_raw: list[dict]) -> str | None:
    methods = ["STIR", "SHAKE", "BUILD", "BLEND", "DRY SHAKE", "DRY BLEND", "THROW", "MUDDLE"]
    for step in instructions_raw:
        method = step.get("name", "").strip().upper()
        if method in methods:
            return method
    
    return None

def extract_glass(instructions_raw: list[dict]) -> str | None:
    for step in instructions_raw:
        step_name = step.get("name", "")
        if step_name != "Prepare glass":
            continue
        text = step.get("text", "").split()
        glass = []        
        for word in text:
            if word == word.upper():
                glass.append(word.strip(".,"))
        if glass:
            return ' '.join(glass)
    return None

def extract_garnish(instructions_raw: list[dict]) -> str | None:
    for step in instructions_raw:
        step_name = step.get("name", "")
        if step_name != "Prepare garnish":
            continue
        text = step.get("text", "").split()
        garnish_words = []
        for word in text[3:]:
            garnish_words.append(word.strip(".,"))
        garnish = ' '.join(garnish_words)
        if garnish:
            return garnish
    return None

def normalize_recipe(raw_recipe: dict) -> dict:
    parse_errors = []
    source_url = raw_recipe.get("source_url")
    name = raw_recipe.get("name")
    
    if not name:
        parse_errors.append("name missing")
    
    ingredients_raw = raw_recipe.get("ingredients_raw", [])
    if not ingredients_raw:
        parse_errors.append("ingredients_raw missing")
    
    instructions_raw = raw_recipe.get("instructions_raw", [])
    if not instructions_raw:
        parse_errors.append("instructions_raw missing")
    
    if "name missing" in parse_errors or "ingredients_raw missing" in parse_errors:
        clean_recipe = {
            "source_url": source_url,
            "name": name,
            "glass": None,
            "garnish": None,
            "method": None,
            "ingredients": None,
            "parse_status": "failed",
            "parse_errors": parse_errors
        }
        return clean_recipe
    
    clean_parsed_ingredients = parse_ingredients(ingredients_raw)

    for ingredient in clean_parsed_ingredients:
        if ingredient.get("unresolved"):
            parse_errors.append(f'Unresolved ingredient: {ingredient.get("raw")}')

    method = extract_method(instructions_raw)
    glass = extract_glass(instructions_raw)
    garnish = extract_garnish(instructions_raw)

    if method is None:
        parse_errors.append("method not found")

    if glass is None:
        parse_errors.append("glass not found")    
    
    if parse_errors:
        parse_status = "partial"
    else:
        parse_status = "ok"

    clean_recipe = {
        "source_url": source_url,
        "name": name,
        "glass": glass,
        "garnish": garnish,
        "method": method,
        "ingredients": clean_parsed_ingredients,
        "parse_status": parse_status,
        "parse_errors": parse_errors
    }

    return clean_recipe