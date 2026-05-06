import httpx

def fetch_page_html(recipe_url: str) -> str:
    response = httpx.get(recipe_url, timeout=5.0)
    response.raise_for_status()
    return response.text