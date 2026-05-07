import httpx
import xml.etree.ElementTree as ET
# вытащить urls
def fetch_sitemap_xml(sitemap_url: str) -> str:
    response = httpx.get(sitemap_url, timeout=5.0)
    response.raise_for_status()
    return response.text
# отфильтровать <loc>
def extract_locs(xml_text: str) -> list[str]:
    root = ET.fromstring(xml_text)
    urls = [
        node.text.strip() 
        for node in root.iter() 
        if node.tag.endswith('loc') and node.text.strip()
    ]
    return urls
# отфильтровать /cocktails/recipe/
def filter_recipe_urls(urls: list[str]) -> list[str]:
    return [url for url in urls if "/cocktails/recipe/" in url]
# получить recipe_url, первые limit штук
def get_recipe_urls(sitemap_url: str, limit: int = 10) -> list[str]:
    xml_text = fetch_sitemap_xml(sitemap_url)
    all_urls = extract_locs(xml_text)
    urls = filter_recipe_urls(all_urls)
    return urls[:limit]