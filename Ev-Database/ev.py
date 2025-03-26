from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)


url = "https://ev-database.org/"
driver.get(url)
wait = WebDriverWait(driver, 10)

ev_list = []


def scrape_page():
    ev_elements = driver.find_elements(By.CLASS_NAME, "list-item")

    for ev in ev_elements:
        try:
            name = ev.find_element(By.CLASS_NAME, "title").text
            range_km = ev.find_element(By.CLASS_NAME, "erange_real").text
            battery_kwh = ev.find_element(By.CLASS_NAME, "battery").text
            efficiency = ev.find_element(By.CLASS_NAME, "efficiency").text
            price = ev.find_element(By.CLASS_NAME, "price_buy").text

            ev_list.append({
                "Name": name,
                "Range (km)": range_km,
                "Battery (kWh)": battery_kwh,
                "Efficiency (Wh/km)": efficiency,
                "Price": price
            })
        except Exception as e:
            print(f"Skipping an entry due to: {e}")


while True:
    scrape_page()

    try:
        
        next_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@class, 'next')]")))

        
        if "disabled" in next_button.get_attribute("class"):
            break

        
        ActionChains(driver).move_to_element(next_button).click().perform()
        time.sleep(3)

    except Exception:
        break 


df = pd.DataFrame(ev_list)
df.to_csv("ev_data.csv", index=False)

print(" Scraping completed. Data saved to ev_data.csv")

driver.quit()
