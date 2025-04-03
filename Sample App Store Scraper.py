import pandas as pd
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import random
import time
import json
from datetime import datetime
import re
from urllib.parse import unquote

# ===== CONFIGURATION =====
MAX_APPS = 50
COUNTRY = "us"
LANGUAGE = "en"
OUTPUT_FILE = "playstore_data.xlsx"
HEADLESS = True
LOAD_TIMEOUT = 90000  # 90 seconds
REQUEST_DELAY = (3, 7)


# =========================

def safe_text(element, default="Not Available"):
    return element.text.strip() if element and element.text.strip() else default


def safe_attr(element, attr, default="Not Available"):
    return element.get(attr, default) if element and element.get(attr) else default


def nuclear_json_extract(data, keys, default="Not Available"):
    try:
        for key in keys.split('.'):
            if isinstance(data, list):
                data = data[0].get(key, default) if data else default
            else:
                data = data.get(key, default)
        return data if data and data != default else default
    except:
        return default


def get_element_pair(soup, primary_text, sibling_tag='div', default="Not Available"):
    try:
        primary = soup.find('div', string=re.compile(primary_text))
        if not primary:
            return (default, default)
        sibling = primary.find_next_sibling(sibling_tag)
        return (
            safe_text(primary, default),
            safe_text(sibling, default)
        )
    except:
        return (default, default)


def parse_installs(installs_text):
    try:
        if not installs_text:
            return (0, 0)

        clean_text = installs_text.replace(',', '').replace('+', '').strip()

        if 'M' in clean_text:
            num = float(re.search(r'\d+\.?\d*', clean_text).group())
            return (int(num * 1_000_000), int(num * 1_000_000))
        if 'K' in clean_text:
            num = float(re.search(r'\d+\.?\d*', clean_text).group())
            return (int(num * 1_000), int(num * 1_000))
        if '-' in clean_text:
            nums = [int(n) for n in re.findall(r'\d+', clean_text)]
            return (min(nums), max(nums)) if nums else (0, 0)
        if match := re.search(r'\d+', clean_text):
            num = int(match.group())
            return (num, num)
        return (0, 0)
    except:
        return (0, 0)


def get_app_ids():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale=LANGUAGE
        )
        context.add_init_script("""
            delete navigator.__proto__.webdriver;
            Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]});
        """)

        page = context.new_page()
        page.goto(
            f"https://play.google.com/store/apps/top?hl={LANGUAGE}&gl={COUNTRY}",
            timeout=120000,
            wait_until="networkidle"
        )

        for _ in range(5):
            page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            time.sleep(random.uniform(1, 2))

        content = page.content()
        soup = BeautifulSoup(content, 'html.parser')
        app_links = list({
            a['href'].split('id=')[1]
            for a in soup.select('a[href^="/store/apps/details?id="]')
        })[:MAX_APPS]
        browser.close()
        return app_links


def scrape_app(page, app_id):
    for attempt in range(3):
        try:
            page.goto(
                f"https://play.google.com/store/apps/details?id={app_id}",
                timeout=LOAD_TIMEOUT,
                wait_until="domcontentloaded"
            )
            page.wait_for_selector('h1', state='attached', timeout=30000)

            content = page.content()
            soup = BeautifulSoup(content, 'html.parser')
            script_tag = soup.find('script', type='application/ld+json')
            json_data = json.loads(script_tag.string) if script_tag else {}

            # Data extraction
            installs_text = get_element_pair(soup, 'Downloads|Installs')[1]
            min_installs, max_installs = parse_installs(installs_text)

            return {
                'App Name': safe_text(soup.find('h1'), nuclear_json_extract(json_data, 'name')),
                'App ID': app_id,
                'Category': safe_text(soup.find('a', {'itemprop': 'genre'}),
                                      nuclear_json_extract(json_data, 'applicationCategory')),
                'Rating': float(nuclear_json_extract(json_data, 'aggregateRating.ratingValue', 0)),
                'Rating Count': int(nuclear_json_extract(json_data, 'aggregateRating.ratingCount', 0)),
                'Price': nuclear_json_extract(json_data, 'offers.price', 'Free'),
                'Currency': nuclear_json_extract(json_data, 'offers.priceCurrency', 'Not Available'),
                'Free': 'Free' if 'Free' in str(nuclear_json_extract(json_data, 'offers.price')) else 'Paid',
                'Size': get_element_pair(soup, 'Size')[1],
                'Installs': installs_text,
                'Minimum Installs': min_installs,
                'Maximum Installs': max_installs,
                'Minimum Android': get_element_pair(soup, 'Requires Android')[1],
                'Last Updated': get_element_pair(soup, 'Updated on')[1],
                'Content Rating': get_element_pair(soup, 'Rated for')[1],
                'Developer': nuclear_json_extract(json_data, 'author.name', get_element_pair(soup, 'Offered By')[1]),
                'Developer ID': unquote(app_id.split('.')[0]) if '.' in app_id else 'Not Available',
                'Developer Email': safe_attr(soup.find('a', href=re.compile(r'mailto:')), 'href').replace('mailto:',
                                                                                                          ''),
                'Developer Website': safe_attr(soup.find('a', {'aria-label': 'Visit developer\'s website'}), 'href'),
                'Privacy Policy': nuclear_json_extract(json_data, 'privacyPolicy', 'Not Available'),
                'In-App Purchases': 'Yes' if soup.find('div', string='In-app purchases') else 'No',
                'Ad Supported': 'Yes' if soup.find('div', string='Contains ads') else 'No',
                'Editors Choice': 'Yes' if soup.find('meta', {'name': 'editorsChoiceBadgeUrl'}) else 'No',
                'Released Date': get_element_pair(soup, 'Released on')[1],
                'Current Version': get_element_pair(soup, 'Current Version')[1],
                'App Icon URL': safe_attr(soup.find('img', {'alt': 'Icon image'}), 'src'),
                'Screenshots': [safe_attr(img, 'src') for img in soup.select('img[alt^="Screenshot Image"]')],
                'Promo Video': safe_attr(soup.find('meta', property='og:video'), 'content'),
                'Description': safe_text(soup.find('div', {'data-g-id': 'description'})),
                'Short Description': f"{safe_text(soup.find('div', {'data-g-id': 'description'}))[:197]}..." if soup.find(
                    'div', {'data-g-id': 'description'}) else 'Not Available',
                'Recent Changes': get_element_pair(soup, "What's new")[1],
                'Interactive Elements': [safe_text(el) for el in
                                         soup.select('div[aria-label="Interactive Elements"] div')],
                'Supported Languages': [safe_text(lang) for lang in
                                        soup.select('div[aria-label="Supported Languages"] div')],
                'Country': COUNTRY,
                'Language': LANGUAGE,
                'Scraped At': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

        except Exception as e:
            print(f"Attempt {attempt + 1} failed for {app_id}: {str(e)}")
            time.sleep(5)

    return {
        'App ID': app_id,
        'Error': 'Failed after 3 attempts',
        'Scraped At': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


def main():
    print("🚀 Starting scraping process...")
    app_ids = get_app_ids()
    print(f"🎯 Found {len(app_ids)} apps")

    results = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=HEADLESS)
        context = browser.new_context()
        page = context.new_page()

        for idx, app_id in enumerate(app_ids):
            print(f"⚡ Processing {idx + 1}/{len(app_ids)}: {app_id}")
            result = scrape_app(page, app_id)
            results.append(result)
            time.sleep(random.uniform(*REQUEST_DELAY))

        browser.close()

    df = pd.DataFrame(results)
    df.to_excel(OUTPUT_FILE, index=False)
    print(f"✅ Success! Saved {len(results)} apps to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()