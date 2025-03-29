### **Methods and Tools Used in API Data Retrieval**

#### **1. Libraries Used**
- **Requests**: Used to send HTTP requests (`requests.get()`) to the API endpoint.  
- **JSON Handling**: Used `response.json()` to parse the API response into a Python dictionary.  

#### **2. API Data Retrieval Process**
- Constructed the API URL with an **API key** for authentication.  
- Used `requests.get(url)` to send an HTTP GET request.  
- Checked the response status (`response.status_code == 200`), ensuring successful data retrieval.  
- Extracted and printed the JSON data.

---

### **Errors and Issues Encountered**
1. **Invalid or Expired API Key**  
   - If the API key is incorrect or expired, the API may return a **403 Forbidden** or **401 Unauthorized** error.  
   - Solution: Ensure the API key is active and correctly formatted.  

2. **Rate Limits**  
   - The API may restrict the number of requests per hour/day.  
   - Solution: Implement retries and check the API’s rate limit policy.  

3. **Network Errors**  
   - Connection issues may cause timeouts or failures (`requests.exceptions.RequestException`).  
   - Solution: Use exception handling (`try-except`) and implement retries with exponential backoff.  

4. **Invalid JSON Response**  
   - Some API responses may be malformed or empty.  
   - Solution: Check for `"error"` fields in the response and handle missing data safely.  


