import html
from fractions import Fraction


def parse_fraction_token(token: str) -> float | None:
    token = token.strip(".,").replace("⁄", "/")

    if "/" not in token:
        return None

    try:
        return float(Fraction(token))
    except (ValueError, ZeroDivisionError):
        return None


def parse_amount(parts: list[str]) -> tuple[float | None, int]:
    if not parts:
        return None, 0

    try:
        amount = float(parts[0])
    except ValueError:
        amount = None

    if amount is not None:
        if len(parts) > 1:
            fraction = parse_fraction_token(parts[1])
            if fraction is not None:
                return amount + fraction, 2

        return amount, 1

    fraction = parse_fraction_token(parts[0])
    if fraction is not None:
        return fraction, 1

    return None, 0


def make_unresolved_ingredient(ingredient_raw: str) -> dict:
    return {
        "raw": ingredient_raw,
        "amount": None,
        "unit": None,
        "name": None,
        "comment": None,
        "unresolved": True,
    }


def make_parsed_ingredient(
    ingredient_raw: str,
    amount: float | None,
    unit: str,
    name: str,
) -> dict:
    return {
        "raw": ingredient_raw,
        "amount": amount,
        "unit": unit,
        "name": name,
        "comment": None,
        "unresolved": False,
    }


def parse_ingredient(ingredient_raw: str) -> dict:
    units = {
        "ml",
        "dash",
        "barspoon",
        "drop",
        "whole",
        "cube",
        "slice",
        "pint",
        "scoop",
        "pinch",
        "grind",
        "twist",
        "wedge",
        "inch",
        "pea",
        "swath",
        "sprig",
        "knob",
        "gram",
        "litre",
        "bag",
        "bottle",
        "cupful",
        "disc",
        "ring",
        "segment",
        "unit",
    }

    count_markers = {"fresh", "dried"}
    leaf_markers = {"leaf", "leaves"}

    unresolved = make_unresolved_ingredient(ingredient_raw)

    text = html.unescape(ingredient_raw).strip()
    lower_text = text.lower()

    if lower_text.startswith("top up with "):
        name = text[len("top up with "):].strip()
        if name:
            return make_parsed_ingredient(
                ingredient_raw=ingredient_raw,
                amount=None,
                unit="top_up",
                name=name,
            )
        return unresolved

    if lower_text.startswith("float "):
        name = text[len("float "):].strip()
        if name:
            return make_parsed_ingredient(
                ingredient_raw=ingredient_raw,
                amount=None,
                unit="float",
                name=name,
            )
        return unresolved

    if lower_text.startswith("splash "):
        name = text[len("splash "):].strip()
        if name:
            return make_parsed_ingredient(
                ingredient_raw=ingredient_raw,
                amount=None,
                unit="splash",
                name=name,
            )
        return unresolved

    parts = text.split()

    if len(parts) < 2:
        return unresolved

    amount, consumed = parse_amount(parts)

    if amount is None:
        return unresolved

    if len(parts) <= consumed:
        return unresolved

    unit_candidate = parts[consumed].lower().strip(".,")

    if unit_candidate in units:
        name = " ".join(parts[consumed + 1:]).strip()

        if not name:
            return unresolved

        return make_parsed_ingredient(
            ingredient_raw=ingredient_raw,
            amount=amount,
            unit=unit_candidate,
            name=name,
        )

    if unit_candidate in count_markers:
        name = " ".join(parts[consumed:]).strip()

        if not name:
            return unresolved

        return make_parsed_ingredient(
            ingredient_raw=ingredient_raw,
            amount=amount,
            unit="count",
            name=name,
        )

    last_word = parts[-1].lower().strip(".,")

    if last_word in leaf_markers:
        name = " ".join(parts[consumed:]).strip()

        if not name:
            return unresolved

        return make_parsed_ingredient(
            ingredient_raw=ingredient_raw,
            amount=amount,
            unit="count",
            name=name,
        )

    return unresolved


def parse_ingredients(ingredients_raw: list[str]) -> list[dict]:
    clean_parsed_ingredients = [
        parse_ingredient(ingredient_raw)
        for ingredient_raw in ingredients_raw
    ]
    return clean_parsed_ingredients


def extract_method(instructions_raw: list[dict]) -> str | None:
    methods = [
        "STIR",
        "SHAKE",
        "BUILD",
        "BLEND",
        "DRY SHAKE",
        "DRY BLEND",
        "THROW",
        "MUDDLE",
        "LAYER",
        "POUR",
        "COAT",
        "SWIRL",
        "CHURN",
        "ROLL",
        "REGAL",
    ]

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

        text = step.get("text", "")
        text = html.unescape(text)
        words = text.split()

        glass = []

        for word in words:
            if word == word.upper():
                glass.append(word.strip(".,"))

        if glass:
            return " ".join(glass)

    return None


def extract_garnish(instructions_raw: list[dict]) -> str | None:
    for step in instructions_raw:
        step_name = step.get("name", "")
        if step_name != "Prepare garnish":
            continue

        text = step.get("text", "")
        text = html.unescape(text)
        words = text.split()

        garnish_words = []

        for word in words[3:]:
            garnish_words.append(word.strip(".,"))

        garnish = " ".join(garnish_words)

        if garnish:
            return garnish

    return None


def normalize_recipe(raw_recipe: dict) -> dict:
    parse_errors = []

    source_url = raw_recipe.get("source_url")
    name = raw_recipe.get("name")
    description = raw_recipe.get("description")
    image_url = raw_recipe.get("image_url")
    if image_url == "/assets/images/themes/default_v5/cocktails/pixelated.jpg":
        image_url = None

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
            "description": description,
            "image_url": image_url,
            "glass": None,
            "garnish": None,
            "method": None,
            "ingredients": None,
            "parse_status": "failed",
            "parse_errors": parse_errors,
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
        "description": description,
        "image_url": image_url,
        "glass": glass,
        "garnish": garnish,
        "method": method,
        "ingredients": clean_parsed_ingredients,
        "parse_status": parse_status,
        "parse_errors": parse_errors,
    }

    return clean_recipe