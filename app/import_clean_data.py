import argparse
import json
from pathlib import Path


from app.db.connection import get_connection
from app.db.importer import import_recipes

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run import pipeline"
    )

    parser.add_argument("--input", type=str, default="data/clean_data.json", help="Path to clean_data.json")
    return parser.parse_args()

def load_clean_recipes(path: Path) -> list[dict]:
    with open(path, "r", encoding="utf-8") as f:
        clean_recipes = json.load(f)
        if not isinstance(clean_recipes, list):
            raise ValueError("clean data file must contain a list")
        return clean_recipes
    
def main() -> None:
    args = parse_args()
    input_path = Path(args.input)

    clean_recipes = load_clean_recipes(input_path)

    conn = get_connection()

    try:
        imported_count = import_recipes(conn, clean_recipes)
        conn.commit()
        print(f"Imported recipes: {imported_count}")
    
    except Exception:
        conn.rollback()
        raise
    
    finally:
        conn.close()

if __name__ == "__main__":
    main()