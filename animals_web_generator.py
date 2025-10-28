import requests
import json
from pathlib import Path
import html
import sys

API_KEY = "m76+OfPfOQNYc6KOtBb9qA==HpZ45W5exHYGnCPK"
URL = "https://api.api-ninjas.com/v1/animals"
OUTPUT_FILE = 'animals.html'

def fetch_animals(name: str):
    """Call the API Ninjas Animals endpoint and return a list of animals."""
    headers = {"X-Api-Key": API_KEY}
    try:
        resp = requests.get(URL, headers=headers, params={"name": name}, timeout=15)
    except requests.RequestException as e:
        print(f"Network error: {e}")
        return []

    if resp.ok:
        try:
            return resp.json() or []
        except ValueError:
            print("Error: API returned non-JSON response.")
            return []
    else:
        print(f"Error {resp.status_code}: {resp.text}")
        return []

def add_row(rows, label, value):
    """Append a formatted row to rows if value is truthy."""
    if value:
        rows.append(
            f"<div><strong>{html.escape(str(label))}:</strong> "
            f"{html.escape(str(value))}</div>"
        )

def render_items(animal):
    """Render a single animal card HTML block."""
    name = html.escape(animal.get("name", "Unknown"))
    taxonomy = animal.get("taxonomy", {}) or {}
    characteristics = animal.get("characteristics", {}) or {}
    locations = animal.get("locations", []) or []
    rows = []
    add_row(rows, "Kingdom", taxonomy.get("kingdom"))
    add_row(rows, "Phylum", taxonomy.get("phylum"))
    add_row(rows, "Class", taxonomy.get("class"))
    add_row(rows, "Order", taxonomy.get("order"))
    add_row(rows, "Family", taxonomy.get("family"))
    add_row(rows, "Genus", taxonomy.get("genus"))

    add_row(rows, "Type", characteristics.get("type"))
    add_row(rows, "Diet", characteristics.get("diet") or characteristics.get("prey"))
    add_row(rows, "Lifespan", characteristics.get("lifespan"))
    add_row(rows, "Weight", characteristics.get("weight"))
    add_row(rows, "Height", characteristics.get("height"))
    add_row(rows, "Habitat", characteristics.get("habitat"))
    if locations:
        add_row(rows, "Locations", ", ".join(locations))
    details = "\n".join(rows) if rows else "<div>No extra details available.</div>"
    return f"""
<li class="cards__item">
  <h3 class="card__title">{name}</h3>
  <div class="card__text">
    {details}
  </div>
</li>""".strip()

def build_page(query, animals, template_path):
    items_list = []
    for animal in (animals or []):
        items_list.append(render_items(animal))
    if not items_list:
      items_list.append(
          f'<li class="cards__item"><div class="card__text">'
          f'No results for "{html.escape(str(query))}".'
          f'</div></li>'
      )
    items = "\n".join(items_list)
    if template_path.exists():
        template = template_path.read_text(encoding="utf-8")
        return template.replace("__REPLACE_ANIMALS_INFO__", items)
    else:
        return f"""<!doctype html>
<html><head><meta charset="utf-8"><title>Animals — {html.escape(query)}</title></head>
<body><h1>Animals for “{html.escape(query)}”</h1><ul class="cards">{items}</ul></body></html>"""


def save_to_file(content, file_path):
    file_path.write_text(content, encoding="utf-8")

def main():
    animal_name = input("Enter a name of an animal: ").strip()
    if not animal_name:
        print("No animal name provided. Exiting.")
        sys.exit(1)
    animals = fetch_animals(animal_name)
    html_out = build_page(animal_name, animals, Path("animals_template.html"))
    save_to_file(html_out, Path(OUTPUT_FILE))
    print(f"Website was successfully generated to the file {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
