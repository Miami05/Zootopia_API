import requests
import json
from pathlib import Path
import html
import sys
import data_fetcher

OUTPUT_FILE = 'animals.html'

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


def render_empty(query: str) -> str:
    """Render the 'doesn't exist' message as a card."""
    q = html.escape(query)
    return f"""
<li class="cards__item error">
  <h2>The animal "{q}" doesn't exist.</h2>
  <p class="card__text">Try another name (e.g., Fox, Monkey).</p>
</li>""".strip()


def build_page(query, animals, template_path):
    """Fill the HTML template with cards for all returned animals, or a nice message."""
    items = (
        "\n".join(render_items(a) for a in animals)
        if animals else render_empty(query)
    )
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
    animals = data_fetcher.fetch_data(animal_name)
    html_out = build_page(animal_name, animals, Path("animals_template.html"))
    save_to_file(html_out, Path(OUTPUT_FILE))
    print(f"Website was successfully generated to the file {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
