import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urljoin, urlparse

websites = {
    "InsideEVs EV Policies": "https://insideevs.com/news/456312/ev-policy-global/",
    "InsideEVs EV Guidelines": "https://insideevs.com/news/456312/ev-policy-global/",
    "InsideEVs EV Standards": "https://insideevs.com/news/456312/ev-policy-global/",
    "InsideEVs EV Incentives": "https://insideevs.com/news/456312/ev-policy-global/",
    "InsideEVs EV News": "https://insideevs.com/news/"
}


def extract_main_content(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            return None, None

        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.strip() if soup.title else ""

        main_tags = soup.find_all(["article", "main", "section", "div"], recursive=True)
        content_blocks = []

        for tag in main_tags:
            text = tag.get_text(separator=' ', strip=True)
            if len(text.split()) > 100:
                content_blocks.append(text)

        if not content_blocks:
            content_blocks = [soup.get_text(separator=' ', strip=True)]

        combined_text = "\n".join(content_blocks)
        lines = combined_text.splitlines()
        unique_lines = list(dict.fromkeys([line.strip() for line in lines if line.strip()]))
        cleaned_text = " ".join(unique_lines)

        return title, cleaned_text

    except Exception:
        return None, None

def extract_links_from_page(base_url):
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code != 200:
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        article_links = set()

        for a in soup.find_all("a", href=True):
            href = a["href"]
            full_url = urljoin(base_url, href)
            if urlparse(full_url).netloc == urlparse(base_url).netloc and "/20" in href:
                article_links.add(full_url)

        return list(article_links)

    except Exception:
        return []

filename = "insideEV.csv"

with open(filename, "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Label", "URL", "Title", "Main_Content"])

    for label, base_url in websites.items():
        page_urls = extract_links_from_page(base_url)
        if not page_urls:
            page_urls = [base_url]

        for url in page_urls:
            title, content = extract_main_content(url)
            if content:
                writer.writerow([label, url, title, content])
