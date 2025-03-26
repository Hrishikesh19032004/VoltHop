import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://electrek.co/guides/ev/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = requests.get(BASE_URL, headers=HEADERS)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article")

    data = []
    
    for article in articles:
        title_elem = article.find("h3")
        title = title_elem.text.strip() if title_elem else "No Title"
        
        link_elem = article.find("a")
        link = link_elem["href"] if link_elem else "No Link"
        
        desc_elem = article.find("p")
        description = desc_elem.text.strip() if desc_elem else "No Description"
        
        data.append({"Title": title, "Link": link, "Description": description})
    
    df = pd.DataFrame(data)
    df.to_csv("Elecktrek_ev_articles.csv", index=False)
    
    print(" EV articles scraped and saved as 'ev_articles.csv'.")
    
else:
    print(f" Failed to fetch page. Status Code: {response.status_code}")
