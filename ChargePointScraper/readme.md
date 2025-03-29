
###  Methods and Tools Used:

#### **1. Web Scraping & API Interaction**
- **Requests Library**: Used to send HTTP requests to ChargePoint's API endpoints.
- **Authentication Handling**: The script authenticates via `requests.post()` to `ChargePointScraper.AUTH_URL` and retrieves a `user_id` for subsequent API calls.
- **Fetching Station Data**: The `get_station_data()` method sends a GET request to `ChargePointScraper.STATION_DATA_URL` with required parameters (latitude, longitude, user_id) to fetch EV charging station availability.

#### **2. Data Processing & Error Handling**
- **JSON Parsing**: Responses from ChargePoint's API are parsed using `.json()`. The script extracts available and total charging spots per station.
- **Exception Handling**: Custom exceptions (`ChargePointScraperException`, `ChargePointAuthenticationExpiredException`) are used to handle:
  - Invalid login credentials
  - Connection issues (`requests.exceptions.ConnectionError`)
  - Unexpected API response formats (`KeyError`, `IndexError`, `ValueError`)
  
#### **3. Live Monitoring & Notifications**
- **Real-time Monitoring**: `poll_chargepoint_stations()` continuously fetches station data at 60-second intervals.
- **Color-Coded Output**: Uses `colorama` for color-coded terminal display:
  - **Green**: All spots available
  - **Yellow**: Some spots available
  - **Red**: No spots available
- **Push Notifications**:
  - **MacOS**: `pync.Notifier` for system notifications.
  - **Boxcar API**: Sends push notifications to registered users when new charging spots become available.

---

### **Issues Encountered While Scraping ChargePoint Data:**
1. **Authentication Issues**:
   - If credentials expire or are incorrect, the scraper raises an exception.
   - ChargePoint may use CAPTCHA or session-based authentication, requiring token handling.

2. **API Response Format Changes**:
   - If ChargePoint modifies its API response structure, key extraction (`stations['station_name']`) could break.

3. **Geolocation Constraints**:
   - The script defaults to a fixed latitude/longitude range, missing stations outside this predefined area.

4. **Rate Limiting & Blocking**:
   - Frequent API requests may trigger temporary bans or require API keys with usage limits.

5. **Error in Handling Unexpected JSON Data**:
   - The script expects `'station_list'['summaries']`, but if ChargePoint returns a different structure, it fails with a `KeyError`.

