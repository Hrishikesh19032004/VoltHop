from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-popup-blocking")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

url = "https://chargefinder.com/en/search"
driver.get(url)
time.sleep(5)

for _ in range(30):
    driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
    time.sleep(2)

stations = driver.find_elements(By.CLASS_NAME, "station-list__item")

data = []
for station in stations:
    try:
        name = station.find_element(By.CLASS_NAME, "station-name").text
        location = station.find_element(By.CLASS_NAME, "station-location").text
        availability = station.find_element(By.CLASS_NAME, "station-availability").text
        data.append((name, location, availability))
    except:
        continue

driver.quit()

for item in data:
    print(item)
