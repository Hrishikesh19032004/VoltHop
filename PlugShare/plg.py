from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1920,1080")
options.add_argument("--no-sandbox")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url = "https://www.plugshare.com/"
driver.get(url)
wait = WebDriverWait(driver, 20)
actions = ActionChains(driver)

wait.until(EC.presence_of_element_located((By.ID, "map")))

driver.execute_script("document.querySelector('#map').scrollIntoView();")
time.sleep(2)

def scrape_charging_stations():
    charging_stations = []
    markers = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "button[title*='Charger']")))

    for i, marker in enumerate(markers[:5]):
        try:
            actions.move_to_element(marker).click().perform()
            time.sleep(3)

            name = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".infodetails .name"))).text
            address = driver.find_element(By.CSS_SELECTOR, ".infodetails .address").text
            plug_types = driver.find_element(By.CSS_SELECTOR, ".plugs").text

            charging_stations.append({
                "Name": name,
                "Address": address,
                "Plug Types": plug_types
            })

            close_button = driver.find_element(By.CSS_SELECTOR, "button[aria-label='Close']")
            close_button.click()
            time.sleep(2)

        except Exception as e:
            print(f"Error extracting data: {e}")

    return charging_stations

stations = scrape_charging_stations()

df = pd.DataFrame(stations)
df.to_csv("plugshare_stations.csv", index=False)

driver.quit()

print("Scraping complete. Data saved to plugshare_stations.csv")
