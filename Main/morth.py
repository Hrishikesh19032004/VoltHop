import requests
from bs4 import BeautifulSoup
import csv
from urllib.parse import urlparse

websites ={
    "EV Policy & Sales Data": "https://www.siam.in/PressRelease/1066",
    "Automotive Industry Reports": "https://www.siam.in/research",
    "EV Production & Trends": "https://www.siam.in/media/PressRelease/1089",
    "Electric Vehicle Adoption": "https://www.siam.in/ev-in-india",
    "EV Sales and Policy Updates": "https://www.siam.in/industry-data"
}


def extract_main_content(url):
    try:
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print(f"Failed to retrieve {url}, status code: {response.status_code}")
            return None, None

        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.strip() if soup.title else "No title found"

        main_tags = soup.find_all(["article", "main", "section", "div"], recursive=True)
        content_blocks = []

        for tag in main_tags:
            text = tag.get_text(separator=' ', strip=True)
            if len(text.split()) > 100:  # Only take large blocks of text
                content_blocks.append(text)

        if not content_blocks:  # If no content blocks found, take all text
            content_blocks = [soup.get_text(separator=' ', strip=True)]

        combined_text = "\n".join(content_blocks)
        lines = combined_text.splitlines()
        unique_lines = list(dict.fromkeys([line.strip() for line in lines if line.strip()]))  # Remove duplicates
        cleaned_text = " ".join(unique_lines)

        return title, cleaned_text

    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None, None

for label, url in websites.items():
    domain = urlparse(url).netloc.replace('.', '_')  # Ensure valid filename
    filename = f"{domain}.csv"

    with open(filename, "w", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Label", "URL", "Title", "Main_Content"])

        title, content = extract_main_content(url)
        if content:  # Only write to file if content was found
            writer.writerow([label, url, title, content])
        else:
            print(f"No content found for {label} at {url}")
