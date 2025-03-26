import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


options = Options()
options.add_argument("--headless") 
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


url = "https://www.tesla.com/inventory"
driver.get(url)


time.sleep(5)


html_source = driver.page_source
driver.quit()


with open("tesla_page_source.html", "w", encoding="utf-8") as file:
    file.write(html_source)

print("Page source saved to 'tesla_page_source.html'. Open this file to inspect the structure.")
