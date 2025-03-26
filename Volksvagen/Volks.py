from playwright.sync_api import sync_playwright
import json
import pandas as pd
import time

def scrape_vw_ev_models():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context()
        page = context.new_page()

        page.goto("https://www.volkswagen.de/de/modelle-und-konfigurator.html", timeout=180000, wait_until="load")

        for _ in range(15):
            page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            time.sleep(2)
            
            load_more_button = page.query_selector('button:has-text("Mehr anzeigen")')
            if load_more_button:
                load_more_button.click()
                time.sleep(3)

        page.wait_for_selector('.owc-teaser-vehicle-card', timeout=120000)

        ev_models = page.evaluate('''() => {
            return Array.from(document.querySelectorAll('.owc-teaser-vehicle-card')).map(card => ({
                "Model": card.querySelector('.owc-teaser-vehicle-card__heading')?.innerText.trim() || 'N/A',
                "Price": card.querySelector('.owc-price')?.innerText.trim() || 'N/A',
                "Description": card.querySelector('.owc-teaser-vehicle-card__copy')?.innerText.trim() || 'N/A',
                "Config_Link": card.querySelector('.owc-teaser-vehicle-card__cta a')?.href || 'N/A'
            }));
        }''')

        with open('vw_ev_models.json', 'w', encoding='utf-8') as f:
            json.dump(ev_models, f, indent=2, ensure_ascii=False)

        df = pd.DataFrame(ev_models)
        df.to_csv('vw_ev_models.csv', index=False, encoding='utf-8')

        browser.close()

scrape_vw_ev_models()