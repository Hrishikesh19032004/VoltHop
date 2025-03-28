import requests

api_key = "XWC1IVFlFXemhVaymTWmBd8dtY3yhpcWjkQcrfyL"
url = f"https://developer.nrel.gov/api/alt-fuel-stations/v1.json?api_key={api_key}&limit=5"


response = requests.get(url)


if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")
