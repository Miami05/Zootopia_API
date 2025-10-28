import requests

API_KEY = "m76+OfPfOQNYc6KOtBb9qA==HpZ45W5exHYGnCPK"
URL = "https://api.api-ninjas.com/v1/animals"

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