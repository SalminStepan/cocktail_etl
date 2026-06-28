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
