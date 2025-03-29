### **Methods and Tools Used in Web Scraping**

#### **1. Libraries Used**
- **Requests**: Used to send an HTTP request (`requests.get()`) to fetch the webpage content.  
- **BeautifulSoup (bs4)**: Parses the HTML response and extracts required information.  
- **Pandas**: Stores scraped data in a structured format and exports it to CSV.

#### **2. Web Scraping Approach**
- **Fetching Webpages**:  
  - Sent an HTTP GET request with a custom **User-Agent** to avoid bot detection.  
  - Checked for a successful response (`response.status_code == 200`).  

- **Extracting Article Details**:  
  - Used **`soup.find("h1")`** to extract the title.  
  - **`soup.find("time")`** to get the published date.  
  - **`soup.find("a", class_="author")`** to find the author.  
  - **`soup.find_all("p")`** to collect the article content.  

- **Scraping Multiple Articles from the News Page**:  
  - **`soup.find_all("article")`** to find all articles on the page.  
  - Extracted **title, link, date, and description**.  
  - Appended data to a **Pandas DataFrame** and saved it to `insideevs_news.csv`.

---

### **Errors and Issues Encountered**
1. **Bot Detection & Blocking**  
   - Some pages may block automated requests despite using a user-agent string.  
   - Solution: **Selenium** could be used to mimic real user interactions.  

2. **Missing or Dynamic Elements**  
   - Some articles didn’t have an author or description, returning `None`.  
   - Solution: Used conditional checks (`if element else "No Data"`) to avoid errors.  

3. **Inconsistent HTML Structure**  
   - The structure of different news articles varied slightly, affecting extraction.  
   - Solution: Used multiple class selectors and alternative methods.  

