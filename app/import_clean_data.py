import argparse
from pathlib import Path
from app.db.repository import clear_database 
from app.clean_storage import load_clean_recipes

from app.db.connection import get_connection
from app.db.importer import import_recipes

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run import pipeline"
    )

    parser.add_argument("--input", type=str, default="data/clean_data.json", help="Path to clean_data.json")
    parser.add_argument(
        "--clear",
        action="store_true",
        help="Clear cocktails and ingredients tables before import",
    )    
    return parser.parse_args()
    
def main() -> None:
    args = parse_args()
    input_path = Path(args.input)

    clean_recipes = load_clean_recipes(str(input_path))

    conn = get_connection()

    try:
        if args.clear:
            clear_database(conn)
            print("Database cleared")

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