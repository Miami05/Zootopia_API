import requests
import os
from dotenv import load_dotenv

load_dotenv()
URL = "https://api.api-ninjas.com/v1/animals"
API_KEY = os.getenv("API_KEY", "").strip()

def fetch_data(name):
    """
    Fetches the animals data for the animal 'animal_name'.
    Returns: a list of animals, each animal is a dictionary:
    {
        'name': ...,
        'taxonomy': {
         ...
      },
        'locations': [
            ...
        ],
        'characteristics': {
            ...
        }
    },
    """
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