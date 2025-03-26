from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time


options = Options()
options.add_argument("--headless")  
options.add_argument("--disable-blink-features=AutomationControlled")  
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get("https://evgo.com")
time.sleep(5)  
data = []

for article in articles:
    try:
        title = article.find_element(By.TAG_NAME, "h2").text
        link = article.find_element(By.TAG_NAME, "a").get_attribute("href")
        data.append({"Title": title, "Link": link})
    except:
        continue


df = pd.DataFrame(data)
df.to_csv("evgo_data.csv", index=False)
print(" Data scraped successfully and saved to 'evgo_data.csv'")


driver.quit()
