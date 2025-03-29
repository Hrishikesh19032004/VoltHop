### **Methods and Tools Used for Web Scraping**  

#### **1. Libraries Used**  
- **Selenium**: Automates browser actions to extract data from dynamic web pages.  
- **WebDriver Manager**: Manages the ChromeDriver automatically, ensuring compatibility.  
- **Pandas**: Stores extracted data in a structured format and saves it as a CSV file.  

#### **2. Web Scraping Process**  
- **Launched a headless Chrome browser** to access the PlugShare website.  
- **Used WebDriverWait and ActionChains** to interact with elements dynamically.  
- **Scrolled to the map section** and located charging station markers.  
- **Clicked on each marker**, extracted details like name, address, and plug types.  
- **Saved the extracted data** into a CSV file (`plugshare_stations.csv`).  

---

### **Errors and Issues Encountered**  

1. **Dynamic Content Loading**  
   - The site loads elements dynamically, causing `NoSuchElementException`.  
   - Solution: Used `WebDriverWait` to ensure elements were fully loaded.  

2. **Click Interception Error**  
   - Some elements were hidden behind overlays, preventing interaction.  
   - Solution: Used `ActionChains.move_to_element()` before clicking.  

3. **Inconsistent Element Locators**  
   - Some elements had different classes/structures on various pages.  
   - Solution: Used more robust CSS selectors (`By.CSS_SELECTOR`).  

4. **Rate Limiting or CAPTCHA Challenges**  
   - PlugShare may block excessive automated requests.  
   - Solution: Introduced delays (`time.sleep()`) between actions.  

