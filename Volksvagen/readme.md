### **Methods and Tools Used for Web Scraping**  

#### **1. Tools & Libraries**  
- **Playwright**: Automates web interactions and handles dynamic elements efficiently.  
- **JSON & Pandas**: Stores extracted data in structured formats (JSON & CSV).  

#### **2. Web Scraping Process**  
- **Launched a Chromium browser** (non-headless for debugging).  
- **Navigated to Volkswagen’s model page** and waited for it to load.  
- **Scrolled down multiple times** to load more vehicle models dynamically.  
- **Clicked the "Mehr anzeigen" (Load More) button** to reveal additional models.  
- **Extracted details** such as model name, price, description, and configuration link.  
- **Saved data in JSON & CSV formats** for further analysis.  

---

### **Errors and Issues Encountered**  

1. **Slow Loading & Timeouts**  
   - The page took longer than expected to load all elements.  
   - Solution: Increased `timeout` values and used `wait_for_selector()`.  

2. **Dynamic Content Not Fully Loaded**  
   - Scrolling sometimes didn’t trigger all vehicle models to appear.  
   - Solution: Implemented multiple scroll attempts (`window.scrollBy()`).  

3. **"Mehr anzeigen" Button Not Always Available**  
   - The "Load More" button wasn’t always present.  
   - Solution: Used `query_selector()` with a conditional check before clicking.  

4. **Encoding Issues in CSV Output**  
   - Special characters (e.g., German umlauts) caused encoding problems.  
   - Solution: Used `utf-8` encoding for JSON & CSV exports.  

