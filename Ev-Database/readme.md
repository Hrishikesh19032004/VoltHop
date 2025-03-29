### **Methods and Tools Used in Web Scraping:**

#### **1. Selenium WebDriver**  
- **Automates Chrome Browser**: Uses **`webdriver.Chrome`** to interact with web pages.  
- **Headless Mode**: Enables `--headless` mode to run without opening a browser window.  
- **Bypass Automation Detection**: Includes `"--disable-blink-features=AutomationControlled"` to avoid detection.  

#### **2. Web Scraping Techniques**  
- **Finding Elements**: Uses `find_element(By.CLASS_NAME, "title")` and `find_elements(By.CLASS_NAME, "list-item")` to locate key details like EV name, range, battery capacity, efficiency, and price.  
- **Handling Pagination**: Implements a loop to click the "Next" button until no more pages are available (`element_to_be_clickable((By.XPATH, "//a[contains(@class, 'next')]"))`).  

#### **3. Data Storage**  
- **Pandas DataFrame**: Extracted data is stored in a structured format.  
- **CSV Export**: Saves as `"ev_data.csv"` using `df.to_csv("ev_data.csv", index=False)`.  

---

### **Errors and Issues Encountered:**
1. **JavaScript-Rendered Content:**  
   - Some elements are dynamically loaded, causing `NoSuchElementException`.  
   - Solution: Used `WebDriverWait` to ensure elements load before interaction.  

2. **Anti-Scraping Measures:**  
   - Websites may detect automation tools and block access.  
   - Solution: Used a **custom user-agent**, `--headless` mode, and `ActionChains` for human-like interactions.  

3. **Pagination Issues:**  
   - Some sites don’t have a standard "Next" button or disable it dynamically.  
   - Solution: Used **explicit waits** (`WebDriverWait(driver, 10)`) and checked if the button is **disabled** before proceeding.  

