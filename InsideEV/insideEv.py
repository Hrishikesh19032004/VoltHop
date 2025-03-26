import requests
from bs4 import BeautifulSoup


URL = "https://insideevs.com/news/754275/xiaomi-ford-gm-outsold-evs/"


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


response = requests.get(URL, headers=HEADERS)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")

    
    title = soup.find("h1").text.strip()

    
    date = soup.find("time").text.strip() if soup.find("time") else "No Date"

    
    author_elem = soup.find("a", class_="author")
    author = author_elem.text.strip() if author_elem else "No Author"

    
    paragraphs = soup.find_all("p")
    content = "\n".join([p.text.strip() for p in paragraphs])

    
    print(f"Title: {title}")
    print(f"Date: {date}")
    print(f"Author: {author}")
    print("\nArticle Content:\n")
    print(content[:1000])  

else:
    print(f" Failed to fetch the page. Status Code: {response.status_code}")
