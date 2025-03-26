import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_URL = "https://insideevs.com/news/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

response = requests.get(BASE_URL, headers=HEADERS)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    articles = soup.find_all("article")
    data = []

    for article in articles:
        title_elem = article.find("a", class_="title")
        title = title_elem.text.strip() if title_elem else "No Title"
        link = "https://insideevs.com" + title_elem["href"] if title_elem else "No Link"
        date_elem = article.find("time")
        date = date_elem.text.strip() if date_elem else "No Date"
        desc_elem = article.find("p")
        description = desc_elem.text.strip() if desc_elem else "No Description"
        data.append({"Title": title, "Link": link, "Date": date, "Description": description})

    df = pd.DataFrame(data)
    df.to_csv("insideevs_news.csv", index=False)
    print("Scraped successfully! Data saved to 'insideevs_news.csv'")

else:
    print(f"Failed to fetch the page. Status Code: {response.status_code}")
