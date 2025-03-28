import requests

# Replace 'YOUR_API_KEY' with the actual API key from NREL
api_key = "XWC1IVFlFXemhVaymTWmBd8dtY3yhpcWjkQcrfyL"
url = f"https://developer.nrel.gov/api/alt-fuel-stations/v1.json?api_key={api_key}&limit=5"

# Fetch data
response = requests.get(url)

# Parse JSON response
if response.status_code == 200:
    data = response.json()
    print(data)
else:
    print(f"Error: {response.status_code}")
