import requests
from bs4 import BeautifulSoup
import csv
import time
import random
from urllib.parse import urlparse
import logging
import os

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)
websites = {
    "Tata Nexon EV Max System Fault": "https://www.team-bhp.com/forum/electric-cars/263539-tata-nexon-ev-max-shows-hv-system-fault-even-before-battery-reaches-9-a.html",
    "Hyundai Kona EV Battery Issues": "https://www.team-bhp.com/forum/electric-cars/231105-hyundai-kona-ev-owners-face-battery-issues-breakdowns-india.html",
    "Nexon EV Max Charging Issues in Kashmir": "https://www.team-bhp.com/forum/electric-cars/282681-bangalore-leh-tata-nexon-ev-max-stuck-kashmir-highway-charging-issues-5.html",
    "Nexon EV Max Fast Charging Stranding": "https://www.team-bhp.com/news/tata-nexon-ev-max-fast-charging-attempt-leaves-me-stranded",
    "Tiago EV Recurring Charging Issues": "https://www.team-bhp.com/news/tiago-ev-recurring-charging-issue-unhappy-tatas-service-support",
    "Charger Error Codes": "https://instachargeapp.pulseenergy.io/charger-error-codes",
    "OBDII Scanner Connection Errors": "https://www.team-bhp.com/forum/diy-do-yourself/246521-facing-errors-while-connecting-obdii-scanner-any-recommendations.html",
    "OBD-2 Trouble Codes": "https://www.mgevs.com/threads/obd-2-codes-trouble-codes.17131/",
    "MG EV Owners Group": "https://www.facebook.com/groups/232460761114676/",
    "MG EVs OBD Codes": "https://mgevs.com/threads/obd-2-codes-trouble-codes.17131/",
    "Chevy Bolt Fault Codes": "https://www.chevybolt.org/threads/fault-codes.49657/",
    "Tata Tiago EV NCAP": "https://www.globalncap.org/news/tataligorev",
    "Tata Nexon Five Star Rating": "https://www.globalncap.org/news/tata-does-it-again-five-stars-for-the-new-nexon",
    "Safest Cars in India": "https://www.acko.com/car-guide/safest-cars-in-india/",
    "PlugShare Location": "https://www.plugshare.com/location/357525",
    "EV Charging Stations Experience": "https://www.team-bhp.com/forum/electric-cars/231386-bhpians-experience-ev-charging-stations-across-india-especially-non-metros-2-print.html",
    "RFID Cards for DC Fast Charging": "https://www.team-bhp.com/forum/electric-cars/277438-comparison-rfid-cards-dc-fast-charging-evs-india.html",
    "Used Electric Cars in Mumbai": "https://www.spinny.com/used-electric-cars-in-mumbai/s/",
    "Cars24 Used EVs": "https://www.cars24.com/buy-used-electric-cars/",
    "OLX Electric Cars": "https://www.olx.in/items/q-electric-car",
    "CarDekho Used Electric Cars": "https://www.cardekho.com/used-electric+cars+in+india",
    "Carwale Used Tata Nexon EV": "https://www.carwale.com/used/tata-nexon-ev/",
    "OLX Cars Electric": "https://www.olx.in/cars_c84/q-electric-cars",
    "Droom Used Electric Cars": "https://droom.in/electric-cars/used",
    "EV Owners Switching Back to ICE": "https://economictimes.indiatimes.com/industry/renewables/from-repairs-to-resale-survey-reveals-why-most-ev-owners-in-india-want-to-switch-back-to-ice-vehicles/articleshow/112083415.cms",
    "FAME II Scheme": "https://fame2.heavyindustries.gov.in",
    "Autocar India EV News": "https://www.autocarindia.com/car-news/electric-cars",
    "Financial Express EV News": "https://www.financialexpress.com/auto/electric-vehicles/",
    "E-Amrit National Policy": "https://e-amrit.niti.gov.in/national-level-policy",
    "EV India Online News": "https://evindia.online/news",
    "Hindustan Times EV News": "https://auto.hindustantimes.com/auto/electric-vehicles",
    "EV Story News": "https://evstory.in/",
    "EV Reporter": "https://evreporter.com/",
    "EV Tech News": "https://evtechnews.in/",
    "Economic Times EV News": "https://economictimes.indiatimes.com/topic/ev",
    "CarDekho Upcoming EVs": "https://www.cardekho.com/upcomingcars/electric",
    "Carwale New Electric Cars": "https://www.carwale.com/new/electric-cars/",
    "Ola Electric": "https://en.wikipedia.org/wiki/Ola_Electric",
    "India's Greenline Mobility Investment": "https://www.reuters.com/sustainability/climate-energy/indias-greenline-mobility-invest-275-million-decarbonize-heavy-truck-fleet-2025-04-10/",
    "Financial Times EV Article": "https://www.ft.com/content/a730b0b8-b009-4b19-a83c-fc4f54e68f1f",
    "Skoda EV Investment in India": "https://www.reuters.com/business/autos-transportation/vws-skoda-invest-manufacturing-evs-india-despite-14-bln-tax-demand-overhang-2025-03-14/",
    "India Backs EV Tariff Cuts": "https://www.reuters.com/world/india/india-backs-ev-tariff-cuts-trump-trade-deal-defying-autos-lobby-sources-say-2025-04-02/",
    "BYD Blocked from Selling EVs in India": "https://www.businessinsider.com/byd-just-got-blocked-from-selling-evs-in-india-2025-4",
    "Tata Motors EV Events": "https://evolve.tatamotors.com/events/previous"
}

def extract_main_content(url):
    """
    Scrape the webpage content and extract title and main text content
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        logging.info(f"Scraping: {url}")
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            logging.error(f"Failed to retrieve {url}: Status code {response.status_code}")
            return None, None

        soup = BeautifulSoup(response.text, "html.parser")
        title = soup.title.string.strip() if soup.title else "No Title"
        
        # Try to find the most relevant content container
        main_content = None
        
        # Look for typical content containers
        for selector in ["main", "article", "#content", ".content", ".main-content", 
                         "section.main", "[role='main']", ".page-content"]:
            content_area = soup.select_one(selector)
            if content_area:
                main_content = content_area
                break
        
        # If no specific container found, use the body
        if not main_content:
            main_content = soup.body
        
        if main_content:
            # Remove navigation, footer, scripts, etc.
            for unwanted in main_content.select('nav, footer, header, script, style, .menu, .navigation, .sidebar, .footer, .header, .nav'):
                unwanted.decompose()
            
            # Get the text content
            content = main_content.get_text(separator=' ', strip=True)
            
            # Clean up content - remove excessive whitespace
            content = ' '.join(content.split())
            
            # Truncate very long content (optional)
            if len(content) > 10000:
                content = content[:10000] + "... [content truncated]"
                
            return title, content
        else:
            logging.warning(f"No main content found for {url}")
            return title, "No content found"

    except requests.exceptions.RequestException as e:
        logging.error(f"Request error for {url}: {e}")
        return None, None
    except Exception as e:
        logging.error(f"Error processing {url}: {e}")
        return None, None

def get_domain_name(url):
    """Extract a clean domain name from URL"""
    parsed_url = urlparse(url)
    domain = parsed_url.netloc
    # Remove 'www.' if present
    if domain.startswith('www.'):
        domain = domain[4:]
    return domain

def get_output_filename(url):
    """Generate filename based on domain"""
    domain = get_domain_name(url)
    # Replace any remaining dots with underscores
    clean_domain = domain.replace('.', '_')
    return f"{clean_domain}.csv"

def append_to_csv(filename, row_data):
    """Append data to CSV file, create with headers if doesn't exist"""
    file_exists = os.path.isfile(filename)
    
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if not file_exists:
            writer.writerow(["Label", "URL", "Title", "Description"])
        writer.writerow(row_data)

def main():
    """
    Main function to run the scraper and save results to domain-specific files
    """
    # Create output directory if it doesn't exist
    output_dir = "scraped_data"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Track which domains we've already processed
    processed_domains = set()
    
    # Counter for progress reporting
    total_urls = len(websites)
    processed = 0
    
    # Set to track which files we've created in this run
    created_files = set()
    
    for label, url in websites.items():
        try:
            # Add delay between requests to avoid overloading the server
            delay = random.uniform(1.0, 3.0)
            time.sleep(delay)
            
            # Get domain name and create filename
            domain = get_domain_name(url)
            filename = os.path.join(output_dir, get_output_filename(url))
            
            # Track new files for this run
            if filename not in created_files and not os.path.exists(filename):
                created_files.add(filename)
            
            title, content = extract_main_content(url)
            
            if title and content:
                append_to_csv(filename, [label, url, title, content])
                logging.info(f"Successfully scraped: {label} ({url}) - Saved to {filename}")
            else:
                append_to_csv(filename, [label, url, "Failed to retrieve", ""])
                logging.warning(f"Failed to extract content from: {label} ({url})")
            
            # Update progress
            processed += 1
            if processed % 5 == 0 or processed == total_urls:
                logging.info(f"Progress: {processed}/{total_urls} URLs processed ({processed/total_urls*100:.1f}%)")
                
        except Exception as e:
            logging.error(f"Unexpected error processing {label} ({url}): {e}")
            # Try to save the error information
            filename = os.path.join(output_dir, get_output_filename(url))
            try:
                append_to_csv(filename, [label, url, "Error", str(e)])
            except:
                logging.error(f"Could not save error information to file")
    
    logging.info(f"Scraping complete. Results saved to domain-specific files in {output_dir} directory")

if __name__ == "__main__":
    main()