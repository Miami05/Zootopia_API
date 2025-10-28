
# Zootopia API — Animals Website Generator

A tiny Python project that fetches animal data and generates a static HTML page.  
Users enter an animal name (e.g., **Fox**, **Monkey**), data is fetched from the API Ninjas Animals API, and the results are rendered into `animals.html`.

---

## Features

- **Data–UI separation:**  
  - **Data Fetcher** (`data_fetcher.py`) – fetches data (API or any other source).  
  - **Website Generator** (`animals_web_generator.py`) – renders HTML from a list of animal dictionaries.
- **Template-driven UI:** Fills the placeholder `__REPLACE_ANIMALS_INFO__` in `animals_template.html`.
- **Graceful empty state:** Shows a friendly message when no animals are found (e.g., user input is gibberish).
- **.env-based config:** Keeps API keys out of source control.

---


- The **website generator** is **agnostic** to where data comes from; it only depends on the **shape**:
  ```python
  {
    "name": "...",
    "taxonomy": {...},
    "locations": [...],
    "characteristics": {...}
  }


## Getting Started

### Prerequisites

-   Python 3.8+
    
-   An API key from API Ninjas – Animals

### Install dependencies

`pip3 install -r requirements.txt`

### Configure environment

Create a `.env` file in the project root (kept out of git) with:

`API_NINJAS_KEY=your-real-api-key`


## Install & Run

```bash
# 1) Get the repo
git clone https://github.com/Miami05/Zootopia_API.git
cd Zootopia_API

# 2) Install deps
pip3 install -r requirements.txt

# 3) Set API key (one of these)
echo 'API_NINJAS_KEY=your-api-key' > .env
# or: export API_NINJAS_KEY="your-api-key"

# 4) Run the generator
python3 animals_web_generator.py
# Enter an animal name (e.g., Fox)

# 5) Open the output
# -> animals.html