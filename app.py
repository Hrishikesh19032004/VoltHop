import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


options = Options()
options.add_argument("--headless")  
options.add_argument("--disable-blink-features=AutomationControlled")  
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


url = "https://www.tesla.com/inventory"
driver.get(url)
time.sleep(5)  
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5) 
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height


car_list = []
cars = driver.find_elements(By.CSS_SELECTOR, "article.result.card.vehicle-card")

for car in cars:
    try:
        model = car.find_element(By.CSS_SELECTOR, "div.tds-form-input-choice-label label").text
        try:
            price = car.find_element(By.CSS_SELECTOR, "span.tds-chip-text").text
        except:
            price = "Price Not Available"
        try:
            location = car.find_element(By.CSS_SELECTOR, "div.result-location").text
        except:
            location = "Location Not Available"

        car_list.append([model, price, location])

    except Exception as e:
        print("Error extracting car:", e)

driver.quit()


df = pd.DataFrame(car_list, columns=["Model", "Price", "Location"])
df.to_csv("tesla_inventory.csv", index=False)

print(" Tesla inventory saved to tesla_inventory.csv")
