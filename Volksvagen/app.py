import requests
from bs4 import BeautifulSoup
import csv

url = "https://www.volkswagen.de/de/modelle-und-konfigurator.html"
headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

cars = soup.find_all("li", {"data-testid": "cartile"})

with open("car_data.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["Car Name", "Price"])

    for car in cars:
        car_name = car.get("aria-label", "Car name not found")
        price_element = car.find("div", class_="StyledTextComponent-sc-hqqa9q xzMkt")
        price = price_element.text.strip() if price_element else "Price not found"
        writer.writerow([car_name, price])

print("Data successfully saved to car_data.csv!")
