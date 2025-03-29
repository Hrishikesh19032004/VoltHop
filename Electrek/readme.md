### **Methods and Tools Used in Web Scraping:**

#### **1. Requests Library**  
- **`requests.get(BASE_URL, headers=HEADERS)`**: Sends an HTTP GET request to **Electrek's EV guide page** with a user-agent header to mimic a real browser and avoid blocking.

#### **2. BeautifulSoup (bs4)**  
- **`soup = BeautifulSoup(response.text, "html.parser")`**: Parses the webpage's HTML content.
- **`soup.find_all("article")`**: Finds all `<article>` elements, which likely contain EV news articles.
- **Extracting Data:**
  - **Title** → `article.find("h3").text.strip()`  
  - **Link** → `article.find("a")["href"]`  
  - **Description** → `article.find("p").text.strip()`  

#### **3. Pandas for Data Storage**  
- **`pd.DataFrame(data)`**: Converts the extracted data into a structured table.
- **`df.to_csv("Elecktrek_ev_articles.csv", index=False)`**: Saves the data to a CSV file.

---

### **Errors and Issues Encountered:**
1. **Website Blocking or CAPTCHA:**  
   - Electrek may block automated requests or use **Cloudflare protection**, causing `403 Forbidden` errors.
   - Solution: **Use rotating proxies, CAPTCHA solvers, or Selenium for dynamic content.**

2. **Changing HTML Structure:**  
   - If `article.find("h3")` or `article.find("p")` returns `None`, the script throws an **AttributeError**.
   - Solution: **Use `.get_text(strip=True)` with default values to handle missing elements.**

3. **Encoding Issues in CSV Output:**  
   - Some articles may contain special characters, causing encoding errors.
   - Solution: **Save CSV with UTF-8 encoding (`df.to_csv("file.csv", encoding="utf-8-sig")`).**

