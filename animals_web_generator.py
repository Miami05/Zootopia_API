import requests
import json

API_KEY = 'm76+OfPfOQNYc6KOtBb9qA==HpZ45W5exHYGnCPK'
URL = 'https://api.api-ninjas.com/v1/animals?name=fox'

def main():
    headers = {
        'X-Api-Key': API_KEY
    }
    response = requests.get(URL, headers=headers)
    if response.status_code == 200:
        data = response.json()
        print(json.dumps(data, indent=4))
    else:
        print("Error: ", response.status_code, response.text)

if __name__ == '__main__':
    main()
