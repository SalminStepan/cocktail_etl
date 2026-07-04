def upsert_cocktail(conn, clean_recipe: dict) -> int:
    params = {
        "source": "diffordsguide",
        "source_url": clean_recipe["source_url"],
        "name": clean_recipe["name"],
        "description": clean_recipe.get("description"),
        "image_url": clean_recipe.get("image_url"),
        "glass": clean_recipe.get("glass"),
        "garnish": clean_recipe.get("garnish"),
        "method": clean_recipe.get("method"),
        "parse_status": clean_recipe["parse_status"],
    }

    with conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO cocktails (
                source,
                source_url,
                name,
                description,
                image_url,
                glass,
                garnish,
                method,
                parse_status
            )
            VALUES (
                %(source)s,
                %(source_url)s,
                %(name)s,
                %(description)s,
                %(image_url)s,
                %(glass)s,
                %(garnish)s,
                %(method)s,
                %(parse_status)s
            )
            ON CONFLICT (source_url)
            DO UPDATE SET
                source = EXCLUDED.source,
                name = EXCLUDED.name,
                description = EXCLUDED.description,
                image_url = EXCLUDED.image_url,
                glass = EXCLUDED.glass,
                garnish = EXCLUDED.garnish,
                method = EXCLUDED.method,
                parse_status = EXCLUDED.parse_status,
                updated_at = NOW()
            RETURNING id;
            """,
            params,
        )

        row = cur.fetchone()
        return row["id"]

def replace_ingredients(conn, cocktail_id: int, ingredients: list[dict] | None) -> None:
    with conn.cursor() as cur:
        cur.execute("DELETE FROM ingredients WHERE cocktail_id = %(cocktail_id)s", {"cocktail_id": cocktail_id})
        if not ingredients:
            return

        for position, ingredient in enumerate(ingredients, start=1):
            params = {
                "cocktail_id": cocktail_id,
                "position": position,
                "raw": ingredient["raw"],
                "amount": ingredient.get("amount"),
                "unit": ingredient.get("unit"),
                "name": ingredient.get("name"),
                "comment": ingredient.get("comment"),
                "unresolved": ingredient["unresolved"],
            }
            cur.execute(
                """
                INSERT INTO ingredients (
                    cocktail_id,
                    position,
                    raw,
                    amount,
                    unit,
                    name,
                    comment,
                    unresolved
                )
                VALUES (
                    %(cocktail_id)s,
                    %(position)s,
                    %(raw)s,
                    %(amount)s,
                    %(unit)s,
                    %(name)s,
                    %(comment)s,
                    %(unresolved)s
                )
                """,
                params
            )

def clear_database(conn) -> None:
    with conn.cursor() as cur:
        cur.execute(
            """
            TRUNCATE TABLE ingredients, cocktails CASCADE;
            """
        )