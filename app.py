# # # import os
# # # import datetime
# # # from datetime import timedelta
# # # import requests
# # # from bs4 import BeautifulSoup
# # # from flask import Flask, request, jsonify, session
# # # from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# # # from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# # # from flask_cors import CORS
# # # from pymongo import MongoClient
# # # from apscheduler.schedulers.background import BackgroundScheduler
# # # import smtplib
# # # from email.mime.text import MIMEText
# # # from dotenv import load_dotenv
# # # from flasgger import Swagger, swag_from
# # # from selenium import webdriver
# # # from selenium.webdriver.chrome.options import Options
# # # from selenium.webdriver.chrome.service import Service
# # # from webdriver_manager.chrome import ChromeDriverManager
# # # from selenium.webdriver.common.by import By
# # # from selenium.webdriver.support.ui import WebDriverWait
# # # from selenium.webdriver.support import expected_conditions as EC
# # # from dateutil.parser import parse
# # # from datetime import datetime, timezone
# # # from bson.objectid import ObjectId
# # # import re
# # # import time

# # # load_dotenv()

# # # app = Flask(__name__)
# # # app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')
# # # CORS(app)

# # # # JWT Setup
# # # jwt = JWTManager(app)
# # # app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret')

# # # # Login Manager
# # # login_manager = LoginManager()
# # # login_manager.init_app(app)

# # # # Swagger Setup
# # # swagger = Swagger(app, template={
# # #     "swagger": "2.0",
# # #     "info": {
# # #         "title": "AusClassicAuctions API",
# # #         "description": "API for Australian Classic Car Auctions Aggregator",
# # #         "version": "1.0.0"
# # #     },
# # #     "securityDefinitions": {
# # #         "Bearer": {
# # #             "type": "apiKey",
# # #             "name": "Authorization",
# # #             "in": "header",
# # #             "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
# # #         }
# # #     }
# # # })

# # # # MongoDB Setup
# # # client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/'))
# # # db = client['ausclassicauctions']
# # # lots_collection = db['lots']  # Current and upcoming lots
# # # sold_collection = db['sold']  # Sold archive
# # # users_collection = db['users']
# # # watchlists_collection = db['watchlists']
# # # saved_searches_collection = db['saved_searches']

# # # # User Model
# # # class User(UserMixin):
# # #     def __init__(self, id, email):
# # #         self.id = id
# # #         self.email = email

# # # @login_manager.user_loader
# # # def load_user(user_id):
# # #     user = users_collection.find_one({'_id': ObjectId(user_id)})
# # #     if user:
# # #         return User(user['_id'], user['email'])
# # #     return None

# # # # Scraping Sources
# # # SOURCES = [
# # #         {'url': 'https://www.tradinggarage.com', 'name': 'tradinggarage'},

# # #     {'url': 'https://carbids.com.au/t/unique-and-classic-car-auctions#!?page=1&count=96&filter%5BDisplay%5D=true', 'name': 'carbids'},
# # #     {'url': 'https://collectingcars.com/buy?refinementList%5BlistingStage%5D%5B0%5D=live&refinementList%5BregionCode%5D%5B0%5D=APAC&refinementList%5BcountryCode%5D%5B0%5D=AU', 'name': 'collectingcars'},
# # #     # {'url': 'https://burnsandcoauctions.com.au', 'name': 'burnsandco'},
# # #     # {'url': 'https://www.lloydsonline.com.au/AuctionLots.aspx?smode=0&aid=65946', 'name': 'lloydsonline'},
# # #     # {'url': 'https://www.seven82motors.com.au', 'name': 'seven82motors'},
# # #     # {'url': 'https://www.chicaneauctions.com.au', 'name': 'chicaneauctions'},
# # #     # {'url': 'https://www.doningtonauctions.com.au', 'name': 'doningtonauctions'},
# # #     {'url': 'https://www.bennettsclassicauctions.com.au', 'name': 'bennettsclassicauctions'}
# # # ]

# # # def get_driver():
# # #     options = Options()
# # #     options.headless = True
# # #     service = Service(ChromeDriverManager().install())
# # #     return webdriver.Chrome(service=service, options=options)

# # # def scrape_site(source):
# # #     url = source['url']
# # #     name = source['name']
# # #     if name == 'bennettsclassicauctions':
# # #         return scrape_bennetts(url)
# # #     elif name == 'burnsandco':
# # #         return scrape_burnsandco(url)
# # #     elif name == 'carbids':
# # #         return scrape_carbids(url)
# # #     elif name == 'tradinggarage':
# # #         return scrape_tradinggarage(url)    
# # #     elif name == 'collectingcars':
# # #         return scrape_collectingcars()
# # #     else:
# # #         # Generic scraper for other sites (placeholder)
# # #         try:
# # #             driver = get_driver()
# # #             driver.get(url)
# # #             soup = BeautifulSoup(driver.page_source, 'html.parser')
# # #             driver.quit()

# # #             listings = []
# # #             item_class = 'auction-item'  # Generic; adjust per site
# # #             for item in soup.find_all('div', class_=item_class):
# # #                 lot = parse_lot(item, url)
# # #                 if lot and is_classic(lot):
# # #                     lot['source'] = url
# # #                     listings.append(lot)
# # #             return listings
# # #         except Exception as e:
# # #             print(f"Error scraping {url}: {e}")
# # #             return []




# # # def scrape_tradinggarage(base_url="https://www.tradinggarage.com"):
# # #     """
# # #     Simple Trading Garage scraper using public APIs.
# # #     Prints the name/title of each car as it scrapes.
# # #     (No pagination needed - returns all auctions at once)
# # #     """
# # #     listings = []
# # #     print("Starting Trading Garage API scrape...\n")

# # #     session = requests.Session()
# # #     session.headers.update({
# # #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
# # #                      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
# # #         'Accept': 'application/json',
# # #         'Referer': 'https://www.tradinggarage.com/',
# # #     })

# # #     # Two main endpoints (all cars returned in one call each)
# # #     endpoints = {
# # #         'live': 'https://portal.tradinggarage.com/api/v1/auctions?status=live',
# # #         'coming_soon': 'https://portal.tradinggarage.com/api/v1/auctions?status=coming_soon'
# # #     }

# # #     for status, api_url in endpoints.items():
# # #         try:
# # #             print(f"Fetching {status.upper()} auctions...")
# # #             r = session.get(api_url, timeout=12)

# # #             if r.status_code != 200:
# # #                 print(f"→ {status.upper()} failed (HTTP {r.status_code})\n")
# # #                 continue

# # #             data = r.json()

# # #             auctions = (
# # #                 data.get('data', []) or
# # #                 data.get('auctions', []) or
# # #                 data.get('items', []) or
# # #                 data.get('results', []) or []
# # #             )

# # #             if not auctions:
# # #                 print(f"→ {status.upper()}: No auctions found\n")
# # #                 continue

# # #             print(f"→ {status.upper()}: Found {len(auctions)} auctions\n")

# # #             for auction in auctions:
# # #                 # Build basic car name/title
# # #                 title = auction.get('title') or auction.get('name', 'Unknown Car')
# # #                 year = str(auction.get('year', ''))
# # #                 make = auction.get('make', '')
# # #                 model = auction.get('model', '')

# # #                 # Clean and pretty name
# # #                 car_name = f"{year} {make} {model}".strip()
# # #                 if not car_name or car_name == year:
# # #                     car_name = title

# # #                 # Print the car name immediately
# # #                 print(f"Scraped: {car_name}")

# # #                 # Full lot data (same as before)
# # #                 lot = {
# # #                     'source': 'tradinggarage',
# # #                     'status': status,
# # #                     'auction_id': auction.get('id') or auction.get('auctionId'),
# # #                     'title': title,
# # #                     'year': year,
# # #                     'make': make,
# # #                     'model': model,
# # #                     'odometer': auction.get('odometer') or auction.get('mileage', ''),
# # #                     'price': (
# # #                         auction.get('currentBid') or
# # #                         auction.get('buyNowPrice') or
# # #                         auction.get('estimate') or
# # #                         auction.get('startingPrice') or
# # #                         'TBA'
# # #                     ),
# # #                     'auction_date': None,
# # #                     'location': auction.get('location', 'Online / Melbourne'),
# # #                     'images': auction.get('images', []) or [auction.get('mainImage', '')],
# # #                     'url': auction.get('url') or f"https://www.tradinggarage.com/auctions/{auction.get('slug') or auction.get('id') or ''}",
# # #                     'description': auction.get('description', ''),
# # #                     'reserve': auction.get('reserveStatus', 'Yes'),
# # #                     'scrape_time': datetime.now(timezone.utc).isoformat()
# # #                 }

# # #                 # Try to get auction date
# # #                 for date_key in ['endDate', 'closingDate', 'auctionDate', 'endsAt', 'startsAt']:
# # #                     if auction.get(date_key):
# # #                         try:
# # #                             lot['auction_date'] = parse(auction[date_key]).isoformat()
# # #                             break
# # #                         except:
# # #                             pass

# # #                 # Fallback parsing from title if needed
# # #                 if not lot['make'] or not lot['model']:
# # #                     m = re.search(r'(\d{4})\s*([a-zA-Z]+)\s*(.+?)(?:\s+|$)', lot['title'])
# # #                     if m:
# # #                         lot['year'] = m.group(1)
# # #                         lot['make'] = m.group(2).capitalize()
# # #                         lot['model'] = m.group(3).strip().capitalize()

# # #                 if is_classic(lot):
# # #                     listings.append(lot)

# # #             print("")  # empty line between statuses

# # #         except Exception as e:
# # #             print(f"→ {status.upper()} error: {str(e)}\n")

# # #     print(f"Trading Garage total collected: {len(listings)} classic cars\n")
# # #     print(listings)
# # #     return listings
# # # import requests
# # # from datetime import datetime, timezone
# # # from dateutil.parser import parse
# # # import re
# # # import time

# # # def scrape_collectingcars():
# # #     """
# # #     Scraper for Collecting Cars (Australia/APAC live auctions)
# # #     Uses the Typesense multi_search API (no Selenium needed)
# # #     Prints each car's title as it's scraped.
# # #     (Confirmed working January 2026)
# # #     """
# # #     listings = []
# # #     print("Starting Collecting Cars API scrape...\n")

# # #     api_url = "https://dora.production.collecting.com/multi_search"

# # #     headers = {
# # #         'x-typesense-api-key': 'aKIufK0SfYHMRp9mUBkZPR7pksehPBZq',
# # #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
# # #                      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
# # #         'Accept': 'application/json',
# # #         'Content-Type': 'application/json',
# # #         'Referer': 'https://collectingcars.com/',
# # #     }

# # #     # Base payload (your original + pagination support)
# # #     base_payload = {
# # #         "searches": [
# # #             {
# # #                 "query_by": "title,productMake,vehicleMake,productYear,tags,lotType,driveSide,location,collectionId,modelId",
# # #                 "query_by_weights": "9,8,7,6,5,4,3,2,1,0",
# # #                 "text_match_type": "sum_score",
# # #                 "sort_by": "rank:asc",
# # #                 "highlight_full_fields": "*",
# # #                 "facet_by": "lotType, regionCode, countryCode, saleFormat, noReserve, isBoosted, productMake, vendorType, driveSide, listingStage, tags",
# # #                 "max_facet_values": 999,
# # #                 "facet_counts": True,
# # #                 "facet_stats": True,
# # #                 "facet_distribution": True,
# # #                 "facet_return_parent": True,
# # #                 "collection": "production_cars",
# # #                 "q": "*",
# # #                 "filter_by": "listingStage:=[`live`] && countryCode:=[`AU`] && regionCode:=[`APAC`]",
# # #                 "page": 1,
# # #                 "per_page": 50   # ← increased for faster scraping (max ~100 usually safe)
# # #             }
# # #         ]
# # #     }

# # #     page = 1
# # #     while True:
# # #         # Update page number in payload
# # #         base_payload["searches"][0]["page"] = page

# # #         try:
# # #             print(f"Fetching page {page}...")
# # #             response = requests.post(api_url, headers=headers, json=base_payload, timeout=15)

# # #             if response.status_code != 200:
# # #                 print(f"API error: HTTP {response.status_code}")
# # #                 break

# # #             data = response.json()

# # #             # Extract results from multi_search response
# # #             if "results" not in data or not data["results"]:
# # #                 print("No more results")
# # #                 break

# # #             result = data["results"][0]  # first (and only) search
# # #             hits = result.get("hits", [])

# # #             if not hits:
# # #                 print(f"Page {page}: No more auctions")
# # #                 break

# # #             print(f"Page {page}: Found {len(hits)} auctions\n")

# # #             for hit in hits:
# # #                 doc = hit.get("document", {})

# # #                 # Build clean car name
# # #                 title = doc.get('title', 'Unknown Car')
# # #                 year = str(doc.get('productYear', ''))
# # #                 make = doc.get('productMake') or doc.get('vehicleMake', '')
# # #                 model = doc.get('model', '')

# # #                 car_name = f"{year} {make} {model}".strip()
# # #                 if not car_name or car_name == year:
# # #                     car_name = title

# # #                 # Print as we scrape
# # #                 print(f"Scraped: {car_name}")

# # #                 lot = {
# # #                     'source': 'collectingcars',
# # #                     'status': 'live',
# # #                     'auction_id': doc.get('id'),
# # #                     'title': title,
# # #                     'year': year,
# # #                     'make': make,
# # #                     'model': model,
# # #                     'odometer': doc.get('odometer', '') or doc.get('mileage', ''),
# # #                     'price': doc.get('currentBid') or doc.get('buyNowPrice') or doc.get('estimate', 'TBA'),
# # #                     'auction_date': None,
# # #                     'location': doc.get('location', 'Australia'),
# # #                     'images': doc.get('images', []) or [doc.get('mainImage', '')],
# # #                     'url': f"https://collectingcars.com/for-sale/{doc.get('slug', '')}",
# # #                     'description': doc.get('description', ''),
# # #                     'reserve': 'No' if doc.get('noReserve', False) else 'Yes',
# # #                     'scrape_time': datetime.now(timezone.utc).isoformat()
# # #                 }

# # #                 # Try to parse auction end date
# # #                 for date_key in ['endDate', 'auctionEndDate', 'closingDate']:
# # #                     if doc.get(date_key):
# # #                         try:
# # #                             lot['auction_date'] = parse(doc[date_key]).isoformat()
# # #                             break
# # #                         except:
# # #                             pass

# # #                 # Fallback year/make/model from title
# # #                 if not lot['make'] or not lot['model']:
# # #                     m = re.search(r'(\d{4})\s*([a-zA-Z]+)\s*(.+?)(?:\s+|$)', lot['title'])
# # #                     if m:
# # #                         lot['year'] = m.group(1)
# # #                         lot['make'] = m.group(2).capitalize()
# # #                         lot['model'] = m.group(3).strip().capitalize()

# # #                 if is_classic(lot):
# # #                     listings.append(lot)

# # #             page += 1
# # #             time.sleep(1.2)  # polite delay

# # #         except Exception as e:
# # #             print(f"Page {page} error: {str(e)}")
# # #             break
# # #     print(listings)
# # #     print(f"\nCollecting Cars total collected: {len(listings)} classic cars\n")
# # #     return listings
# # # def scrape_carbids(base_url):
# # #     """
# # #     Modern scraping approach for carbids.com.au (as of early-mid 2025 style)
# # #     Tries two strategies:
# # #     1. Wait longer + scroll to trigger lazy loading / angular render
# # #     2. Intercept the most important API call (Search/Tags or similar)
# # #     """
# # #     listings = []
# # #     print("Starting CarBids scrape...")

# # #     # ── Strategy 1: Heavy browser simulation + waiting + scrolling ───────────────
# # #     try:
# # #         driver = get_driver()
# # #         driver.set_window_size(1400, 900)  # bigger window sometimes helps

# # #         # Build clean URL without fragment (angular often ignores it anyway)
# # #         clean_url = base_url.split('#')[0]
# # #         driver.get(clean_url)

# # #         # Give Angular plenty of time to initialize + make initial requests
# # #         try:
# # #             WebDriverWait(driver, 25).until(
# # #                 EC.presence_of_element_located((By.CSS_SELECTOR, "div.wrapper.col-lg-4"))
# # #             )
# # #         except:
# # #             print("Main wrapper not found after 25s → probably still loading via XHR")

# # #         # Aggressive scrolling to force lazy loading / infinite scroll simulation
# # #         last_height = driver.execute_script("return document.body.scrollHeight")
# # #         scroll_attempts = 0
# # #         max_scrolls = 12

# # #         while scroll_attempts < max_scrolls:
# # #             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# # #             time.sleep(1.8 + scroll_attempts * 0.3)  # progressive delay

# # #             new_height = driver.execute_script("return document.body.scrollHeight")
# # #             if new_height == last_height:
# # #                 scroll_attempts += 1
# # #             else:
# # #                 scroll_attempts = 0
# # #                 last_height = new_height

# # #         # Give final render chance
# # #         time.sleep(4)

# # #         soup = BeautifulSoup(driver.page_source, 'html.parser')
# # #         driver.quit()

# # #         lot_divs = soup.select('div.wrapper.col-lg-4.col-md-6.col-sm-6.mobile-margin')

# # #         print(f"Found {len(lot_divs)} lot wrappers after heavy scrolling")

# # #         if lot_divs:
# # #             for div in lot_divs:
# # #                 lot = {}

# # #                 # Title → year/make/model
# # #                 title_elem = div.select_one('h3.h5.p-b-10')
# # #                 title = title_elem.get_text(strip=True) if title_elem else ''
                
# # #                 # Very common pattern on carbids: "12/1969 Ford Mustang Mach 1"
# # #                 m = re.match(r'(\d{1,2}/\d{4})\s+([^/]+?)\s+(.+?)(?:\s*\([^)]+\))?$', title)
# # #                 if m:
# # #                     lot['year']   = m.group(1).strip()
# # #                     lot['make']   = m.group(2).strip()
# # #                     lot['model']  = m.group(3).strip()
# # #                 else:
# # #                     lot['year'] = ''
# # #                     lot['make'] = ''
# # #                     lot['model'] = title

# # #                 # Icons + values
# # #                 def get_next_text(icon_class):
# # #                     i = div.select_one(f'i.{icon_class.replace(" ", ".")}')
# # #                     if i:
# # #                         txt = i.next_sibling
# # #                         return txt.strip() if txt and isinstance(txt, str) else ''
# # #                     return ''

# # #                 lot['odometer']    = get_next_text('fas fa-tachometer-alt')
# # #                 lot['transmission'] = get_next_text('fas fa-cogs')
# # #                 lot['fuel_type']   = get_next_text('fas fa-gas-pump')
# # #                 lot['engine']      = get_next_text('fas fa-oil-can')

# # #                 # Price / status
# # #                 price_big = div.select_one('span.h2')
# # #                 if price_big:
# # #                     lot['price_range'] = price_big.get_text(strip=True)
# # #                 else:
# # #                     start_price = div.select_one('span.h4')
# # #                     lot['price_range'] = start_price.get_text(strip=True) if start_price else 'Auction TBA'

# # #                 # Countdown & calendar date
# # #                 countdown = div.select_one('span[id^="closingCountdownTextGrid"]')
# # #                 calendar_span = div.select_one('span[id^="closingTimeGrid"]')

# # #                 lot['closing_text'] = countdown.get_text(strip=True) if countdown else ''
                
# # #                 calendar_text = ''
# # #                 if calendar_span:
# # #                     txt = calendar_span.get_text(strip=True)
# # #                     calendar_text = txt.strip('()[] ')
                
# # #                 try:
# # #                     lot['auction_date'] = parse(calendar_text) if calendar_text else None
# # #                 except:
# # #                     lot['auction_date'] = None

# # #                 # Location
# # #                 loc_div = div.select_one('div.bgm-white.p-5.m-r-5.p-l-15.p-r-15')
# # #                 city = loc_div.get_text(strip=True) if loc_div else ''
                
# # #                 state_span = div.select_one('span.p-5[style*="float: right"]')
# # #                 state = state_span.get_text(strip=True) if state_span else ''
                
# # #                 lot['location'] = f"{city} {state}".strip()

# # #                 # Ref number
# # #                 ref = div.select_one('mark.h5.p-t-5.p-b-5.p-r-10.p-l-10')
# # #                 lot['reference_number'] = ref.get_text(strip=True) if ref else ''

# # #                 # Images — try both ng-src and src
# # #                 imgs = div.select('img.img-responsive')
# # #                 lot['images'] = []
# # #                 for img in imgs:
# # #                     src = img.get('ng-src') or img.get('src') or ''
# # #                     if src:
# # #                         if src.startswith('//'): src = 'https:' + src
# # #                         lot['images'].append(src)

# # #                 # Detail link
# # #                 a = div.select_one('a[ng-href]')
# # #                 lot['url'] = a['ng-href'] if a else clean_url

# # #                 # Quick description
# # #                 lot['description'] = ' '.join(filter(None, [
# # #                     lot.get('odometer'),
# # #                     lot.get('transmission'),
# # #                     lot.get('fuel_type'),
# # #                     lot.get('engine')
# # #                 ]))

# # #                 lot['reserve'] = 'Yes'  # most are reserve
# # #                 lot['body_style'] = extract_body_style(lot['description'])
# # #                 lot['scrape_time'] = datetime.utcnow()
# # #                 lot['source'] = 'carbids'

# # #                 if is_classic(lot):
# # #                     listings.append(lot)

# # #             print(f"→ Successfully parsed {len(listings)} cars with browser method")
# # #             print(listings)
# # #             if listings:
# # #                 return listings  # ← early return if we got something good

# # #     except Exception as e:
# # #         print("Browser heavy scraping failed:", str(e))

# # #     # ── Strategy 2: Try to hit the API directly (most reliable long-term) ───────
# # #     print("Falling back to API attempt...")

# # #     try:
# # #         s = requests.Session()
# # #         s.headers.update({
# # #             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
# # #                          '(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
# # #             'Accept': 'application/json, text/plain, */*',
# # #             'X-Requested-With': 'XMLHttpRequest',
# # #         })

# # #         # Very often needed — get anti-forgery token first
# # #         r = s.get(clean_url)
# # #         soup_init = BeautifulSoup(r.text, 'html.parser')
# # #         token_input = soup_init.find('input', {'name': '__RequestVerificationToken'})
# # #         if token_input and token_input.get('value'):
# # #             s.headers['__RequestVerificationToken'] = token_input['value']

# # #         page = 0
# # #         while True:
# # #             payload = {
# # #                 "top": 96,
# # #                 "skip": page * 96,
# # #                 "sort": {"aucClose": "asc"},
# # #                 "tagName": "Unique and Classic Car Auctions",
# # #                 "filter": {
# # #                     "Display": True,
# # #                     # You can add more filters later if needed
# # #                 }
# # #             }

# # #             try:
# # #                 resp = s.post(
# # #                     "https://carbids.com.au/Search/Tags",
# # #                     json=payload,
# # #                     timeout=20
# # #                 )

# # #                 if resp.status_code != 200:
# # #                     print(f"API returned {resp.status_code} → stopping")
# # #                     break

# # #                 data = resp.json()

# # #                 auctions = data.get('auctions', [])  # ← field name may change!
# # #                 if not auctions:
# # #                     print("No more auctions in API response")
# # #                     break

# # #                 print(f"API page {page+1} → got {len(auctions)} cars")

# # #                 for auc in auctions:
# # #                     lot = {
# # #                         'source': 'carbids',
# # #                         'url': auc.get('AucDetailsUrlLink', clean_url),
# # #                         'reference_number': auc.get('aucReferenceNo', ''),
# # #                         'year': str(auc.get('aucYear', '')),
# # #                         'make': auc.get('aucMake', ''),
# # #                         'model': auc.get('aucModel', ''),
# # #                         'odometer': auc.get('aucOdometer', ''),
# # #                         'transmission': auc.get('aucTransmission', ''),
# # #                         'fuel_type': auc.get('aucFuelType', ''),
# # #                         'engine': f"{auc.get('aucCapacity','')} {auc.get('aucCylinder','')} cyl",
# # #                         'price_range': auc.get('aucCurrentBid', 0) or 'Auction TBA',
# # #                         'location': f"{auc.get('aucCity','')} {auc.get('aucState','')}".strip(),
# # #                         'images': [auc.get('aucCarsThumbnailUrl')] + 
# # #                                  (auc.get('aucMediumThumbnailUrlList', []) or []),
# # #                         'closing_text': auc.get('closingCountdownText', ''),
# # #                         'auction_date': parse(auc['aucCloseUtc']) if auc.get('aucCloseUtc') else None,
# # #                         'description': auc.get('aucTitle', ''),
# # #                         'reserve': 'Yes',
# # #                         'scrape_time': datetime.utcnow(),
# # #                     }

# # #                     if is_classic(lot):
# # #                         listings.append(lot)

# # #                 page += 1
# # #                 time.sleep(1.4)  # polite delay

# # #             except Exception as inner_e:
# # #                 print("API call failed:", str(inner_e))
# # #                 break

# # #     except Exception as outer_e:
# # #         print("API fallback also failed:", str(outer_e))
# # #     print(listings)
# # #     print(f"Final count from CarBids: {len(listings)} cars")
# # #     return listings
# # # def scrape_bennetts(base_url):
# # #     pages = [base_url, base_url + '/off-site.php']  # Scrape main and off-site
# # #     all_listings = []
# # #     for page_url in pages:
# # #         try:
# # #             driver = get_driver()
# # #             driver.get(page_url)
# # #             soup = BeautifulSoup(driver.page_source, 'html.parser')
# # #             driver.quit()

# # #             # Parse auction date from h3 in sitename
# # #             sitename = soup.find('div', id='sitename')
# # #             h3 = sitename.find('h3') if sitename else None
# # #             auction_text = h3.text.strip() if h3 else ''
# # #             date_match = re.search(r'(\d{1,2}[ST|ND|RD|TH]{0,2} \w+ \d{4})', auction_text.upper())
# # #             time_match = re.search(r'@ (\d{1,2}[AP]M)', auction_text.upper())
# # #             auction_date_str = ''
# # #             if date_match:
# # #                 date_str = re.sub(r'([ST|ND|RD|TH])', '', date_match.group(1))
# # #                 auction_date_str += date_str
# # #             if time_match:
# # #                 auction_date_str += ' ' + time_match.group(1)
# # #             auction_date = None
# # #             try:
# # #                 auction_date = parse(auction_date_str)
# # #             except:
# # #                 pass

# # #             # Find all clear divs with column
# # #             sections = soup.find_all('div', class_='clear')
# # #             for section in sections:
# # #                 column = section.find('div', class_='column column-600 column-left')
# # #                 if column:
# # #                     h3_cat = column.find('h3')
# # #                     category = h3_cat.text.strip() if h3_cat else ''
# # #                     table = column.find('table')
# # #                     if table:
# # #                         tbody = table.find('tbody')
# # #                         trs = tbody.find_all('tr') if tbody else table.find_all('tr')
# # #                         for tr in trs[1:]:  # Skip header
# # #                             tds = tr.find_all('td')
# # #                             if len(tds) == 7:
# # #                                 photo_td = tds[0]
# # #                                 a = photo_td.find('a')
# # #                                 detail_url = base_url + '/' + a['href'].lstrip('/') if a else ''
# # #                                 img = photo_td.find('img')
# # #                                 image_src = base_url + '/' + img['src'].lstrip('/') if img and img['src'].startswith('images') else img['src']
# # #                                 make = tds[1].text.strip()
# # #                                 stock_model = tds[2].text.strip()
# # #                                 parts = stock_model.split('/')
# # #                                 stock_ref = parts[0].strip() if parts else ''
# # #                                 model = parts[1].strip() if len(parts) > 1 else stock_model
# # #                                 year = tds[3].text.strip()
# # #                                 options = tds[4].text.strip()
# # #                                 location_td = tds[5]
# # #                                 location = location_td.text.strip().replace('\n', '').replace('br /', '')
# # #                                 lot = {
# # #                                     'source': page_url,
# # #                                     'make': make,
# # #                                     'model': model,
# # #                                     'year': year,
# # #                                     'price_range': None,  # No price in list
# # #                                     'auction_date': auction_date,
# # #                                     'location': location,
# # #                                     'images': [image_src] if image_src else [],
# # #                                     'url': detail_url,
# # #                                     'description': options,  # Use options as desc for now; scrape detail for full
# # #                                     'reserve': 'Yes',  # Assume
# # #                                     'body_style': extract_body_style(options),
# # #                                     'transmission': extract_transmission(options),
# # #                                     'scrape_time': datetime.now()
# # #                                 }
# # #                                 if is_classic(lot):
# # #                                     all_listings.append(lot)
# # #         except Exception as e:
# # #             print(f"Error scraping Bennetts page {page_url}: {e}")
# # #     print(f"Scraped {len(all_listings)} listings from Bennetts")
# # #     return all_listings

# # # def scrape_burnsandco(base_url):
# # #     pages = [base_url + '/current-auctions/', base_url + '/upcoming-auctions/']
# # #     all_listings = []
# # #     for page_url in pages:
# # #         try:
# # #             driver = get_driver()
# # #             driver.get(page_url)
# # #             soup = BeautifulSoup(driver.page_source, 'html.parser')
# # #             driver.quit()

# # #             articles = soup.find_all('article', class_='regular masonry-blog-item')
# # #             for article in articles:
# # #                 img_link = article.find('a', class_='img-link')
# # #                 detail_url = img_link['href'] if img_link else ''
# # #                 img = img_link.find('img') if img_link else None
# # #                 image_src = img['src'] if img else ''
# # #                 meta_category = article.find('span', class_='meta-category')
# # #                 category = meta_category.text.strip() if meta_category else ''
# # #                 date_item = article.find('span', class_='date-item')
# # #                 auction_date_str = date_item.text.strip() if date_item else ''
# # #                 auction_date = None
# # #                 try:
# # #                     auction_date = parse(auction_date_str)
# # #                 except:
# # #                     pass
# # #                 title_a = article.find('h3', class_='title').find('a') if article.find('h3', class_='title') else None
# # #                 title = title_a.text.strip() if title_a else ''
# # #                 excerpt = article.find('div', class_='excerpt').text.strip() if article.find('div', class_='excerpt') else ''
# # #                 place = article.find('p', class_='place').text.strip() if article.find('p', class_='place') else ''
# # #                 bid_links = article.find_all('p', class_='registration_bidding_link')
# # #                 for bid_p in bid_links:
# # #                     bid_a = bid_p.find('a')
# # #                     bid_url = bid_a['href'] if bid_a else ''
# # #                     # Now scrape lots from bid_url
# # #                     catalogue_lots = scrape_catalogue(bid_url)
# # #                     for cat_lot in catalogue_lots:
# # #                         cat_lot['auction_date'] = auction_date or cat_lot.get('auction_date')
# # #                         cat_lot['location'] = place or cat_lot.get('location')
# # #                         cat_lot['source'] = bid_url
# # #                         all_listings.append(cat_lot)
# # #         except Exception as e:
# # #             print(f"Error scraping Burns page {page_url}: {e}")
# # #     print(f"Scraped {len(all_listings)} listings from Burns & Co")
# # #     return all_listings

# # # def scrape_catalogue(catalogue_url):
# # #     listings = []
# # #     try:
# # #         driver = get_driver()
# # #         driver.get(catalogue_url)
# # #         soup = BeautifulSoup(driver.page_source, 'html.parser')
# # #         driver.quit()

# # #         # Adjust based on actual catalogue structure
# # #         # Assuming lots are in divs with class 'lot-item' or similar; inspect site
# # #         lot_items = soup.find_all('div', class_='lot-item')  # Placeholder class
# # #         for item in lot_items:
# # #             lot_number = item.find('span', class_='lot-number').text.strip() if item.find('span', class_='lot-number') else ''
# # #             desc = item.find('div', class_='lot-description').text.strip() if item.find('div', class_='lot-description') else ''
# # #             # Parse desc for make, model, year
# # #             match = re.match(r'(\d{4})? ?(.*?) (.*)', desc)
# # #             year = match.group(1) if match and match.group(1) else ''
# # #             make = match.group(2) if match else ''
# # #             model = match.group(3) if match else desc
# # #             images = [img['src'] for img in item.find_all('img')]
# # #             detail_a = item.find('a', class_='lot-detail')
# # #             detail_url = catalogue_url + detail_a['href'] if detail_a else ''
# # #             current_bid = item.find('span', class_='current-bid').text.strip() if item.find('span', class_='current-bid') else ''
# # #             lot = {
# # #                 'lot_number': lot_number,
# # #                 'make': make,
# # #                 'model': model,
# # #                 'year': year,
# # #                 'price_range': current_bid,  # Use current bid as estimate
# # #                 'auction_date': None,  # Parse from page if needed
# # #                 'location': None,
# # #                 'images': images,
# # #                 'url': detail_url,
# # #                 'description': desc,
# # #                 'reserve': 'Yes',
# # #                 'body_style': extract_body_style(desc),
# # #                 'transmission': extract_transmission(desc),
# # #                 'scrape_time': datetime.now()
# # #             }
# # #             if is_classic(lot):
# # #                 listings.append(lot)
# # #     except Exception as e:
# # #         print(f"Error scraping catalogue {catalogue_url}: {e}")
# # #     return listings

# # # def parse_lot(item, url):
# # #     # Generic parse_lot remains for other sites
# # #     try:
# # #         description = item.find('p', class_='desc') or item.find('div', class_='description')  # Adjust
# # #         description_text = description.text.strip() if description else ''
# # #         year_elem = item.find('span', class_='year') or item.find('h3')  # Adjust
# # #         year_str = year_elem.text.strip() if year_elem else '0'
# # #         make_elem = item.find('span', class_='make') or item.find('h2')
# # #         model_elem = item.find('span', class_='model')
# # #         price_elem = item.find('span', class_='estimate') or item.find('div', class_='price')
# # #         date_elem = item.find('span', class_='date')
# # #         location_elem = item.find('span', class_='location')
# # #         link_elem = item.find('a', class_='lot-link') or item.find('a')

# # #         lot = {
# # #             'make': make_elem.text.strip() if make_elem else None,
# # #             'model': model_elem.text.strip() if model_elem else None,
# # #             'year': year_str,
# # #             'price_range': price_elem.text.strip() if price_elem else None,
# # #             'auction_date': parse_date(date_elem.text.strip()) if date_elem else None,
# # #             'location': location_elem.text.strip() if location_elem else 'Online',
# # #             'images': [img['src'] for img in item.find_all('img', class_='thumbnail')][:6],
# # #             'url': link_elem['href'] if link_elem else url,
# # #             'description': description_text,
# # #             'reserve': 'No' if 'no reserve' in description_text.lower() else 'Yes',
# # #             'body_style': extract_body_style(description_text),
# # #             'transmission': extract_transmission(description_text),
# # #             'scrape_time': datetime.now()
# # #         }
# # #         return lot
# # #     except:
# # #         return None

# # # def parse_date(date_str):
# # #     try:
# # #         return parse(date_str)
# # #     except:
# # #         return None

# # # def extract_body_style(desc):
# # #     lower_desc = desc.lower()
# # #     styles = ['coupe', 'convertible', 'sedan', 'wagon', 'ute', 'truck']
# # #     for style in styles:
# # #         if style in lower_desc:
# # #             return style
# # #     return None

# # # def extract_transmission(desc):
# # #     lower_desc = desc.lower()
# # #     if 'manual' in lower_desc:
# # #         return 'manual'
# # #     if 'auto' in lower_desc or 'automatic' in lower_desc:
# # #         return 'auto'
# # #     return None

# # # def is_classic(lot):
# # #     try:
# # #         year = int(lot['year'])
# # #     except:
# # #         year = 0
# # #     desc = lot['description'].lower() if lot['description'] else ''
# # #     return year < 1990 or any(word in desc for word in ['collector', 'classic', 'future classic', 'modern classic'])

# # # def scrape_all():
# # #     all_lots = []
# # #     for source in SOURCES:
# # #         lots = scrape_site(source)
# # #         all_lots.extend(lots)
    
# # #     for lot in all_lots:
# # #         if lot['auction_date']:
# # #             lots_collection.update_one({'url': lot['url']}, {'$set': lot}, upsert=True)
    
# # #     now = datetime.now()
# # #     ended = lots_collection.find({'auction_date': {'$lt': now}})
# # #     for end in ended:
# # #         sold_collection.insert_one(end)
# # #         lots_collection.delete_one({'_id': end['_id']})
    
# # #     two_years_ago = now - timedelta(days=730)
# # #     sold_collection.delete_many({'auction_date': {'$lt': two_years_ago}})

# # # # Scheduler
# # # scheduler = BackgroundScheduler()
# # # scheduler.add_job(scrape_all, 'interval', hours=4)
# # # scheduler.start()

# # # @app.route('/api/scrape', methods=['POST'])
# # # @swag_from({
# # #     'tags': ['Admin'],
# # #     'summary': 'Trigger manual scrape',
# # #     'security': [{'Bearer': []}],
# # #     'responses': {
# # #         '200': {'description': 'Scraping completed'}
# # #     }
# # # })
# # # @jwt_required()
# # # def manual_scrape():
# # #     scrape_all()
# # #     return jsonify({'message': 'Scraping completed'})

# # # @app.route('/api/register', methods=['POST'])
# # # @swag_from({
# # #     'tags': ['Users'],
# # #     'summary': 'Register a new user',
# # #     'parameters': [
# # #         {
# # #             'name': 'body',
# # #             'in': 'body',
# # #             'required': True,
# # #             'schema': {
# # #                 'type': 'object',
# # #                 'properties': {
# # #                     'email': {'type': 'string'},
# # #                     'password': {'type': 'string'}
# # #                 },
# # #                 'required': ['email', 'password']
# # #             }
# # #         }
# # #     ],
# # #     'responses': {
# # #         '200': {'description': 'User registered'},
# # #         '400': {'description': 'User already exists'}
# # #     }
# # # })
# # # def register():
# # #     data = request.json
# # #     email = data['email']
# # #     password = data['password']  # Hash in production using bcrypt
# # #     if users_collection.find_one({'email': email}):
# # #         return jsonify({'error': 'User exists'}), 400
# # #     user_id = users_collection.insert_one({'email': email, 'password': password}).inserted_id
# # #     user = User(str(user_id), email)
# # #     login_user(user)
# # #     return jsonify({'message': 'Registered'})

# # # @app.route('/api/login', methods=['POST'])
# # # @swag_from({
# # #     'tags': ['Users'],
# # #     'summary': 'Login user',
# # #     'parameters': [
# # #         {
# # #             'name': 'body',
# # #             'in': 'body',
# # #             'required': True,
# # #             'schema': {
# # #                 'type': 'object',
# # #                 'properties': {
# # #                     'email': {'type': 'string'},
# # #                     'password': {'type': 'string'}
# # #                 },
# # #                 'required': ['email', 'password']
# # #             }
# # #         }
# # #     ],
# # #     'responses': {
# # #         '200': {'description': 'Login successful, token returned'},
# # #         '401': {'description': 'Invalid credentials'}
# # #     }
# # # })
# # # def login():
# # #     data = request.json
# # #     email = data['email']
# # #     password = data['password']
# # #     user_doc = users_collection.find_one({'email': email, 'password': password})
# # #     if user_doc:
# # #         user = User(str(user_doc['_id']), email)
# # #         login_user(user)
# # #         access_token = create_access_token(identity=str(user_doc['_id']))
# # #         return jsonify({'token': access_token})
# # #     return jsonify({'error': 'Invalid credentials'}), 401

# # # @app.route('/api/logout')
# # # @swag_from({
# # #     'tags': ['Users'],
# # #     'summary': 'Logout user',
# # #     'responses': {
# # #         '200': {'description': 'Logged out'}
# # #     }
# # # })
# # # @login_required
# # # def logout():
# # #     logout_user()
# # #     return jsonify({'message': 'Logged out'})

# # # @app.route('/api/calendar', methods=['GET'])
# # # @swag_from({
# # #     'tags': ['Auctions'],
# # #     'summary': 'Get auction calendar',
# # #     'parameters': [
# # #         {'name': 'state', 'in': 'query', 'type': 'string', 'description': 'Filter by state'},
# # #         {'name': 'month', 'in': 'query', 'type': 'string', 'description': 'Filter by month (YYYY-MM)'},
# # #         {'name': 'auction_house', 'in': 'query', 'type': 'string', 'description': 'Filter by auction house'},
# # #         {'name': 'online_only', 'in': 'query', 'type': 'boolean', 'description': 'Filter online only'}
# # #     ],
# # #     'responses': {
# # #         '200': {'description': 'List of upcoming auctions'}
# # #     }
# # # })
# # # def calendar():
# # #     state = request.args.get('state')
# # #     month = request.args.get('month')
# # #     auction_house = request.args.get('auction_house')
# # #     online_only = request.args.get('online_only') == 'true'
    
# # #     query = {}
# # #     if state:
# # #         query['location'] = {'$regex': state, '$options': 'i'}
# # #     if month:
# # #         try:
# # #             start = datetime.strptime(month + '-01', '%Y-%m-%d')
# # #             end = start + timedelta(days=31)
# # #             query['auction_date'] = {'$gte': start, '$lt': end}
# # #         except:
# # #             pass
# # #     if auction_house:
# # #         query['source'] = {'$regex': auction_house, '$options': 'i'}
# # #     if online_only:
# # #         query['location'] = 'Online'
    
# # #     now = datetime.now()
# # #     upcoming = lots_collection.find({
# # #         **query,
# # #         'auction_date': {'$gte': now, '$lt': now + timedelta(days=90)}
# # #     }).sort('auction_date', 1)
    
# # #     return jsonify([dict(lot, **{'_id': str(lot['_id'])}) for lot in upcoming])

# # # @app.route('/api/search', methods=['GET'])
# # # @swag_from({
# # #     'tags': ['Auctions'],
# # #     'summary': 'Search for lots',
# # #     'parameters': [
# # #         {'name': 'make', 'in': 'query', 'type': 'string'},
# # #         {'name': 'model', 'in': 'query', 'type': 'string'},
# # #         {'name': 'variant', 'in': 'query', 'type': 'string'},
# # #         {'name': 'year_min', 'in': 'query', 'type': 'integer'},
# # #         {'name': 'year_max', 'in': 'query', 'type': 'integer'},
# # #         {'name': 'price_min', 'in': 'query', 'type': 'integer'},
# # #         {'name': 'price_max', 'in': 'query', 'type': 'integer'},
# # #         {'name': 'state', 'in': 'query', 'type': 'string'},
# # #         {'name': 'auction_house', 'in': 'query', 'type': 'string'},
# # #         {'name': 'no_reserve', 'in': 'query', 'type': 'boolean'},
# # #         {'name': 'body_style', 'in': 'query', 'type': 'string'},
# # #         {'name': 'transmission', 'in': 'query', 'type': 'string'},
# # #         {'name': 'newly_added', 'in': 'query', 'type': 'string', 'description': 'e.g., 24h'},
# # #         {'name': 'sort', 'in': 'query', 'type': 'string', 'description': 'e.g., auction_date asc'}
# # #     ],
# # #     'responses': {
# # #         '200': {'description': 'Search results'}
# # #     }
# # # })
# # # def search():
# # #     make = request.args.get('make')
# # #     model = request.args.get('model')
# # #     variant = request.args.get('variant')
# # #     year_min = request.args.get('year_min')
# # #     year_max = request.args.get('year_max')
# # #     price_min = request.args.get('price_min')
# # #     price_max = request.args.get('price_max')
# # #     state = request.args.get('state')
# # #     auction_house = request.args.get('auction_house')
# # #     no_reserve = request.args.get('no_reserve') == 'true'
# # #     body_style = request.args.get('body_style')
# # #     transmission = request.args.get('transmission')
# # #     newly_added = request.args.get('newly_added')
    
# # #     query = {}
# # #     if make:
# # #         query['make'] = {'$regex': make, '$options': 'i'}
# # #     if model:
# # #         query['model'] = {'$regex': model, '$options': 'i'}
# # #     if variant:
# # #         query['variant'] = {'$regex': variant, '$options': 'i'}
# # #     if year_min or year_max:
# # #         query['year'] = {}
# # #         if year_min:
# # #             query['year']['$gte'] = year_min
# # #         if year_max:
# # #             query['year']['$lte'] = year_max
# # #     if price_min or price_max:
# # #         # Assuming price_range is {'low': int, 'high': int}; parse in scrape if string
# # #         if price_min:
# # #             query['price_range.low'] = {'$gte': int(price_min)}
# # #         if price_max:
# # #             query['price_range.high'] = {'$lte': int(price_max)}
# # #     if state:
# # #         query['location'] = {'$regex': state, '$options': 'i'}
# # #     if auction_house:
# # #         query['source'] = {'$regex': auction_house, '$options': 'i'}
# # #     if no_reserve:
# # #         query['reserve'] = 'No'
# # #     if body_style:
# # #         query['body_style'] = {'$regex': body_style, '$options': 'i'}
# # #     if transmission:
# # #         query['transmission'] = {'$regex': transmission, '$options': 'i'}
# # #     if newly_added:
# # #         try:
# # #             hours = int(newly_added[:-1])
# # #             time_ago = datetime.now() - timedelta(hours=hours)
# # #             query['scrape_time'] = {'$gte': time_ago}
# # #         except:
# # #             pass
    
# # #     sort = request.args.get('sort', 'auction_date asc').split(' ')
# # #     sort_field = sort[0]
# # #     sort_dir = 1 if len(sort) > 1 and sort[1] == 'asc' else -1
    
# # #     results = lots_collection.find(query).sort(sort_field, sort_dir)
# # #     return jsonify([dict(result, **{'_id': str(result['_id'])}) for result in results])

# # # @app.route('/api/lot/<lot_id>', methods=['GET'])
# # # @swag_from({
# # #     'tags': ['Auctions'],
# # #     'summary': 'Get individual lot details',
# # #     'parameters': [
# # #         {'name': 'lot_id', 'in': 'path', 'type': 'string', 'required': True}
# # #     ],
# # #     'responses': {
# # #         '200': {'description': 'Lot details'},
# # #         '404': {'description': 'Not found'}
# # #     }
# # # })
# # # def get_lot(lot_id):
# # #     lot = lots_collection.find_one({'_id': ObjectId(lot_id)})
# # #     if not lot:
# # #         return jsonify({'error': 'Not found'}), 404
# # #     lot['_id'] = str(lot['_id'])
# # #     related = sold_collection.find({
# # #         'make': lot['make'],
# # #         'model': lot['model'],
# # #         'year': lot['year']
# # #     }).limit(5)
# # #     lot['related'] = [dict(rel, **{'_id': str(rel['_id'])}) for rel in related]
# # #     return jsonify(lot)

# # # @app.route('/api/watchlist', methods=['GET', 'POST'])
# # # @swag_from({
# # #     'tags': ['Users'],
# # #     'summary': 'Manage watchlist',
# # #     'security': [{'Bearer': []}],
# # #     'parameters': [
# # #         {
# # #             'name': 'body',
# # #             'in': 'body',
# # #             'required': False,
# # #             'schema': {
# # #                 'type': 'object',
# # #                 'properties': {
# # #                     'lot_id': {'type': 'string'}
# # #                 }
# # #             }
# # #         }
# # #     ],
# # #     'responses': {
# # #         '200': {'description': 'Watchlist or added message'}
# # #     }
# # # })
# # # @jwt_required()
# # # def watchlist():
# # #     user_id = get_jwt_identity()
# # #     if request.method == 'POST':
# # #         lot_id = request.json.get('lot_id')
# # #         watchlists_collection.update_one(
# # #             {'user_id': user_id},
# # #             {'$addToSet': {'lots': ObjectId(lot_id)}},
# # #             upsert=True
# # #         )
# # #         return jsonify({'message': 'Added'})
    
# # #     watch = watchlists_collection.find_one({'user_id': user_id})
# # #     if watch:
# # #         lots = lots_collection.find({'_id': {'$in': watch['lots']}})
# # #         return jsonify([dict(lot, **{'_id': str(lot['_id'])}) for lot in lots])
# # #     return jsonify([])

# # # @app.route('/api/saved_searches', methods=['GET', 'POST'])
# # # @swag_from({
# # #     'tags': ['Users'],
# # #     'summary': 'Manage saved searches',
# # #     'security': [{'Bearer': []}],
# # #     'responses': {
# # #         '200': {'description': 'Saved searches or saved message'}
# # #     }
# # # })
# # # @jwt_required()
# # # def saved_searches():
# # #     user_id = get_jwt_identity()
# # #     if request.method == 'POST':
# # #         search_params = request.json
# # #         saved_searches_collection.insert_one({'user_id': user_id, **search_params})
# # #         return jsonify({'message': 'Saved'})
    
# # #     searches = saved_searches_collection.find({'user_id': user_id})
# # #     return jsonify([dict(s, **{'_id': str(s['_id'])}) for s in searches])

# # # def send_alert(user_id, message):
# # #     user = users_collection.find_one({'_id': ObjectId(user_id)})
# # #     if user:
# # #         smtp_server = os.getenv('SMTP_SERVER')
# # #         smtp_port = int(os.getenv('SMTP_PORT', 587))
# # #         sender = os.getenv('SENDER_EMAIL')
# # #         password = os.getenv('SENDER_PASSWORD')
        
# # #         msg = MIMEText(message)
# # #         msg['Subject'] = 'Auction Alert'
# # #         msg['From'] = sender
# # #         msg['To'] = user['email']
        
# # #         with smtplib.SMTP(smtp_server, smtp_port) as server:
# # #             server.starttls()
# # #             server.login(sender, password)
# # #             server.sendmail(sender, user['email'], msg.as_string())

# # # @app.route('/api/sold', methods=['GET'])
# # # @swag_from({
# # #     'tags': ['Auctions'],
# # #     'summary': 'Get sold prices archive',
# # #     'parameters': [
# # #         {'name': 'make', 'in': 'query', 'type': 'string'},
# # #         {'name': 'model', 'in': 'query', 'type': 'string'},
# # #         {'name': 'year', 'in': 'query', 'type': 'integer'}
# # #     ],
# # #     'responses': {
# # #         '200': {'description': 'Sold lots'}
# # #     }
# # # })
# # # def sold():
# # #     make = request.args.get('make')
# # #     model = request.args.get('model')
# # #     year = request.args.get('year')
    
# # #     query = {}
# # #     if make:
# # #         query['make'] = {'$regex': make, '$options': 'i'}
# # #     if model:
# # #         query['model'] = {'$regex': model, '$options': 'i'}
# # #     if year:
# # #         query['year'] = year
    
# # #     results = sold_collection.find(query).sort('auction_date', -1)
# # #     return jsonify([dict(r, **{'_id': str(r['_id'])}) for r in results])

# # # @app.route('/api/market_pulse', methods=['GET'])
# # # @swag_from({
# # #     'tags': ['Auctions'],
# # #     'summary': 'Get market pulse data',
# # #     'responses': {
# # #         '200': {'description': 'Top sales and risers'}
# # #     }
# # # })
# # # def market_pulse():
# # #     now = datetime.now()
# # #     month_start = now - timedelta(days=30)
# # #     top_sales = sold_collection.find({'auction_date': {'$gte': month_start}}).sort('total_price', -1).limit(10)
# # #     top_sales_list = [dict(s, **{'_id': str(s['_id'])}) for s in top_sales]
    
# # #     pipeline = [
# # #         {'$match': {'auction_date': {'$gte': month_start}}},
# # #         {'$group': {'_id': {'make': '$make', 'model': '$model'}, 'avg_price': {'$avg': '$total_price'}, 'count': {'$sum': 1}}},
# # #         {'$sort': {'avg_price': -1}},
# # #         {'$limit': 10}
# # #     ]
# # #     risers = list(sold_collection.aggregate(pipeline))
# # #     return jsonify({'top_sales': top_sales_list, 'risers': risers})

# # # @app.route('/api/on_the_block', methods=['GET'])
# # # @swag_from({
# # #     'tags': ['Auctions'],
# # #     'summary': 'Get lots closing soon',
# # #     'responses': {
# # #         '200': {'description': 'Live lots'}
# # #     }
# # # })
# # # def on_the_block():
# # #     now = datetime.now()
# # #     two_hours = now + timedelta(hours=2)
# # #     live = lots_collection.find({'auction_date': {'$gte': now, '$lt': two_hours}})
# # #     return jsonify([dict(l, **{'_id': str(l['_id'])}) for l in live])

# # # @app.route('/api/auction_houses', methods=['GET'])
# # # @swag_from({
# # #     'tags': ['Auctions'],
# # #     'summary': 'Get auction houses directory',
# # #     'responses': {
# # #         '200': {'description': 'List of auction houses'}
# # #     }
# # # })
# # # def auction_houses():
# # #     houses = set(lot.get('source') for lot in lots_collection.find({}, {'source': 1}))
# # #     directory = []
# # #     for house in houses:
# # #         upcoming = lots_collection.count_documents({'source': house, 'auction_date': {'$gt': datetime.now()}})
# # #         name = house.split('//')[-1].split('.')[0] if house else 'Unknown'
# # #         directory.append({
# # #             'name': name,
# # #             'upcoming': upcoming,
# # #             'buyers_premium': 'Unknown'  # Add scraping if available
# # #         })
# # #     return jsonify(directory)

# # # # Initial scrape
# # # scrape_all()

# # # if __name__ == '__main__':
# # #     app.run(debug=True)
# # import os
# # import datetime
# # from datetime import timedelta
# # import requests
# # from bs4 import BeautifulSoup
# # from flask import Flask, request, jsonify, session
# # from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# # from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# # from flask_cors import CORS
# # from pymongo import MongoClient
# # from apscheduler.schedulers.background import BackgroundScheduler
# # import smtplib
# # from email.mime.text import MIMEText
# # from dotenv import load_dotenv
# # from flasgger import Swagger, swag_from
# # from selenium import webdriver
# # from selenium.webdriver.chrome.options import Options
# # from selenium.webdriver.chrome.service import Service
# # from webdriver_manager.chrome import ChromeDriverManager
# # from selenium.webdriver.common.by import By
# # from selenium.webdriver.support.ui import WebDriverWait
# # from selenium.webdriver.support import expected_conditions as EC
# # from dateutil.parser import parse
# # from datetime import datetime, timezone
# # from bson.objectid import ObjectId
# # import re
# # import time
# # import uuid

# # load_dotenv()

# # app = Flask(__name__)
# # app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')
# # CORS(app)

# # # JWT Setup
# # jwt = JWTManager(app)
# # app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret')

# # # Login Manager
# # login_manager = LoginManager()
# # login_manager.init_app(app)

# # # Swagger Setup
# # swagger = Swagger(app, template={
# #     "swagger": "2.0",
# #     "info": {
# #         "title": "AusClassicAuctions API",
# #         "description": "API for Australian Classic Car Auctions Aggregator",
# #         "version": "1.0.0"
# #     },
# #     "securityDefinitions": {
# #         "Bearer": {
# #             "type": "apiKey",
# #             "name": "Authorization",
# #             "in": "header",
# #             "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
# #         }
# #     }
# # })

# # # MongoDB Setup
# # client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/'))
# # db = client['ausclassicauctions']
# # lots_collection = db['lots']  # Current and upcoming lots
# # sold_collection = db['sold']  # Sold archive
# # users_collection = db['users']
# # watchlists_collection = db['watchlists']
# # saved_searches_collection = db['saved_searches']

# # # User Model
# # class User(UserMixin):
# #     def __init__(self, id, email):
# #         self.id = id
# #         self.email = email

# # @login_manager.user_loader
# # def load_user(user_id):
# #     user = users_collection.find_one({'_id': ObjectId(user_id)})
# #     if user:
# #         return User(user['_id'], user['email'])
# #     return None

# # # Scraping Sources
# # SOURCES = [
# #         {'url': 'https://www.tradinggarage.com', 'name': 'tradinggarage'},

# #     {'url': 'https://carbids.com.au/t/unique-and-classic-car-auctions#!?page=1&count=96&filter%5BDisplay%5D=true', 'name': 'carbids'},
# #     {'url': 'https://collectingcars.com/buy?refinementList%5BlistingStage%5D%5B0%5D=live&refinementList%5BregionCode%5D%5B0%5D=APAC&refinementList%5BcountryCode%5D%5B0%5D=AU', 'name': 'collectingcars'},
# #     # {'url': 'https://burnsandcoauctions.com.au', 'name': 'burnsandco'},
# #     # {'url': 'https://www.lloydsonline.com.au/AuctionLots.aspx?smode=0&aid=65946', 'name': 'lloydsonline'},
# #     # {'url': 'https://www.seven82motors.com.au', 'name': 'seven82motors'},
# #     # {'url': 'https://www.chicaneauctions.com.au', 'name': 'chicaneauctions'},
# #     # {'url': 'https://www.doningtonauctions.com.au', 'name': 'doningtonauctions'},
# #     {'url': 'https://www.bennettsclassicauctions.com.au', 'name': 'bennettsclassicauctions'}
# # ]

# # def get_driver():
# #     options = Options()
# #     options.headless = True
# #     service = Service(ChromeDriverManager().install())
# #     return webdriver.Chrome(service=service, options=options)

# # def scrape_site(source):
# #     url = source['url']
# #     name = source['name']
# #     if name == 'bennettsclassicauctions':
# #         return scrape_bennetts(url)
# #     elif name == 'burnsandco':
# #         return scrape_burnsandco(url)
# #     elif name == 'carbids':
# #         return scrape_carbids(url)
# #     elif name == 'tradinggarage':
# #         return scrape_tradinggarage(url)    
# #     elif name == 'collectingcars':
# #         return scrape_collectingcars()
# #     else:
# #         # Generic scraper for other sites (placeholder)
# #         try:
# #             driver = get_driver()
# #             driver.get(url)
# #             soup = BeautifulSoup(driver.page_source, 'html.parser')
# #             driver.quit()

# #             listings = []
# #             item_class = 'auction-item'  # Generic; adjust per site
# #             for item in soup.find_all('div', class_=item_class):
# #                 lot = parse_lot(item, url)
# #                 if lot and is_classic(lot):
# #                     lot['source'] = url
# #                     listings.append(lot)
# #             return listings
# #         except Exception as e:
# #             print(f"Error scraping {url}: {e}")
# #             return []

# # def scrape_tradinggarage(base_url="https://www.tradinggarage.com"):
# #     """
# #     Simple Trading Garage scraper using public APIs.
# #     Prints the name/title of each car as it scrapes.
# #     (No pagination needed - returns all auctions at once)
# #     """
# #     listings = []
# #     print("Starting Trading Garage API scrape...\n")

# #     session = requests.Session()
# #     session.headers.update({
# #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
# #                      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
# #         'Accept': 'application/json',
# #         'Referer': 'https://www.tradinggarage.com/',
# #     })

# #     # Two main endpoints (all cars returned in one call each)
# #     endpoints = {
# #         'live': 'https://portal.tradinggarage.com/api/v1/auctions?status=live',
# #         'coming_soon': 'https://portal.tradinggarage.com/api/v1/auctions?status=coming_soon'
# #     }

# #     for status, api_url in endpoints.items():
# #         try:
# #             print(f"Fetching {status.upper()} auctions...")
# #             r = session.get(api_url, timeout=12)

# #             if r.status_code != 200:
# #                 print(f"→ {status.upper()} failed (HTTP {r.status_code})\n")
# #                 continue

# #             data = r.json()

# #             auctions = (
# #                 data.get('data', []) or
# #                 data.get('auctions', []) or
# #                 data.get('items', []) or
# #                 data.get('results', []) or []
# #             )

# #             if not auctions:
# #                 print(f"→ {status.upper()}: No auctions found\n")
# #                 continue

# #             print(f"→ {status.upper()}: Found {len(auctions)} auctions\n")

# #             for auction in auctions:
# #                 # Build basic car name/title
# #                 title = auction.get('title') or auction.get('name', 'Unknown Car')
# #                 year = str(auction.get('year', ''))
# #                 make = auction.get('make', '')
# #                 model = auction.get('model', '')

# #                 # Clean and pretty name
# #                 car_name = f"{year} {make} {model}".strip()
# #                 if not car_name or car_name == year:
# #                     car_name = title

# #                 # Print the car name immediately
# #                 print(f"Scraped: {car_name}")

# #                 # Full lot data (same as before)
# #                 lot = {
# #                     'source': 'tradinggarage',
# #                     'status': status,
# #                     'auction_id': auction.get('id') or auction.get('auctionId'),
# #                     'title': title,
# #                     'year': year,
# #                     'make': make,
# #                     'model': model,
# #                     'odometer': auction.get('odometer') or auction.get('mileage', ''),
# #                     'price': (
# #                         auction.get('currentBid') or
# #                         auction.get('buyNowPrice') or
# #                         auction.get('estimate') or
# #                         auction.get('startingPrice') or
# #                         'TBA'
# #                     ),
# #                     'auction_date': None,
# #                     'location': auction.get('location', 'Online / Melbourne'),
# #                     'images': auction.get('images', []) or [auction.get('mainImage', '')],
# #                     'url': auction.get('url') or f"https://www.tradinggarage.com/auctions/{auction.get('slug') or auction.get('id') or ''}",
# #                     'description': auction.get('description', ''),
# #                     'reserve': auction.get('reserveStatus', 'Yes'),
# #                     'scrape_time': datetime.now(timezone.utc).isoformat()
# #                 }

# #                 # Try to get auction date
# #                 for date_key in ['endDate', 'closingDate', 'auctionDate', 'endsAt', 'startsAt']:
# #                     if auction.get(date_key):
# #                         try:
# #                             lot['auction_date'] = parse(auction[date_key]).isoformat()
# #                             break
# #                         except:
# #                             pass

# #                 # Fallback parsing from title if needed
# #                 if not lot['make'] or not lot['model']:
# #                     m = re.search(r'(\d{4})\s*([a-zA-Z]+)\s*(.+?)(?:\s+|$)', lot['title'])
# #                     if m:
# #                         lot['year'] = m.group(1)
# #                         lot['make'] = m.group(2).capitalize()
# #                         lot['model'] = m.group(3).strip().capitalize()

# #                 if is_classic(lot):
# #                     listings.append(lot)

# #             print("")  # empty line between statuses

# #         except Exception as e:
# #             print(f"→ {status.upper()} error: {str(e)}\n")

# #     print(f"Trading Garage total collected: {len(listings)} classic cars\n")
# #     print(listings)
# #     return listings

# # import requests
# # from datetime import datetime, timezone
# # from dateutil.parser import parse
# # import re
# # import time

# # def scrape_collectingcars():
# #     """
# #     Scraper for Collecting Cars (Australia/APAC live auctions)
# #     Uses the Typesense multi_search API (no Selenium needed)
# #     Prints each car's title as it's scraped.
# #     (Confirmed working January 2026)
# #     """
# #     listings = []
# #     print("Starting Collecting Cars API scrape...\n")

# #     api_url = "https://dora.production.collecting.com/multi_search"

# #     headers = {
# #         'x-typesense-api-key': 'aKIufK0SfYHMRp9mUBkZPR7pksehPBZq',
# #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
# #                      '(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
# #         'Accept': 'application/json',
# #         'Content-Type': 'application/json',
# #         'Referer': 'https://collectingcars.com/',
# #     }

# #     # Base payload (your original + pagination support)
# #     base_payload = {
# #         "searches": [
# #             {
# #                 "query_by": "title,productMake,vehicleMake,productYear,tags,lotType,driveSide,location,collectionId,modelId",
# #                 "query_by_weights": "9,8,7,6,5,4,3,2,1,0",
# #                 "text_match_type": "sum_score",
# #                 "sort_by": "rank:asc",
# #                 "highlight_full_fields": "*",
# #                 "facet_by": "lotType, regionCode, countryCode, saleFormat, noReserve, isBoosted, productMake, vendorType, driveSide, listingStage, tags",
# #                 "max_facet_values": 999,
# #                 "facet_counts": True,
# #                 "facet_stats": True,
# #                 "facet_distribution": True,
# #                 "facet_return_parent": True,
# #                 "collection": "production_cars",
# #                 "q": "*",
# #                 "filter_by": "listingStage:=[`live`] && countryCode:=[`AU`] && regionCode:=[`APAC`]",
# #                 "page": 1,
# #                 "per_page": 50   # ← increased for faster scraping (max ~100 usually safe)
# #             }
# #         ]
# #     }

# #     page = 1
# #     while True:
# #         # Update page number in payload
# #         base_payload["searches"][0]["page"] = page

# #         try:
# #             print(f"Fetching page {page}...")
# #             response = requests.post(api_url, headers=headers, json=base_payload, timeout=15)

# #             if response.status_code != 200:
# #                 print(f"API error: HTTP {response.status_code}")
# #                 break

# #             data = response.json()

# #             # Extract results from multi_search response
# #             if "results" not in data or not data["results"]:
# #                 print("No more results")
# #                 break

# #             result = data["results"][0]  # first (and only) search
# #             hits = result.get("hits", [])

# #             if not hits:
# #                 print(f"Page {page}: No more auctions")
# #                 break

# #             print(f"Page {page}: Found {len(hits)} auctions\n")

# #             for hit in hits:
# #                 doc = hit.get("document", {})

# #                 # Build clean car name
# #                 title = doc.get('title', 'Unknown Car')
# #                 year = str(doc.get('productYear', ''))
# #                 make = doc.get('productMake') or doc.get('vehicleMake', '')
# #                 model = doc.get('model', '')

# #                 car_name = f"{year} {make} {model}".strip()
# #                 if not car_name or car_name == year:
# #                     car_name = title

# #                 # Print as we scrape
# #                 print(f"Scraped: {car_name}")

# #                 lot = {
# #                     'source': 'collectingcars',
# #                     'status': 'live',
# #                     'auction_id': doc.get('id'),
# #                     'title': title,
# #                     'year': year,
# #                     'make': make,
# #                     'model': model,
# #                     'odometer': doc.get('odometer', '') or doc.get('mileage', ''),
# #                     'price': doc.get('currentBid') or doc.get('buyNowPrice') or doc.get('estimate', 'TBA'),
# #                     'auction_date': None,
# #                     'location': doc.get('location', 'Australia'),
# #                     'images': doc.get('images', []) or [doc.get('mainImage', '')],
# #                     'url': f"https://collectingcars.com/for-sale/{doc.get('slug', '')}",
# #                     'description': doc.get('description', ''),
# #                     'reserve': 'No' if doc.get('noReserve', False) else 'Yes',
# #                     'scrape_time': datetime.now(timezone.utc).isoformat()
# #                 }

# #                 # Try to parse auction end date
# #                 for date_key in ['endDate', 'auctionEndDate', 'closingDate']:
# #                     if doc.get(date_key):
# #                         try:
# #                             lot['auction_date'] = parse(doc[date_key]).isoformat()
# #                             break
# #                         except:
# #                             pass

# #                 # Fallback year/make/model from title
# #                 if not lot['make'] or not lot['model']:
# #                     m = re.search(r'(\d{4})\s*([a-zA-Z]+)\s*(.+?)(?:\s+|$)', lot['title'])
# #                     if m:
# #                         lot['year'] = m.group(1)
# #                         lot['make'] = m.group(2).capitalize()
# #                         lot['model'] = m.group(3).strip().capitalize()

# #                 if is_classic(lot):
# #                     listings.append(lot)

# #             page += 1
# #             time.sleep(1.2)  # polite delay

# #         except Exception as e:
# #             print(f"Page {page} error: {str(e)}")
# #             break
# #     print(listings)
# #     print(f"\nCollecting Cars total collected: {len(listings)} classic cars\n")
# #     return listings

# # def scrape_carbids(base_url):
# #     """
# #     Modern scraping approach for carbids.com.au (as of early-mid 2025 style)
# #     Tries two strategies:
# #     1. Wait longer + scroll to trigger lazy loading / angular render
# #     2. Intercept the most important API call (Search/Tags or similar)
# #     """
# #     listings = []
# #     print("Starting CarBids scrape...")

# #     # ── Strategy 1: Heavy browser simulation + waiting + scrolling ───────────────
# #     try:
# #         driver = get_driver()
# #         driver.set_window_size(1400, 900)  # bigger window sometimes helps

# #         # Build clean URL without fragment (angular often ignores it anyway)
# #         clean_url = base_url.split('#')[0]
# #         driver.get(clean_url)

# #         # Give Angular plenty of time to initialize + make initial requests
# #         try:
# #             WebDriverWait(driver, 25).until(
# #                 EC.presence_of_element_located((By.CSS_SELECTOR, "div.wrapper.col-lg-4"))
# #             )
# #         except:
# #             print("Main wrapper not found after 25s → probably still loading via XHR")

# #         # Aggressive scrolling to force lazy loading / infinite scroll simulation
# #         last_height = driver.execute_script("return document.body.scrollHeight")
# #         scroll_attempts = 0
# #         max_scrolls = 12

# #         while scroll_attempts < max_scrolls:
# #             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
# #             time.sleep(1.8 + scroll_attempts * 0.3)  # progressive delay

# #             new_height = driver.execute_script("return document.body.scrollHeight")
# #             if new_height == last_height:
# #                 scroll_attempts += 1
# #             else:
# #                 scroll_attempts = 0
# #                 last_height = new_height

# #         # Give final render chance
# #         time.sleep(4)

# #         soup = BeautifulSoup(driver.page_source, 'html.parser')
# #         driver.quit()

# #         lot_divs = soup.select('div.wrapper.col-lg-4.col-md-6.col-sm-6.mobile-margin')

# #         print(f"Found {len(lot_divs)} lot wrappers after heavy scrolling")

# #         if lot_divs:
# #             for div in lot_divs:
# #                 lot = {}

# #                 # Title → year/make/model
# #                 title_elem = div.select_one('h3.h5.p-b-10')
# #                 title = title_elem.get_text(strip=True) if title_elem else ''
                
# #                 # Very common pattern on carbids: "12/1969 Ford Mustang Mach 1"
# #                 m = re.match(r'(\d{1,2}/\d{4})\s+([^/]+?)\s+(.+?)(?:\s*\([^)]+\))?$', title)
# #                 if m:
# #                     lot['year']   = m.group(1).strip()
# #                     lot['make']   = m.group(2).strip()
# #                     lot['model']  = m.group(3).strip()
# #                 else:
# #                     lot['year'] = ''
# #                     lot['make'] = ''
# #                     lot['model'] = title

# #                 # Icons + values
# #                 def get_next_text(icon_class):
# #                     i = div.select_one(f'i.{icon_class.replace(" ", ".")}')
# #                     if i:
# #                         txt = i.next_sibling
# #                         return txt.strip() if txt and isinstance(txt, str) else ''
# #                     return ''

# #                 lot['odometer']    = get_next_text('fas fa-tachometer-alt')
# #                 lot['transmission'] = get_next_text('fas fa-cogs')
# #                 lot['fuel_type']   = get_next_text('fas fa-gas-pump')
# #                 lot['engine']      = get_next_text('fas fa-oil-can')

# #                 # Price / status
# #                 price_big = div.select_one('span.h2')
# #                 if price_big:
# #                     lot['price_range'] = price_big.get_text(strip=True)
# #                 else:
# #                     start_price = div.select_one('span.h4')
# #                     lot['price_range'] = start_price.get_text(strip=True) if start_price else 'Auction TBA'

# #                 # Countdown & calendar date
# #                 countdown = div.select_one('span[id^="closingCountdownTextGrid"]')
# #                 calendar_span = div.select_one('span[id^="closingTimeGrid"]')

# #                 lot['closing_text'] = countdown.get_text(strip=True) if countdown else ''
                
# #                 calendar_text = ''
# #                 if calendar_span:
# #                     txt = calendar_span.get_text(strip=True)
# #                     calendar_text = txt.strip('()[] ')
                
# #                 try:
# #                     lot['auction_date'] = parse(calendar_text) if calendar_text else None
# #                 except:
# #                     lot['auction_date'] = None

# #                 # Location
# #                 loc_div = div.select_one('div.bgm-white.p-5.m-r-5.p-l-15.p-r-15')
# #                 city = loc_div.get_text(strip=True) if loc_div else ''
                
# #                 state_span = div.select_one('span.p-5[style*="float: right"]')
# #                 state = state_span.get_text(strip=True) if state_span else ''
                
# #                 lot['location'] = f"{city} {state}".strip()

# #                 # Ref number
# #                 ref = div.select_one('mark.h5.p-t-5.p-b-5.p-r-10.p-l-10')
# #                 lot['reference_number'] = ref.get_text(strip=True) if ref else ''

# #                 # Images — try both ng-src and src
# #                 imgs = div.select('img.img-responsive')
# #                 lot['images'] = []
# #                 for img in imgs:
# #                     src = img.get('ng-src') or img.get('src') or ''
# #                     if src:
# #                         if src.startswith('//'): src = 'https:' + src
# #                         lot['images'].append(src)

# #                 # Detail link
# #                 a = div.select_one('a[ng-href]')
# #                 lot['url'] = a['ng-href'] if a else clean_url

# #                 # Quick description
# #                 lot['description'] = ' '.join(filter(None, [
# #                     lot.get('odometer'),
# #                     lot.get('transmission'),
# #                     lot.get('fuel_type'),
# #                     lot.get('engine')
# #                 ]))

# #                 lot['reserve'] = 'Yes'  # most are reserve
# #                 lot['body_style'] = extract_body_style(lot['description'])
# #                 lot['scrape_time'] = datetime.utcnow()
# #                 lot['source'] = 'carbids'

# #                 if is_classic(lot):
# #                     listings.append(lot)

# #             print(f"→ Successfully parsed {len(listings)} cars with browser method")
# #             print(listings)
# #             if listings:
# #                 return listings  # ← early return if we got something good

# #     except Exception as e:
# #         print("Browser heavy scraping failed:", str(e))

# #     # ── Strategy 2: Try to hit the API directly (most reliable long-term) ───────
# #     print("Falling back to API attempt...")

# #     try:
# #         s = requests.Session()
# #         s.headers.update({
# #             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
# #                          '(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
# #             'Accept': 'application/json, text/plain, */*',
# #             'X-Requested-With': 'XMLHttpRequest',
# #         })

# #         # Very often needed — get anti-forgery token first
# #         r = s.get(clean_url)
# #         soup_init = BeautifulSoup(r.text, 'html.parser')
# #         token_input = soup_init.find('input', {'name': '__RequestVerificationToken'})
# #         if token_input and token_input.get('value'):
# #             s.headers['__RequestVerificationToken'] = token_input['value']

# #         page = 0
# #         while True:
# #             payload = {
# #                 "top": 96,
# #                 "skip": page * 96,
# #                 "sort": {"aucClose": "asc"},
# #                 "tagName": "Unique and Classic Car Auctions",
# #                 "filter": {
# #                     "Display": True,
# #                     # You can add more filters later if needed
# #                 }
# #             }

# #             try:
# #                 resp = s.post(
# #                     "https://carbids.com.au/Search/Tags",
# #                     json=payload,
# #                     timeout=20
# #                 )

# #                 if resp.status_code != 200:
# #                     print(f"API returned {resp.status_code} → stopping")
# #                     break

# #                 data = resp.json()

# #                 auctions = data.get('auctions', [])  # ← field name may change!
# #                 if not auctions:
# #                     print("No more auctions in API response")
# #                     break

# #                 print(f"API page {page+1} → got {len(auctions)} cars")

# #                 for auc in auctions:
# #                     lot = {
# #                         'source': 'carbids',
# #                         'url': auc.get('AucDetailsUrlLink', clean_url),
# #                         'reference_number': auc.get('aucReferenceNo', ''),
# #                         'year': str(auc.get('aucYear', '')),
# #                         'make': auc.get('aucMake', ''),
# #                         'model': auc.get('aucModel', ''),
# #                         'odometer': auc.get('aucOdometer', ''),
# #                         'transmission': auc.get('aucTransmission', ''),
# #                         'fuel_type': auc.get('aucFuelType', ''),
# #                         'engine': f"{auc.get('aucCapacity','')} {auc.get('aucCylinder','')} cyl",
# #                         'price_range': auc.get('aucCurrentBid', 0) or 'Auction TBA',
# #                         'location': f"{auc.get('aucCity','')} {auc.get('aucState','')}".strip(),
# #                         'images': [auc.get('aucCarsThumbnailUrl')] + 
# #                                  (auc.get('aucMediumThumbnailUrlList', []) or []),
# #                         'closing_text': auc.get('closingCountdownText', ''),
# #                         'auction_date': parse(auc['aucCloseUtc']) if auc.get('aucCloseUtc') else None,
# #                         'description': auc.get('aucTitle', ''),
# #                         'reserve': 'Yes',
# #                         'scrape_time': datetime.utcnow(),
# #                     }

# #                     if is_classic(lot):
# #                         listings.append(lot)

# #                 page += 1
# #                 time.sleep(1.4)  # polite delay

# #             except Exception as inner_e:
# #                 print("API call failed:", str(inner_e))
# #                 break

# #     except Exception as outer_e:
# #         print("API fallback also failed:", str(outer_e))
# #     print(listings)
# #     print(f"Final count from CarBids: {len(listings)} cars")
# #     return listings

# # def scrape_bennetts(base_url):
# #     pages = [base_url, base_url + '/off-site.php']  # Scrape main and off-site
# #     all_listings = []
# #     for page_url in pages:
# #         try:
# #             driver = get_driver()
# #             driver.get(page_url)
# #             soup = BeautifulSoup(driver.page_source, 'html.parser')
# #             driver.quit()

# #             # Parse auction date from h3 in sitename
# #             sitename = soup.find('div', id='sitename')
# #             h3 = sitename.find('h3') if sitename else None
# #             auction_text = h3.text.strip() if h3 else ''
# #             date_match = re.search(r'(\d{1,2}[ST|ND|RD|TH]{0,2} \w+ \d{4})', auction_text.upper())
# #             time_match = re.search(r'@ (\d{1,2}[AP]M)', auction_text.upper())
# #             auction_date_str = ''
# #             if date_match:
# #                 date_str = re.sub(r'([ST|ND|RD|TH])', '', date_match.group(1))
# #                 auction_date_str += date_str
# #             if time_match:
# #                 auction_date_str += ' ' + time_match.group(1)
# #             auction_date = None
# #             try:
# #                 auction_date = parse(auction_date_str)
# #             except:
# #                 pass

# #             # Find all clear divs with column
# #             sections = soup.find_all('div', class_='clear')
# #             for section in sections:
# #                 column = section.find('div', class_='column column-600 column-left')
# #                 if column:
# #                     h3_cat = column.find('h3')
# #                     category = h3_cat.text.strip() if h3_cat else ''
# #                     table = column.find('table')
# #                     if table:
# #                         tbody = table.find('tbody')
# #                         trs = tbody.find_all('tr') if tbody else table.find_all('tr')
# #                         for tr in trs[1:]:  # Skip header
# #                             tds = tr.find_all('td')
# #                             if len(tds) == 7:
# #                                 photo_td = tds[0]
# #                                 a = photo_td.find('a')
# #                                 detail_url = base_url + '/' + a['href'].lstrip('/') if a else ''
# #                                 img = photo_td.find('img')
# #                                 image_src = base_url + '/' + img['src'].lstrip('/') if img and img['src'].startswith('images') else img['src']
# #                                 make = tds[1].text.strip()
# #                                 stock_model = tds[2].text.strip()
# #                                 parts = stock_model.split('/')
# #                                 stock_ref = parts[0].strip() if parts else ''
# #                                 model = parts[1].strip() if len(parts) > 1 else stock_model
# #                                 year = tds[3].text.strip()
# #                                 options = tds[4].text.strip()
# #                                 location_td = tds[5]
# #                                 location = location_td.text.strip().replace('\n', '').replace('br /', '')
# #                                 lot = {
# #                                     'source': page_url,
# #                                     'make': make,
# #                                     'model': model,
# #                                     'year': year,
# #                                     'price_range': None,  # No price in list
# #                                     'auction_date': auction_date,
# #                                     'location': location,
# #                                     'images': [image_src] if image_src else [],
# #                                     'url': detail_url,
# #                                     'description': options,  # Use options as desc for now; scrape detail for full
# #                                     'reserve': 'Yes',  # Assume
# #                                     'body_style': extract_body_style(options),
# #                                     'transmission': extract_transmission(options),
# #                                     'scrape_time': datetime.now()
# #                                 }
# #                                 if is_classic(lot):
# #                                     all_listings.append(lot)
# #         except Exception as e:
# #             print(f"Error scraping Bennetts page {page_url}: {e}")
# #     print(f"Scraped {len(all_listings)} listings from Bennetts")
# #     return all_listings

# # def scrape_burnsandco(base_url):
# #     pages = [base_url + '/current-auctions/', base_url + '/upcoming-auctions/']
# #     all_listings = []
# #     for page_url in pages:
# #         try:
# #             driver = get_driver()
# #             driver.get(page_url)
# #             soup = BeautifulSoup(driver.page_source, 'html.parser')
# #             driver.quit()

# #             articles = soup.find_all('article', class_='regular masonry-blog-item')
# #             for article in articles:
# #                 img_link = article.find('a', class_='img-link')
# #                 detail_url = img_link['href'] if img_link else ''
# #                 img = img_link.find('img') if img_link else None
# #                 image_src = img['src'] if img else ''
# #                 meta_category = article.find('span', class_='meta-category')
# #                 category = meta_category.text.strip() if meta_category else ''
# #                 date_item = article.find('span', class_='date-item')
# #                 auction_date_str = date_item.text.strip() if date_item else ''
# #                 auction_date = None
# #                 try:
# #                     auction_date = parse(auction_date_str)
# #                 except:
# #                     pass
# #                 title_a = article.find('h3', class_='title').find('a') if article.find('h3', class_='title') else None
# #                 title = title_a.text.strip() if title_a else ''
# #                 excerpt = article.find('div', class_='excerpt').text.strip() if article.find('div', class_='excerpt') else ''
# #                 place = article.find('p', class_='place').text.strip() if article.find('p', class_='place') else ''
# #                 bid_links = article.find_all('p', class_='registration_bidding_link')
# #                 for bid_p in bid_links:
# #                     bid_a = bid_p.find('a')
# #                     bid_url = bid_a['href'] if bid_a else ''
# #                     # Now scrape lots from bid_url
# #                     catalogue_lots = scrape_catalogue(bid_url)
# #                     for cat_lot in catalogue_lots:
# #                         cat_lot['auction_date'] = auction_date or cat_lot.get('auction_date')
# #                         cat_lot['location'] = place or cat_lot.get('location')
# #                         cat_lot['source'] = bid_url
# #                         all_listings.append(cat_lot)
# #         except Exception as e:
# #             print(f"Error scraping Burns page {page_url}: {e}")
# #     print(f"Scraped {len(all_listings)} listings from Burns & Co")
# #     return all_listings

# # def scrape_catalogue(catalogue_url):
# #     listings = []
# #     try:
# #         driver = get_driver()
# #         driver.get(catalogue_url)
# #         soup = BeautifulSoup(driver.page_source, 'html.parser')
# #         driver.quit()

# #         # Adjust based on actual catalogue structure
# #         # Assuming lots are in divs with class 'lot-item' or similar; inspect site
# #         lot_items = soup.find_all('div', class_='lot-item')  # Placeholder class
# #         for item in lot_items:
# #             lot_number = item.find('span', class_='lot-number').text.strip() if item.find('span', class_='lot-number') else ''
# #             desc = item.find('div', class_='lot-description').text.strip() if item.find('div', class_='lot-description') else ''
# #             # Parse desc for make, model, year
# #             match = re.match(r'(\d{4})? ?(.*?) (.*)', desc)
# #             year = match.group(1) if match and match.group(1) else ''
# #             make = match.group(2) if match else ''
# #             model = match.group(3) if match else desc
# #             images = [img['src'] for img in item.find_all('img')]
# #             detail_a = item.find('a', class_='lot-detail')
# #             detail_url = catalogue_url + detail_a['href'] if detail_a else ''
# #             current_bid = item.find('span', class_='current-bid').text.strip() if item.find('span', class_='current-bid') else ''
# #             lot = {
# #                 'lot_number': lot_number,
# #                 'make': make,
# #                 'model': model,
# #                 'year': year,
# #                 'price_range': current_bid,  # Use current bid as estimate
# #                 'auction_date': None,  # Parse from page if needed
# #                 'location': None,
# #                 'images': images,
# #                 'url': detail_url,
# #                 'description': desc,
# #                 'reserve': 'Yes',
# #                 'body_style': extract_body_style(desc),
# #                 'transmission': extract_transmission(desc),
# #                 'scrape_time': datetime.now()
# #             }
# #             if is_classic(lot):
# #                 listings.append(lot)
# #     except Exception as e:
# #         print(f"Error scraping catalogue {catalogue_url}: {e}")
# #     return listings

# # def parse_lot(item, url):
# #     # Generic parse_lot remains for other sites
# #     try:
# #         description = item.find('p', class_='desc') or item.find('div', class_='description')  # Adjust
# #         description_text = description.text.strip() if description else ''
# #         year_elem = item.find('span', class_='year') or item.find('h3')  # Adjust
# #         year_str = year_elem.text.strip() if year_elem else '0'
# #         make_elem = item.find('span', class_='make') or item.find('h2')
# #         model_elem = item.find('span', class_='model')
# #         price_elem = item.find('span', class_='estimate') or item.find('div', class_='price')
# #         date_elem = item.find('span', class_='date')
# #         location_elem = item.find('span', class_='location')
# #         link_elem = item.find('a', class_='lot-link') or item.find('a')

# #         lot = {
# #             'make': make_elem.text.strip() if make_elem else None,
# #             'model': model_elem.text.strip() if model_elem else None,
# #             'year': year_str,
# #             'price_range': price_elem.text.strip() if price_elem else None,
# #             'auction_date': parse_date(date_elem.text.strip()) if date_elem else None,
# #             'location': location_elem.text.strip() if location_elem else 'Online',
# #             'images': [img['src'] for img in item.find_all('img', class_='thumbnail')][:6],
# #             'url': link_elem['href'] if link_elem else url,
# #             'description': description_text,
# #             'reserve': 'No' if 'no reserve' in description_text.lower() else 'Yes',
# #             'body_style': extract_body_style(description_text),
# #             'transmission': extract_transmission(description_text),
# #             'scrape_time': datetime.now()
# #         }
# #         return lot
# #     except:
# #         return None

# # def parse_date(date_str):
# #     try:
# #         return parse(date_str)
# #     except:
# #         return None

# # def extract_body_style(desc):
# #     lower_desc = desc.lower()
# #     styles = ['coupe', 'convertible', 'sedan', 'wagon', 'ute', 'truck']
# #     for style in styles:
# #         if style in lower_desc:
# #             return style
# #     return None

# # def extract_transmission(desc):
# #     lower_desc = desc.lower()
# #     if 'manual' in lower_desc:
# #         return 'manual'
# #     if 'auto' in lower_desc or 'automatic' in lower_desc:
# #         return 'auto'
# #     return None

# # def is_classic(lot):
# #     try:
# #         year = int(lot['year'])
# #     except:
# #         year = 0
# #     desc = lot['description'].lower() if lot['description'] else ''
# #     return year < 1990 or any(word in desc for word in ['collector', 'classic', 'future classic', 'modern classic'])

# # def normalize_auction_date(ad):
# #     """Return a datetime or None from various auction_date formats."""
# #     if not ad:
# #         return None
# #     # If already datetime
# #     if isinstance(ad, datetime):
# #         return ad
# #     # If ISO string
# #     if isinstance(ad, str):
# #         try:
# #             return parse(ad)
# #         except:
# #             return None
# #     # If dateutil object or others
# #     try:
# #         return parse(str(ad))
# #     except:
# #         return None

# # def scrape_all():
# #     """
# #     Scrape each source and INSERT/UPSERT every scraped lot into MongoDB.
# #     NOTE: changed to insert all scraped lots regardless of auction_date.
# #     """
# #     all_lots = []
# #     for source in SOURCES:
# #         lots = scrape_site(source)
# #         all_lots.extend(lots)
    
# #     # Upsert all scraped lots (no longer requiring auction_date)
# #     for lot in all_lots:
# #         # ensure scrape_time
# #         if not lot.get('scrape_time'):
# #             lot['scrape_time'] = datetime.utcnow()
# #         # normalize auction_date to datetime or None
# #         lot['auction_date'] = normalize_auction_date(lot.get('auction_date'))
# #         # ensure url exists
# #         if not lot.get('url'):
# #             lot['url'] = f"source://{lot.get('source','unknown')}/{uuid.uuid4()}"
# #         # upsert by url
# #         try:
# #             lots_collection.update_one({'url': lot['url']}, {'$set': lot}, upsert=True)
# #         except Exception as e:
# #             print(f"Failed to upsert lot {lot.get('url')}: {e}")
    
# #     # Move ended lots to sold_collection (only those with auction_date that has passed)
# #     now = datetime.now()
# #     ended = lots_collection.find({'auction_date': {'$lt': now}})
# #     for end in ended:
# #         try:
# #             sold_collection.insert_one(end)
# #             lots_collection.delete_one({'_id': end['_id']})
# #         except Exception as e:
# #             print(f"Error moving ended lot {_id}: {e}")
    
# #     # Cleanup old sold entries older than two years
# #     two_years_ago = now - timedelta(days=730)
# #     try:
# #         sold_collection.delete_many({'auction_date': {'$lt': two_years_ago}})
# #     except Exception as e:
# #         print(f"Error cleaning sold_collection: {e}")

# # # Scheduler
# # scheduler = BackgroundScheduler()
# # scheduler.add_job(scrape_all, 'interval', hours=4)
# # scheduler.start()

# # @app.route('/api/scrape', methods=['POST'])
# # @swag_from({
# #     'tags': ['Admin'],
# #     'summary': 'Trigger manual scrape',
# #     'security': [{'Bearer': []}],
# #     'responses': {
# #         '200': {'description': 'Scraping completed'}
# #     }
# # })
# # @jwt_required()
# # def manual_scrape():
# #     scrape_all()
# #     return jsonify({'message': 'Scraping completed'})

# # @app.route('/api/register', methods=['POST'])
# # @swag_from({
# #     'tags': ['Users'],
# #     'summary': 'Register a new user',
# #     'parameters': [
# #         {
# #             'name': 'body',
# #             'in': 'body',
# #             'required': True,
# #             'schema': {
# #                 'type': 'object',
# #                 'properties': {
# #                     'email': {'type': 'string'},
# #                     'password': {'type': 'string'}
# #                 },
# #                 'required': ['email', 'password']
# #             }
# #         }
# #     ],
# #     'responses': {
# #         '200': {'description': 'User registered'},
# #         '400': {'description': 'User already exists'}
# #     }
# # })
# # def register():
# #     data = request.json
# #     email = data['email']
# #     password = data['password']  # Hash in production using bcrypt
# #     if users_collection.find_one({'email': email}):
# #         return jsonify({'error': 'User exists'}), 400
# #     user_id = users_collection.insert_one({'email': email, 'password': password}).inserted_id
# #     user = User(str(user_id), email)
# #     login_user(user)
# #     return jsonify({'message': 'Registered'})

# # @app.route('/api/login', methods=['POST'])
# # @swag_from({
# #     'tags': ['Users'],
# #     'summary': 'Login user',
# #     'parameters': [
# #         {
# #             'name': 'body',
# #             'in': 'body',
# #             'required': True,
# #             'schema': {
# #                 'type': 'object',
# #                 'properties': {
# #                     'email': {'type': 'string'},
# #                     'password': {'type': 'string'}
# #                 },
# #                 'required': ['email', 'password']
# #             }
# #         }
# #     ],
# #     'responses': {
# #         '200': {'description': 'Login successful, token returned'},
# #         '401': {'description': 'Invalid credentials'}
# #     }
# # })
# # def login():
# #     data = request.json
# #     email = data['email']
# #     password = data['password']
# #     user_doc = users_collection.find_one({'email': email, 'password': password})
# #     if user_doc:
# #         user = User(str(user_doc['_id']), email)
# #         login_user(user)
# #         access_token = create_access_token(identity=str(user_doc['_id']))
# #         return jsonify({'token': access_token})
# #     return jsonify({'error': 'Invalid credentials'}), 401

# # @app.route('/api/logout')
# # @swag_from({
# #     'tags': ['Users'],
# #     'summary': 'Logout user',
# #     'responses': {
# #         '200': {'description': 'Logged out'}
# #     }
# # })
# # @login_required
# # def logout():
# #     logout_user()
# #     return jsonify({'message': 'Logged out'})

# # @app.route('/api/calendar', methods=['GET'])
# # @swag_from({
# #     'tags': ['Auctions'],
# #     'summary': 'Get auction calendar',
# #     'parameters': [
# #         {'name': 'state', 'in': 'query', 'type': 'string', 'description': 'Filter by state'},
# #         {'name': 'month', 'in': 'query', 'type': 'string', 'description': 'Filter by month (YYYY-MM)'},
# #         {'name': 'auction_house', 'in': 'query', 'type': 'string', 'description': 'Filter by auction house'},
# #         {'name': 'online_only', 'in': 'query', 'type': 'boolean', 'description': 'Filter online only'}
# #     ],
# #     'responses': {
# #         '200': {'description': 'List of upcoming auctions'}
# #     }
# # })
# # def calendar():
# #     state = request.args.get('state')
# #     month = request.args.get('month')
# #     auction_house = request.args.get('auction_house')
# #     online_only = request.args.get('online_only') == 'true'
    
# #     query = {}
# #     if state:
# #         query['location'] = {'$regex': state, '$options': 'i'}
# #     if month:
# #         try:
# #             start = datetime.strptime(month + '-01', '%Y-%m-%d')
# #             end = start + timedelta(days=31)
# #             query['auction_date'] = {'$gte': start, '$lt': end}
# #         except:
# #             pass
# #     if auction_house:
# #         query['source'] = {'$regex': auction_house, '$options': 'i'}
# #     if online_only:
# #         query['location'] = 'Online'
    
# #     now = datetime.now()
# #     upcoming = lots_collection.find({
# #         **query,
# #         'auction_date': {'$gte': now, '$lt': now + timedelta(days=90)}
# #     }).sort('auction_date', 1)
    
# #     return jsonify([dict(lot, **{'_id': str(lot['_id'])}) for lot in upcoming])

# # @app.route('/api/search', methods=['GET'])
# # @swag_from({
# #     'tags': ['Auctions'],
# #     'summary': 'Search for lots',
# #     'parameters': [
# #         {'name': 'make', 'in': 'query', 'type': 'string'},
# #         {'name': 'model', 'in': 'query', 'type': 'string'},
# #         {'name': 'variant', 'in': 'query', 'type': 'string'},
# #         {'name': 'year_min', 'in': 'query', 'type': 'integer'},
# #         {'name': 'year_max', 'in': 'query', 'type': 'integer'},
# #         {'name': 'price_min', 'in': 'query', 'type': 'integer'},
# #         {'name': 'price_max', 'in': 'query', 'type': 'integer'},
# #         {'name': 'state', 'in': 'query', 'type': 'string'},
# #         {'name': 'auction_house', 'in': 'query', 'type': 'string'},
# #         {'name': 'no_reserve', 'in': 'query', 'type': 'boolean'},
# #         {'name': 'body_style', 'in': 'query', 'type': 'string'},
# #         {'name': 'transmission', 'in': 'query', 'type': 'string'},
# #         {'name': 'newly_added', 'in': 'query', 'type': 'string', 'description': 'e.g., 24h'},
# #         {'name': 'sort', 'in': 'query', 'type': 'string', 'description': 'e.g., auction_date asc'}
# #     ],
# #     'responses': {
# #         '200': {'description': 'Search results'}
# #     }
# # })
# # def search():
# #     make = request.args.get('make')
# #     model = request.args.get('model')
# #     variant = request.args.get('variant')
# #     year_min = request.args.get('year_min')
# #     year_max = request.args.get('year_max')
# #     price_min = request.args.get('price_min')
# #     price_max = request.args.get('price_max')
# #     state = request.args.get('state')
# #     auction_house = request.args.get('auction_house')
# #     no_reserve = request.args.get('no_reserve') == 'true'
# #     body_style = request.args.get('body_style')
# #     transmission = request.args.get('transmission')
# #     newly_added = request.args.get('newly_added')
    
# #     query = {}
# #     if make:
# #         query['make'] = {'$regex': make, '$options': 'i'}
# #     if model:
# #         query['model'] = {'$regex': model, '$options': 'i'}
# #     if variant:
# #         query['variant'] = {'$regex': variant, '$options': 'i'}
# #     if year_min or year_max:
# #         query['year'] = {}
# #         if year_min:
# #             query['year']['$gte'] = year_min
# #         if year_max:
# #             query['year']['$lte'] = year_max
# #     if price_min or price_max:
# #         # Assuming price_range is {'low': int, 'high': int}; parse in scrape if string
# #         if price_min:
# #             query['price_range.low'] = {'$gte': int(price_min)}
# #         if price_max:
# #             query['price_range.high'] = {'$lte': int(price_max)}
# #     if state:
# #         query['location'] = {'$regex': state, '$options': 'i'}
# #     if auction_house:
# #         query['source'] = {'$regex': auction_house, '$options': 'i'}
# #     if no_reserve:
# #         query['reserve'] = 'No'
# #     if body_style:
# #         query['body_style'] = {'$regex': body_style, '$options': 'i'}
# #     if transmission:
# #         query['transmission'] = {'$regex': transmission, '$options': 'i'}
# #     if newly_added:
# #         try:
# #             hours = int(newly_added[:-1])
# #             time_ago = datetime.now() - timedelta(hours=hours)
# #             query['scrape_time'] = {'$gte': time_ago}
# #         except:
# #             pass
    
# #     sort = request.args.get('sort', 'auction_date asc').split(' ')
# #     sort_field = sort[0]
# #     sort_dir = 1 if len(sort) > 1 and sort[1] == 'asc' else -1
    
# #     results = lots_collection.find(query).sort(sort_field, sort_dir)
# #     return jsonify([dict(result, **{'_id': str(result['_id'])}) for result in results])

# # @app.route('/api/lot/<lot_id>', methods=['GET'])
# # @swag_from({
# #     'tags': ['Auctions'],
# #     'summary': 'Get individual lot details',
# #     'parameters': [
# #         {'name': 'lot_id', 'in': 'path', 'type': 'string', 'required': True}
# #     ],
# #     'responses': {
# #         '200': {'description': 'Lot details'},
# #         '404': {'description': 'Not found'}
# #     }
# # })
# # def get_lot(lot_id):
# #     lot = lots_collection.find_one({'_id': ObjectId(lot_id)})
# #     if not lot:
# #         return jsonify({'error': 'Not found'}), 404
# #     lot['_id'] = str(lot['_id'])
# #     related = sold_collection.find({
# #         'make': lot['make'],
# #         'model': lot['model'],
# #         'year': lot['year']
# #     }).limit(5)
# #     lot['related'] = [dict(rel, **{'_id': str(rel['_id'])}) for rel in related]
# #     return jsonify(lot)

# # @app.route('/api/watchlist', methods=['GET', 'POST'])
# # @swag_from({
# #     'tags': ['Users'],
# #     'summary': 'Manage watchlist',
# #     'security': [{'Bearer': []}],
# #     'parameters': [
# #         {
# #             'name': 'body',
# #             'in': 'body',
# #             'required': False,
# #             'schema': {
# #                 'type': 'object',
# #                 'properties': {
# #                     'lot_id': {'type': 'string'}
# #                 }
# #             }
# #         }
# #     ],
# #     'responses': {
# #         '200': {'description': 'Watchlist or added message'}
# #     }
# # })
# # @jwt_required()
# # def watchlist():
# #     user_id = get_jwt_identity()
# #     if request.method == 'POST':
# #         lot_id = request.json.get('lot_id')
# #         watchlists_collection.update_one(
# #             {'user_id': user_id},
# #             {'$addToSet': {'lots': ObjectId(lot_id)}},
# #             upsert=True
# #         )
# #         return jsonify({'message': 'Added'})
    
# #     watch = watchlists_collection.find_one({'user_id': user_id})
# #     if watch:
# #         lots = lots_collection.find({'_id': {'$in': watch['lots']}})
# #         return jsonify([dict(lot, **{'_id': str(lot['_id'])}) for lot in lots])
# #     return jsonify([])

# # @app.route('/api/saved_searches', methods=['GET', 'POST'])
# # @swag_from({
# #     'tags': ['Users'],
# #     'summary': 'Manage saved searches',
# #     'security': [{'Bearer': []}],
# #     'responses': {
# #         '200': {'description': 'Saved searches or saved message'}
# #     }
# # })
# # @jwt_required()
# # def saved_searches():
# #     user_id = get_jwt_identity()
# #     if request.method == 'POST':
# #         search_params = request.json
# #         saved_searches_collection.insert_one({'user_id': user_id, **search_params})
# #         return jsonify({'message': 'Saved'})
    
# #     searches = saved_searches_collection.find({'user_id': user_id})
# #     return jsonify([dict(s, **{'_id': str(s['_id'])}) for s in searches])

# # def send_alert(user_id, message):
# #     user = users_collection.find_one({'_id': ObjectId(user_id)})
# #     if user:
# #         smtp_server = os.getenv('SMTP_SERVER')
# #         smtp_port = int(os.getenv('SMTP_PORT', 587))
# #         sender = os.getenv('SENDER_EMAIL')
# #         password = os.getenv('SENDER_PASSWORD')
        
# #         msg = MIMEText(message)
# #         msg['Subject'] = 'Auction Alert'
# #         msg['From'] = sender
# #         msg['To'] = user['email']
        
# #         with smtplib.SMTP(smtp_server, smtp_port) as server:
# #             server.starttls()
# #             server.login(sender, password)
# #             server.sendmail(sender, user['email'], msg.as_string())

# # @app.route('/api/sold', methods=['GET'])
# # @swag_from({
# #     'tags': ['Auctions'],
# #     'summary': 'Get sold prices archive',
# #     'parameters': [
# #         {'name': 'make', 'in': 'query', 'type': 'string'},
# #         {'name': 'model', 'in': 'query', 'type': 'string'},
# #         {'name': 'year', 'in': 'query', 'type': 'integer'}
# #     ],
# #     'responses': {
# #         '200': {'description': 'Sold lots'}
# #     }
# # })
# # def sold():
# #     make = request.args.get('make')
# #     model = request.args.get('model')
# #     year = request.args.get('year')
    
# #     query = {}
# #     if make:
# #         query['make'] = {'$regex': make, '$options': 'i'}
# #     if model:
# #         query['model'] = {'$regex': model, '$options': 'i'}
# #     if year:
# #         query['year'] = year
    
# #     results = sold_collection.find(query).sort('auction_date', -1)
# #     return jsonify([dict(r, **{'_id': str(r['_id'])}) for r in results])

# # @app.route('/api/market_pulse', methods=['GET'])
# # @swag_from({
# #     'tags': ['Auctions'],
# #     'summary': 'Get market pulse data',
# #     'responses': {
# #         '200': {'description': 'Top sales and risers'}
# #     }
# # })
# # def market_pulse():
# #     now = datetime.now()
# #     month_start = now - timedelta(days=30)
# #     top_sales = sold_collection.find({'auction_date': {'$gte': month_start}}).sort('total_price', -1).limit(10)
# #     top_sales_list = [dict(s, **{'_id': str(s['_id'])}) for s in top_sales]
    
# #     pipeline = [
# #         {'$match': {'auction_date': {'$gte': month_start}}},
# #         {'$group': {'_id': {'make': '$make', 'model': '$model'}, 'avg_price': {'$avg': '$total_price'}, 'count': {'$sum': 1}}},
# #         {'$sort': {'avg_price': -1}},
# #         {'$limit': 10}
# #     ]
# #     risers = list(sold_collection.aggregate(pipeline))
# #     return jsonify({'top_sales': top_sales_list, 'risers': risers})

# # @app.route('/api/on_the_block', methods=['GET'])
# # @swag_from({
# #     'tags': ['Auctions'],
# #     'summary': 'Get lots closing soon',
# #     'responses': {
# #         '200': {'description': 'Live lots'}
# #     }
# # })
# # def on_the_block():
# #     now = datetime.now()
# #     two_hours = now + timedelta(hours=2)
# #     live = lots_collection.find({'auction_date': {'$gte': now, '$lt': two_hours}})
# #     return jsonify([dict(l, **{'_id': str(l['_id'])}) for l in live])

# # @app.route('/api/auction_houses', methods=['GET'])
# # @swag_from({
# #     'tags': ['Auctions'],
# #     'summary': 'Get auction houses directory',
# #     'responses': {
# #         '200': {'description': 'List of auction houses'}
# #     }
# # })
# # def auction_houses():
# #     houses = set(lot.get('source') for lot in lots_collection.find({}, {'source': 1}))
# #     directory = []
# #     for house in houses:
# #         upcoming = lots_collection.count_documents({'source': house, 'auction_date': {'$gt': datetime.now()}})
# #         name = house.split('//')[-1].split('.')[0] if house else 'Unknown'
# #         directory.append({
# #             'name': name,
# #             'upcoming': upcoming,
# #             'buyers_premium': 'Unknown'  # Add scraping if available
# #         })
# #     return jsonify(directory)

# # # Initial scrape
# # scrape_all()

# # if __name__ == '__main__':
# #     app.run(debug=True)
# import os
# import datetime
# from datetime import timedelta
# import requests
# from bs4 import BeautifulSoup
# from flask import Flask, request, jsonify, session
# from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
# from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
# from flask_cors import CORS
# from pymongo import MongoClient
# from apscheduler.schedulers.background import BackgroundScheduler
# import smtplib
# from email.mime.text import MIMEText
# from dotenv import load_dotenv
# from flasgger import Swagger, swag_from
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from dateutil.parser import parse
# from datetime import datetime, timezone
# from bson.objectid import ObjectId
# import re
# import time
# import uuid

# load_dotenv()

# app = Flask(__name__)
# app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')
# CORS(app)

# # JWT Setup
# jwt = JWTManager(app)
# app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret')

# # Login Manager
# login_manager = LoginManager()
# login_manager.init_app(app)

# # Swagger Setup
# swagger = Swagger(app, template={
#     "swagger": "2.0",
#     "info": {
#         "title": "AusClassicAuctions API",
#         "description": "API for Australian Classic Car Auctions Aggregator",
#         "version": "1.0.0"
#     },
#     "securityDefinitions": {
#         "Bearer": {
#             "type": "apiKey",
#             "name": "Authorization",
#             "in": "header",
#             "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
#         }
#     }
# })

# # MongoDB Setup
# client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/'))
# db = client['ausclassicauctions']
# lots_collection = db['lots']  # Current and upcoming lots
# sold_collection = db['sold']  # Sold archive
# users_collection = db['users']
# watchlists_collection = db['watchlists']
# saved_searches_collection = db['saved_searches']

# # Create indexes for fast queries
# lots_collection.create_index([('auction_date', 1), ('source', 1), ('make', 1), ('model', 1), ('location', 1), ('scrape_time', 1)])
# sold_collection.create_index([('auction_date', 1), ('source', 1), ('make', 1), ('model', 1), ('location', 1)])

# # User Model
# class User(UserMixin):
#     def __init__(self, id, email):
#         self.id = id
#         self.email = email

# @login_manager.user_loader
# def load_user(user_id):
#     user = users_collection.find_one({'_id': ObjectId(user_id)})
#     if user:
#         return User(user['_id'], user['email'])
#     return None

# # Buyers Premiums (approximate percentages, update as needed)
# house_premiums = {
#     'tradinggarage': 0.12,
#     'carbids': 0.15,
#     'collectingcars': 0.06,
#     'bennettsclassicauctions': 0.125,
#     'burnsandco': 0.15,
#     'lloydsonline': 0.20,
#     'seven82motors': 0.10,
#     'chicaneauctions': 0.12,
#     'doningtonauctions': 0.125
# }

# # Scraping Sources (uncommented all for full coverage)
# SOURCES = [
#     {'url': 'https://www.tradinggarage.com', 'name': 'tradinggarage'},
#     # {'url': 'https://carbids.com.au/t/unique-and-classic-car-auctions#!?page=1&count=96&filter%5BDisplay%5D=true', 'name': 'carbids'},
#     # {'url': 'https://collectingcars.com/buy?refinementList%5BlistingStage%5D%5B0%5D=live&refinementList%5BregionCode%5D%5B0%5D=APAC&refinementList%5BcountryCode%5D%5B0%5D=AU', 'name': 'collectingcars'},
#     # {'url': 'https://burnsandcoauctions.com.au', 'name': 'burnsandco'},
#     # {'url': 'https://www.lloydsonline.com.au/AuctionLots.aspx?smode=0&aid=65946', 'name': 'lloydsonline'},
#     # {'url': 'https://www.seven82motors.com.au', 'name': 'seven82motors'},
#     # {'url': 'https://www.chicaneauctions.com.au', 'name': 'chicaneauctions'},
#     # {'url': 'https://www.doningtonauctions.com.au', 'name': 'doningtonauctions'},
#     # {'url': 'https://www.bennettsclassicauctions.com.au', 'name': 'bennettsclassicauctions'}
# ]

# def get_driver():
#     options = Options()
#     options.headless = True
#     service = Service(ChromeDriverManager().install())
#     return webdriver.Chrome(service=service, options=options)

# def parse_price(price_str):
#     if not price_str or price_str == 'TBA':
#         return None
#     try:
#         if isinstance(price_str, (int, float)):
#             val = float(price_str)
#             return {'low': val, 'high': val}
#         price_str = str(price_str).replace(',', '').replace('$', '').strip()
#         m = re.match(r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)', price_str)
#         if m:
#             return {'low': float(m.group(1)), 'high': float(m.group(2))}
#         m = re.match(r'(\d+(?:\.\d+)?)', price_str)
#         if m:
#             val = float(m.group(1))
#             return {'low': val, 'high': val}
#     except:
#         pass
#     return None

# def scrape_site(source):
#     url = source['url']
#     name = source['name']
#     if name == 'bennettsclassicauctions':
#         return scrape_bennetts(url)
#     elif name == 'burnsandco':
#         return scrape_burnsandco(url)
#     elif name == 'carbids':
#         return scrape_carbids(url)
#     elif name == 'tradinggarage':
#         return scrape_tradinggarage(url)    
#     elif name == 'collectingcars':
#         return scrape_collectingcars()
#     else:
#         # Generic scraper for other sites
#         try:
#             driver = get_driver()
#             driver.get(url)
#             soup = BeautifulSoup(driver.page_source, 'html.parser')
#             driver.quit()

#             listings = []
#             item_class = 'auction-item'  # Adjust per site as needed
#             for item in soup.find_all('div', class_=item_class):
#                 lot = parse_lot(item, url)
#                 if lot and is_classic(lot):
#                     lot['source'] = name
#                     listings.append(lot)
#             return listings
#         except Exception as e:
#             print(f"Error scraping {url}: {e}")
#             return []

# def scrape_tradinggarage(base_url="https://www.tradinggarage.com"):
#     listings = []
#     session = requests.Session()
#     session.headers.update({
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
#         'Accept': 'application/json',
#         'Referer': 'https://www.tradinggarage.com/',
#     })

#     endpoints = {
#         'live': 'https://portal.tradinggarage.com/api/v1/auctions?status=live',
#         'coming_soon': 'https://portal.tradinggarage.com/api/v1/auctions?status=coming_soon'
#     }

#     for status, api_url in endpoints.items():
#         try:
#             r = session.get(api_url, timeout=12)
#             if r.status_code != 200:
#                 continue
#             data = r.json()
#             auctions = data.get('data', []) or data.get('auctions', []) or []
#             for auction in auctions:
#                 if auction.get('object_type') != 'vehicle':
#                     continue
#                 title = auction.get('title', 'Unknown Car')
#                 year_str = ''
#                 make = ''
#                 model = ''
#                 m = re.search(r'(\d{4})\s*([a-zA-Z0-9\-() ]+)\s+(.+)', title)
#                 if m:
#                     year_str = m.group(1)
#                     make = m.group(2).strip()
#                     model = m.group(3).strip()
#                 try:
#                     year = int(year_str)
#                 except:
#                     year = 0
#                 price_str = auction.get('last_bid', '0')
#                 auction_date = None
#                 try:
#                     auction_date = parse(auction['auction_end_at'])
#                 except:
#                     pass
#                 images = [auction.get('title_image', '')]
#                 url = f"https://www.tradinggarage.com/auctions/{auction.get('slug', '')}"
#                 reserve = 'No' if auction.get('no_reserve', False) else 'Yes'
#                 location = 'Online / Melbourne'
#                 description = ''
#                 odometer = ''
#                 lot = {
#                     'source': 'tradinggarage',
#                     'status': auction['status']['name'],
#                     'auction_id': auction['id'],
#                     'title': title,
#                     'year': year,
#                     'make': make,
#                     'model': model,
#                     'odometer': odometer,
#                     'price_range': parse_price(price_str),
#                     'auction_date': auction_date,
#                     'location': location,
#                     'images': images,
#                     'url': url,
#                     'description': description,
#                     'reserve': reserve,
#                     'scrape_time': datetime.now(timezone.utc)
#                 }
#                 if is_classic(lot):
#                     listings.append(lot)
#         except Exception as e:
#             pass
#     return listings

# def scrape_collectingcars():
#     listings = []
#     api_url = "https://dora.production.collecting.com/multi_search"
#     headers = {
#         'x-typesense-api-key': 'aKIufK0SfYHMRp9mUBkZPR7pksehPBZq',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
#         'Accept': 'application/json',
#         'Content-Type': 'application/json',
#         'Referer': 'https://collectingcars.com/',
#     }
#     base_payload = {
#         "searches": [
#             {
#                 "query_by": "title,productMake,vehicleMake,productYear,tags,lotType,driveSide,location,collectionId,modelId",
#                 "query_by_weights": "9,8,7,6,5,4,3,2,1,0",
#                 "text_match_type": "sum_score",
#                 "sort_by": "rank:asc",
#                 "highlight_full_fields": "*",
#                 "facet_by": "lotType, regionCode, countryCode, saleFormat, noReserve, isBoosted, productMake, vendorType, driveSide, listingStage, tags",
#                 "max_facet_values": 999,
#                 "facet_counts": True,
#                 "facet_stats": True,
#                 "facet_distribution": True,
#                 "facet_return_parent": True,
#                 "collection": "production_cars",
#                 "q": "*",
#                 "filter_by": "listingStage:=[`live`] && countryCode:=[`AU`] && regionCode:=[`APAC`]",
#                 "page": 1,
#                 "per_page": 50
#             }
#         ]
#     }
#     page = 1
#     while True:
#         base_payload["searches"][0]["page"] = page
#         try:
#             response = requests.post(api_url, headers=headers, json=base_payload, timeout=15)
#             if response.status_code != 200:
#                 break
#             data = response.json()
#             if "results" not in data or not data["results"]:
#                 break
#             result = data["results"][0]
#             hits = result.get("hits", [])
#             if not hits:
#                 break
#             for hit in hits:
#                 doc = hit.get("document", {})
#                 title = doc.get('title', 'Unknown Car')
#                 year_str = str(doc.get('productYear', ''))
#                 try:
#                     year = int(year_str)
#                 except:
#                     year = 0
#                 make = doc.get('productMake') or doc.get('vehicleMake', '')
#                 model = doc.get('model', '')
#                 price_str = doc.get('currentBid') or doc.get('buyNowPrice') or doc.get('estimate', 'TBA')
#                 lot = {
#                     'source': 'collectingcars',
#                     'status': 'live',
#                     'auction_id': doc.get('id'),
#                     'title': title,
#                     'year': year,
#                     'make': make,
#                     'model': model,
#                     'odometer': doc.get('odometer', '') or doc.get('mileage', ''),
#                     'price_range': parse_price(price_str),
#                     'auction_date': None,
#                     'location': doc.get('location', 'Australia'),
#                     'images': doc.get('images', []) or [doc.get('mainImage', '')],
#                     'url': f"https://collectingcars.com/for-sale/{doc.get('slug', '')}",
#                     'description': doc.get('description', ''),
#                     'reserve': 'No' if doc.get('noReserve', False) else 'Yes',
#                     'body_style': extract_body_style(doc.get('description', '')),
#                     'transmission': extract_transmission(doc.get('description', '')),
#                     'scrape_time': datetime.now(timezone.utc)
#                 }
#                 for date_key in ['endDate', 'auctionEndDate', 'closingDate']:
#                     if doc.get(date_key):
#                         try:
#                             lot['auction_date'] = parse(doc[date_key])
#                             break
#                         except:
#                             pass
#                 if not lot['make'] or not lot['model']:
#                     m = re.search(r'(\d{4})\s*([a-zA-Z]+)\s*(.+?)(?:\s+|$)', lot['title'])
#                     if m:
#                         lot['year'] = int(m.group(1))
#                         lot['make'] = m.group(2).capitalize()
#                         lot['model'] = m.group(3).strip().capitalize()
#                 if is_classic(lot):
#                     listings.append(lot)
#             page += 1
#             time.sleep(1.2)
#         except Exception as e:
#             break
#     return listings

# def scrape_carbids(base_url):
#     listings = []
#     # Browser strategy (omitted prints)
#     try:
#         driver = get_driver()
#         driver.set_window_size(1400, 900)
#         clean_url = base_url.split('#')[0]
#         driver.get(clean_url)
#         WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.wrapper.col-lg-4")))
#         last_height = driver.execute_script("return document.body.scrollHeight")
#         scroll_attempts = 0
#         max_scrolls = 12
#         while scroll_attempts < max_scrolls:
#             driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#             time.sleep(1.8 + scroll_attempts * 0.3)
#             new_height = driver.execute_script("return document.body.scrollHeight")
#             if new_height == last_height:
#                 scroll_attempts += 1
#             else:
#                 scroll_attempts = 0
#                 last_height = new_height
#         time.sleep(4)
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         driver.quit()
#         lot_divs = soup.select('div.wrapper.col-lg-4.col-md-6.col-sm-6.mobile-margin')
#         if lot_divs:
#             for div in lot_divs:
#                 lot = {}
#                 title_elem = div.select_one('h3.h5.p-b-10')
#                 title = title_elem.get_text(strip=True) if title_elem else ''
#                 m = re.match(r'(\d{1,2}/\d{4})\s+([^/]+?)\s+(.+?)(?:\s*\([^)]+\))?$', title)
#                 year_str = m.group(1).strip() if m else ''
#                 try:
#                     year = int(year_str.split('/')[-1])
#                 except:
#                     year = 0
#                 lot['year'] = year
#                 lot['make'] = m.group(2).strip() if m else ''
#                 lot['model'] = m.group(3).strip() if m else title
#                 def get_next_text(icon_class):
#                     i = div.select_one(f'i.{icon_class.replace(" ", ".")}')
#                     if i:
#                         txt = i.next_sibling
#                         return txt.strip() if txt and isinstance(txt, str) else ''
#                     return ''
#                 lot['odometer'] = get_next_text('fas fa-tachometer-alt')
#                 lot['transmission'] = get_next_text('fas fa-cogs')
#                 lot['fuel_type'] = get_next_text('fas fa-gas-pump')
#                 lot['engine'] = get_next_text('fas fa-oil-can')
#                 price_big = div.select_one('span.h2')
#                 price_str = price_big.get_text(strip=True) if price_big else ''
#                 if not price_str:
#                     start_price = div.select_one('span.h4')
#                     price_str = start_price.get_text(strip=True) if start_price else 'Auction TBA'
#                 lot['price_range'] = parse_price(price_str)
#                 countdown = div.select_one('span[id^="closingCountdownTextGrid"]')
#                 calendar_span = div.select_one('span[id^="closingTimeGrid"]')
#                 calendar_text = calendar_span.get_text(strip=True).strip('()[] ') if calendar_span else ''
#                 try:
#                     lot['auction_date'] = parse(calendar_text)
#                 except:
#                     lot['auction_date'] = None
#                 loc_div = div.select_one('div.bgm-white.p-5.m-r-5.p-l-15.p-r-15')
#                 city = loc_div.get_text(strip=True) if loc_div else ''
#                 state_span = div.select_one('span.p-5[style*="float: right"]')
#                 state = state_span.get_text(strip=True) if state_span else ''
#                 lot['location'] = f"{city} {state}".strip()
#                 ref = div.select_one('mark.h5.p-t-5.p-b-5.p-r-10.p-l-10')
#                 lot['reference_number'] = ref.get_text(strip=True) if ref else ''
#                 imgs = div.select('img.img-responsive')
#                 lot['images'] = []
#                 for img in imgs:
#                     src = img.get('ng-src') or img.get('src') or ''
#                     if src:
#                         if src.startswith('//'): src = 'https:' + src
#                         lot['images'].append(src)
#                 a = div.select_one('a[ng-href]')
#                 lot['url'] = a['ng-href'] if a else clean_url
#                 lot['description'] = ' '.join(filter(None, [lot.get('odometer'), lot.get('transmission'), lot.get('fuel_type'), lot.get('engine')]))
#                 lot['reserve'] = 'Yes'
#                 lot['body_style'] = extract_body_style(lot['description'])
#                 lot['transmission'] = lot.get('transmission', extract_transmission(lot['description']))
#                 lot['scrape_time'] = datetime.utcnow()
#                 lot['source'] = 'carbids'
#                 if is_classic(lot):
#                     listings.append(lot)
#             if listings:
#                 return listings
#     except Exception as e:
#         pass

#     # API fallback
#     try:
#         s = requests.Session()
#         s.headers.update({
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
#             'Accept': 'application/json, text/plain, */*',
#             'X-Requested-With': 'XMLHttpRequest',
#         })
#         r = s.get(base_url.split('#')[0])
#         soup_init = BeautifulSoup(r.text, 'html.parser')
#         token_input = soup_init.find('input', {'name': '__RequestVerificationToken'})
#         if token_input:
#             s.headers['__RequestVerificationToken'] = token_input['value']
#         page = 0
#         while True:
#             payload = {
#                 "top": 96,
#                 "skip": page * 96,
#                 "sort": {"aucClose": "asc"},
#                 "tagName": "Unique and Classic Car Auctions",
#                 "filter": {"Display": True}
#             }
#             resp = s.post("https://carbids.com.au/Search/Tags", json=payload, timeout=20)
#             if resp.status_code != 200:
#                 break
#             data = resp.json()
#             auctions = data.get('auctions', [])
#             if not auctions:
#                 break
#             for auc in auctions:
#                 year_str = str(auc.get('aucYear', ''))
#                 try:
#                     year = int(year_str)
#                 except:
#                     year = 0
#                 price_str = auc.get('aucCurrentBid', 0) or 'Auction TBA'
#                 lot = {
#                     'source': 'carbids',
#                     'url': auc.get('AucDetailsUrlLink', base_url),
#                     'reference_number': auc.get('aucReferenceNo', ''),
#                     'year': year,
#                     'make': auc.get('aucMake', ''),
#                     'model': auc.get('aucModel', ''),
#                     'odometer': auc.get('aucOdometer', ''),
#                     'transmission': auc.get('aucTransmission', ''),
#                     'fuel_type': auc.get('aucFuelType', ''),
#                     'engine': f"{auc.get('aucCapacity','')} {auc.get('aucCylinder','')} cyl",
#                     'price_range': parse_price(price_str),
#                     'location': f"{auc.get('aucCity','')} {auc.get('aucState','')}".strip(),
#                     'images': [auc.get('aucCarsThumbnailUrl')] + (auc.get('aucMediumThumbnailUrlList', []) or []),
#                     'auction_date': parse(auc['aucCloseUtc']) if auc.get('aucCloseUtc') else None,
#                     'description': auc.get('aucTitle', ''),
#                     'reserve': 'Yes',
#                     'body_style': extract_body_style(auc.get('aucTitle', '')),
#                     'scrape_time': datetime.utcnow(),
#                 }
#                 if is_classic(lot):
#                     listings.append(lot)
#             page += 1
#             time.sleep(1.4)
#     except Exception as e:
#         pass
#     return listings

# def scrape_bennetts(base_url):
#     pages = [base_url, base_url + '/off-site.php']
#     all_listings = []
#     for page_url in pages:
#         try:
#             driver = get_driver()
#             driver.get(page_url)
#             soup = BeautifulSoup(driver.page_source, 'html.parser')
#             driver.quit()
#             sitename = soup.find('div', id='sitename')
#             h3 = sitename.find('h3') if sitename else None
#             auction_text = h3.text.strip() if h3 else ''
#             date_match = re.search(r'(\d{1,2}[ST|ND|RD|TH]{0,2} \w+ \d{4})', auction_text.upper())
#             time_match = re.search(r'@ (\d{1,2}[AP]M)', auction_text.upper())
#             auction_date_str = ''
#             if date_match:
#                 date_str = re.sub(r'([ST|ND|RD|TH])', '', date_match.group(1))
#                 auction_date_str += date_str
#             if time_match:
#                 auction_date_str += ' ' + time_match.group(1)
#             auction_date = None
#             try:
#                 auction_date = parse(auction_date_str)
#             except:
#                 pass
#             sections = soup.find_all('div', class_='clear')
#             for section in sections:
#                 column = section.find('div', class_='column column-600 column-left')
#                 if column:
#                     h3_cat = column.find('h3')
#                     category = h3_cat.text.strip() if h3_cat else ''
#                     table = column.find('table')
#                     if table:
#                         tbody = table.find('tbody')
#                         trs = tbody.find_all('tr') if tbody else table.find_all('tr')
#                         for tr in trs[1:]:
#                             tds = tr.find_all('td')
#                             if len(tds) == 7:
#                                 photo_td = tds[0]
#                                 a = photo_td.find('a')
#                                 detail_url = base_url + '/' + a['href'].lstrip('/') if a else ''
#                                 img = photo_td.find('img')
#                                 image_src = base_url + '/' + img['src'].lstrip('/') if img and img['src'].startswith('images') else img['src']
#                                 make = tds[1].text.strip()
#                                 stock_model = tds[2].text.strip()
#                                 parts = stock_model.split('/')
#                                 stock_ref = parts[0].strip() if parts else ''
#                                 model = parts[1].strip() if len(parts) > 1 else stock_model
#                                 year_str = tds[3].text.strip()
#                                 try:
#                                     year = int(year_str)
#                                 except:
#                                     year = 0
#                                 options = tds[4].text.strip()
#                                 location_td = tds[5]
#                                 location = location_td.text.strip().replace('\n', '').replace('br /', '')
#                                 lot = {
#                                     'source': 'bennettsclassicauctions',
#                                     'make': make,
#                                     'model': model,
#                                     'year': year,
#                                     'price_range': None,
#                                     'auction_date': auction_date,
#                                     'location': location,
#                                     'images': [image_src] if image_src else [],
#                                     'url': detail_url,
#                                     'description': options,
#                                     'reserve': 'Yes',
#                                     'body_style': extract_body_style(options),
#                                     'transmission': extract_transmission(options),
#                                     'scrape_time': datetime.now()
#                                 }
#                                 if is_classic(lot):
#                                     all_listings.append(lot)
#         except Exception as e:
#             pass
#     return all_listings

# def scrape_burnsandco(base_url):
#     pages = [base_url + '/current-auctions/', base_url + '/upcoming-auctions/']
#     all_listings = []
#     for page_url in pages:
#         try:
#             driver = get_driver()
#             driver.get(page_url)
#             soup = BeautifulSoup(driver.page_source, 'html.parser')
#             driver.quit()
#             articles = soup.find_all('article', class_='regular masonry-blog-item')
#             for article in articles:
#                 img_link = article.find('a', class_='img-link')
#                 detail_url = img_link['href'] if img_link else ''
#                 img = img_link.find('img') if img_link else None
#                 image_src = img['src'] if img else ''
#                 meta_category = article.find('span', class_='meta-category')
#                 category = meta_category.text.strip() if meta_category else ''
#                 date_item = article.find('span', class_='date-item')
#                 auction_date_str = date_item.text.strip() if date_item else ''
#                 auction_date = None
#                 try:
#                     auction_date = parse(auction_date_str)
#                 except:
#                     pass
#                 title_a = article.find('h3', class_='title').find('a') if article.find('h3', class_='title') else None
#                 title = title_a.text.strip() if title_a else ''
#                 excerpt = article.find('div', class_='excerpt').text.strip() if article.find('div', class_='excerpt') else ''
#                 place = article.find('p', class_='place').text.strip() if article.find('p', class_='place') else ''
#                 bid_links = article.find_all('p', class_='registration_bidding_link')
#                 for bid_p in bid_links:
#                     bid_a = bid_p.find('a')
#                     bid_url = bid_a['href'] if bid_a else ''
#                     catalogue_lots = scrape_catalogue(bid_url)
#                     for cat_lot in catalogue_lots:
#                         cat_lot['auction_date'] = auction_date or cat_lot.get('auction_date')
#                         cat_lot['location'] = place or cat_lot.get('location')
#                         cat_lot['source'] = 'burnsandco'
#                         all_listings.append(cat_lot)
#         except Exception as e:
#             pass
#     return all_listings

# def scrape_catalogue(catalogue_url):
#     listings = []
#     try:
#         driver = get_driver()
#         driver.get(catalogue_url)
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         driver.quit()
#         lot_items = soup.find_all('div', class_='lot-item')  # Placeholder, adjust based on site inspection
#         for item in lot_items:
#             lot_number = item.find('span', class_='lot-number').text.strip() if item.find('span', class_='lot-number') else ''
#             desc = item.find('div', class_='lot-description').text.strip() if item.find('div', class_='lot-description') else ''
#             match = re.match(r'(\d{4})? ?(.*?) (.*)', desc)
#             year_str = match.group(1) if match and match.group(1) else ''
#             try:
#                 year = int(year_str)
#             except:
#                 year = 0
#             make = match.group(2) if match else ''
#             model = match.group(3) if match else desc
#             images = [img['src'] for img in item.find_all('img')]
#             detail_a = item.find('a', class_='lot-detail')
#             detail_url = catalogue_url + detail_a['href'] if detail_a else ''
#             current_bid = item.find('span', class_='current-bid').text.strip() if item.find('span', class_='current-bid') else ''
#             lot = {
#                 'lot_number': lot_number,
#                 'make': make,
#                 'model': model,
#                 'year': year,
#                 'price_range': parse_price(current_bid),
#                 'auction_date': None,
#                 'location': None,
#                 'images': images,
#                 'url': detail_url,
#                 'description': desc,
#                 'reserve': 'Yes',
#                 'body_style': extract_body_style(desc),
#                 'transmission': extract_transmission(desc),
#                 'scrape_time': datetime.now()
#             }
#             if is_classic(lot):
#                 listings.append(lot)
#     except Exception as e:
#         pass
#     return listings

# def parse_lot(item, url):
#     try:
#         description = item.find('p', class_='desc') or item.find('div', class_='description')
#         description_text = description.text.strip() if description else ''
#         year_elem = item.find('span', class_='year') or item.find('h3')
#         year_str = year_elem.text.strip() if year_elem else '0'
#         try:
#             year = int(year_str)
#         except:
#             year = 0
#         make_elem = item.find('span', class_='make') or item.find('h2')
#         model_elem = item.find('span', class_='model')
#         price_elem = item.find('span', class_='estimate') or item.find('div', class_='price')
#         price_str = price_elem.text.strip() if price_elem else None
#         date_elem = item.find('span', class_='date')
#         location_elem = item.find('span', class_='location')
#         link_elem = item.find('a', class_='lot-link') or item.find('a')
#         lot = {
#             'make': make_elem.text.strip() if make_elem else None,
#             'model': model_elem.text.strip() if model_elem else None,
#             'year': year,
#             'price_range': parse_price(price_str),
#             'auction_date': parse_date(date_elem.text.strip()) if date_elem else None,
#             'location': location_elem.text.strip() if location_elem else 'Online',
#             'images': [img['src'] for img in item.find_all('img', class_='thumbnail')][:6],
#             'url': link_elem['href'] if link_elem else url,
#             'description': description_text,
#             'reserve': 'No' if 'no reserve' in description_text.lower() else 'Yes',
#             'body_style': extract_body_style(description_text),
#             'transmission': extract_transmission(description_text),
#             'scrape_time': datetime.now()
#         }
#         return lot
#     except:
#         return None

# def parse_date(date_str):
#     try:
#         return parse(date_str)
#     except:
#         return None

# def extract_body_style(desc):
#     lower_desc = desc.lower()
#     styles = ['coupe', 'convertible', 'sedan', 'wagon', 'ute', 'truck']
#     for style in styles:
#         if style in lower_desc:
#             return style.capitalize()
#     return None

# def extract_transmission(desc):
#     lower_desc = desc.lower()
#     if 'manual' in lower_desc:
#         return 'Manual'
#     if 'auto' in lower_desc or 'automatic' in lower_desc:
#         return 'Automatic'
#     return None

# def is_classic(lot):
#     try:
#         year = int(lot['year'])
#     except:
#         year = 0
#     text = (lot['description'].lower() if lot['description'] else '') + ' ' + (lot['title'].lower() if lot['title'] else '')
#     return year < 1990 or any(word in text for word in ['collector', 'classic', 'future classic', 'modern classic', 'muscle'])

# def normalize_auction_date(ad):
#     if not ad:
#         return None
#     if isinstance(ad, datetime):
#         return ad
#     if isinstance(ad, str):
#         try:
#             return parse(ad)
#         except:
#             return None
#     try:
#         return parse(str(ad))
#     except:
#         return None

# def extract_provenance(desc):
#     # Simple placeholder: return full desc or parse key phrases
#     return desc

# def build_query(params):
#     query = {}
#     if 'make' in params:
#         query['make'] = {'$regex': params['make'], '$options': 'i'}
#     if 'model' in params:
#         query['model'] = {'$regex': params['model'], '$options': 'i'}
#     if 'variant' in params:
#         query['description'] = {'$regex': params['variant'], '$options': 'i'}  # Assume variant in desc
#     if 'year_min' in params or 'year_max' in params:
#         query['year'] = {}
#         if 'year_min' in params:
#             query['year']['$gte'] = int(params['year_min'])
#         if 'year_max' in params:
#             query['year']['$lte'] = int(params['year_max'])
#     if 'price_min' in params or 'price_max' in params:
#         if 'price_min' in params:
#             query['price_range.low'] = {'$gte': int(params['price_min'])}
#         if 'price_max' in params:
#             query['price_range.high'] = {'$lte': int(params['price_max'])}
#     if 'state' in params:
#         query['location'] = {'$regex': params['state'], '$options': 'i'}
#     if 'auction_house' in params:
#         query['source'] = {'$regex': params['auction_house'], '$options': 'i'}
#     if 'no_reserve' in params and params['no_reserve']:
#         query['reserve'] = 'No'
#     if 'body_style' in params:
#         query['body_style'] = {'$regex': params['body_style'], '$options': 'i'}
#     if 'transmission' in params:
#         query['transmission'] = {'$regex': params['transmission'], '$options': 'i'}
#     if 'newly_added' in params:
#         try:
#             hours = int(params['newly_added'][:-1])
#             time_ago = datetime.now() - timedelta(hours=hours)
#             query['scrape_time'] = {'$gte': time_ago}
#         except:
#             pass
#     return query

# def scrape_all():
#     all_lots = []
#     scrape_start = datetime.utcnow()
#     for source in SOURCES:
#         lots = scrape_site(source)
#         all_lots.extend(lots)
    
#     for lot in all_lots:
#         lot['scrape_time'] = datetime.utcnow()
#         lot['auction_date'] = normalize_auction_date(lot.get('auction_date'))
#         if not lot.get('url'):
#             lot['url'] = f"{lot.get('source','unknown')}/{uuid.uuid4()}"
#         lots_collection.update_one(
#             {'url': lot['url']},
#             {'$set': lot, '$setOnInsert': {'first_scraped': scrape_start}},
#             upsert=True
#         )
    
#     now = datetime.now()
#     ended = lots_collection.find({'auction_date': {'$lt': now}})
#     for end in list(ended):
#         house = end['source']
#         prem = house_premiums.get(house, 0.15)
#         hammer = end.get('price_range', {}).get('high', 0)  # Placeholder for final hammer
#         total = hammer * (1 + prem)
#         sold_doc = dict(end)
#         sold_doc['hammer_price'] = hammer
#         sold_doc['buyers_premium'] = prem * 100
#         sold_doc['total_price'] = total
#         sold_collection.insert_one(sold_doc)
#         lots_collection.delete_one({'_id': end['_id']})
    
#     two_years_ago = now - timedelta(days=730)
#     sold_collection.delete_many({'auction_date': {'$lt': two_years_ago}})
    
#     check_alerts(scrape_start)

# def check_alerts(scrape_start):
#     for saved in saved_searches_collection.find():
#         user_id = saved['user_id']
#         params = {k: v for k, v in saved.items() if k not in ['_id', 'user_id']}
#         query = build_query(params)
#         matches = lots_collection.find({**query, 'first_scraped': {'$gte': scrape_start}})
#         match_list = list(matches)
#         if match_list:
#             titles = [m.get('title', m.get('make', '') + ' ' + m.get('model', '')) for m in match_list]
#             message = f"New matching cars added: {', '.join(titles)}\nView at AusClassicAuctions.com.au"
#             send_alert(user_id, message)

# # Scheduler
# scheduler = BackgroundScheduler()
# scheduler.add_job(scrape_all, 'interval', hours=4)
# scheduler.start()

# @app.route('/api/scrape', methods=['POST'])
# @swag_from({
#     'tags': ['Admin'],
#     'summary': 'Trigger manual scrape',
#     'security': [{'Bearer': []}],
#     'responses': {
#         '200': {'description': 'Scraping completed'}
#     }
# })
# # @jwt_required()
# def manual_scrape():
#     scrape_all()
#     return jsonify({'message': 'Scraping completed'})

# @app.route('/api/register', methods=['POST'])
# @swag_from({
#     'tags': ['Users'],
#     'summary': 'Register a new user',
#     'parameters': [
#         {
#             'name': 'body',
#             'in': 'body',
#             'required': True,
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'email': {'type': 'string'},
#                     'password': {'type': 'string'}
#                 },
#                 'required': ['email', 'password']
#             }
#         }
#     ],
#     'responses': {
#         '200': {'description': 'User registered'},
#         '400': {'description': 'User already exists'}
#     }
# })
# def register():
#     data = request.json
#     email = data['email']
#     password = data['password']  # Hash in production
#     if users_collection.find_one({'email': email}):
#         return jsonify({'error': 'User exists'}), 400
#     user_id = users_collection.insert_one({'email': email, 'password': password}).inserted_id
#     user = User(str(user_id), email)
#     login_user(user)
#     return jsonify({'message': 'Registered'})

# @app.route('/api/login', methods=['POST'])
# @swag_from({
#     'tags': ['Users'],
#     'summary': 'Login user',
#     'parameters': [
#         {
#             'name': 'body',
#             'in': 'body',
#             'required': True,
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'email': {'type': 'string'},
#                     'password': {'type': 'string'}
#                 },
#                 'required': ['email', 'password']
#             }
#         }
#     ],
#     'responses': {
#         '200': {'description': 'Login successful, token returned'},
#         '401': {'description': 'Invalid credentials'}
#     }
# })
# def login():
#     data = request.json
#     email = data['email']
#     password = data['password']
#     user_doc = users_collection.find_one({'email': email, 'password': password})
#     if user_doc:
#         user = User(str(user_doc['_id']), email)
#         login_user(user)
#         access_token = create_access_token(identity=str(user_doc['_id']))
#         return jsonify({'token': access_token})
#     return jsonify({'error': 'Invalid credentials'}), 401

# @app.route('/api/logout')
# @swag_from({
#     'tags': ['Users'],
#     'summary': 'Logout user',
#     'responses': {
#         '200': {'description': 'Logged out'}
#     }
# })
# @login_required
# def logout():
#     logout_user()
#     return jsonify({'message': 'Logged out'})

# @app.route('/api/calendar', methods=['GET'])
# @swag_from({
#     'tags': ['Auctions'],
#     'summary': 'Get auction calendar',
#     'parameters': [
#         {'name': 'state', 'in': 'query', 'type': 'string', 'description': 'Filter by state'},
#         {'name': 'month', 'in': 'query', 'type': 'string', 'description': 'Filter by month (YYYY-MM)'},
#         {'name': 'auction_house', 'in': 'query', 'type': 'string', 'description': 'Filter by auction house'},
#         {'name': 'online_only', 'in': 'query', 'type': 'boolean', 'description': 'Filter online only'}
#     ],
#     'responses': {
#         '200': {'description': 'List of upcoming auctions'}
#     }
# })
# def calendar():
#     now = datetime.now()
#     match = {'auction_date': {'$gte': now, '$lt': now + timedelta(days=90)}}
#     if state := request.args.get('state'):
#         match['location'] = {'$regex': state, '$options': 'i'}
#     if month := request.args.get('month'):
#         try:
#             start = datetime.strptime(month + '-01', '%Y-%m-%d')
#             end = (start.replace(month=start.month % 12 + 1) if start.month == 12 else start.replace(month=start.month + 1)) - timedelta(days=1)
#             match['auction_date'] = {'$gte': start, '$lte': end}
#         except:
#             pass
#     if auction_house := request.args.get('auction_house'):
#         match['source'] = {'$regex': auction_house, '$options': 'i'}
#     if request.args.get('online_only') == 'true':
#         match['location'] = 'Online'
    
#     pipeline = [
#         {'$match': match},
#         {'$group': {'_id': {'date': '$auction_date', 'source': '$source', 'location': '$location'}, 'num_lots': {'$sum': 1}}},
#         {'$sort': {'_id.date': 1}}
#     ]
#     results = list(lots_collection.aggregate(pipeline))
#     formatted = [
#         {
#             'date': r['_id']['date'],
#             'house': r['_id']['source'],
#             'location': r['_id']['location'],
#             'num_lots': r['num_lots']
#         } for r in results
#     ]
#     return jsonify(formatted)

# @app.route('/api/search', methods=['GET'])
# @swag_from({
#     'tags': ['Auctions'],
#     'summary': 'Search for lots',
#     'parameters': [
#         {'name': 'make', 'in': 'query', 'type': 'string'},
#         {'name': 'model', 'in': 'query', 'type': 'string'},
#         {'name': 'variant', 'in': 'query', 'type': 'string'},
#         {'name': 'year_min', 'in': 'query', 'type': 'integer'},
#         {'name': 'year_max', 'in': 'query', 'type': 'integer'},
#         {'name': 'price_min', 'in': 'query', 'type': 'integer'},
#         {'name': 'price_max', 'in': 'query', 'type': 'integer'},
#         {'name': 'state', 'in': 'query', 'type': 'string'},
#         {'name': 'auction_house', 'in': 'query', 'type': 'string'},
#         {'name': 'no_reserve', 'in': 'query', 'type': 'boolean'},
#         {'name': 'body_style', 'in': 'query', 'type': 'string'},
#         {'name': 'transmission', 'in': 'query', 'type': 'string'},
#         {'name': 'newly_added', 'in': 'query', 'type': 'string', 'description': 'e.g., 24h'},
#         {'name': 'sort', 'in': 'query', 'type': 'string', 'description': 'e.g., auction_date asc'}
#     ],
#     'responses': {
#         '200': {'description': 'Search results'}
#     }
# })
# def search():
#     params = request.args.to_dict()
#     query = build_query(params)
#     sort_str = params.get('sort', 'auction_date asc').split()
#     sort_field = sort_str[0]
#     sort_dir = 1 if len(sort_str) > 1 and sort_str[1].lower() == 'asc' else -1
#     results = lots_collection.find(query).sort(sort_field, sort_dir)
#     return jsonify([dict(result, **{'_id': str(result['_id'])}) for result in results])

# @app.route('/api/lot/<lot_id>', methods=['GET'])
# @swag_from({
#     'tags': ['Auctions'],
#     'summary': 'Get individual lot details',
#     'parameters': [
#         {'name': 'lot_id', 'in': 'path', 'type': 'string', 'required': True}
#     ],
#     'responses': {
#         '200': {'description': 'Lot details'},
#         '404': {'description': 'Not found'}
#     }
# })
# def get_lot(lot_id):
#     lot = lots_collection.find_one({'_id': ObjectId(lot_id)})
#     if not lot:
#         return jsonify({'error': 'Not found'}), 404
#     lot['_id'] = str(lot['_id'])
#     lot['provenance'] = extract_provenance(lot.get('description', ''))
#     related = sold_collection.find({
#         'make': lot['make'],
#         'model': lot['model'],
#         'year': lot['year']
#     }).limit(5)
#     lot['related'] = [dict(rel, **{'_id': str(rel['_id'])}) for rel in related]
#     return jsonify(lot)

# @app.route('/api/watchlist', methods=['GET', 'POST'])
# @swag_from({
#     'tags': ['Users'],
#     'summary': 'Manage watchlist',
#     'security': [{'Bearer': []}],
#     'parameters': [
#         {
#             'name': 'body',
#             'in': 'body',
#             'required': False,
#             'schema': {
#                 'type': 'object',
#                 'properties': {
#                     'lot_id': {'type': 'string'}
#                 }
#             }
#         }
#     ],
#     'responses': {
#         '200': {'description': 'Watchlist or added message'}
#     }
# })
# @jwt_required()
# def watchlist():
#     user_id = get_jwt_identity()
#     if request.method == 'POST':
#         lot_id = request.json.get('lot_id')
#         watchlists_collection.update_one(
#             {'user_id': user_id},
#             {'$addToSet': {'lots': ObjectId(lot_id)}},
#             upsert=True
#         )
#         return jsonify({'message': 'Added'})
    
#     watch = watchlists_collection.find_one({'user_id': user_id})
#     if watch:
#         lot_ids = watch['lots']
#         upcoming = list(lots_collection.find({'_id': {'$in': lot_ids}}))
#         sold = list(sold_collection.find({'_id': {'$in': lot_ids}}))
#         all_lots = upcoming + sold
#         now = datetime.now()
#         for l in all_lots:
#             l['_id'] = str(l['_id'])
#             if l.get('auction_date', now) < now:
#                 l['status'] = 'sold'
#             else:
#                 l['status'] = 'upcoming'
#         return jsonify(all_lots)
#     return jsonify([])

# @app.route('/api/saved_searches', methods=['GET', 'POST'])
# @swag_from({
#     'tags': ['Users'],
#     'summary': 'Manage saved searches',
#     'security': [{'Bearer': []}],
#     'responses': {
#         '200': {'description': 'Saved searches or saved message'}
#     }
# })
# @jwt_required()
# def saved_searches():
#     user_id = get_jwt_identity()
#     if request.method == 'POST':
#         search_params = request.json
#         saved_searches_collection.insert_one({'user_id': user_id, **search_params})
#         return jsonify({'message': 'Saved'})
    
#     searches = saved_searches_collection.find({'user_id': user_id})
#     return jsonify([dict(s, **{'_id': str(s['_id'])}) for s in searches])

# def send_alert(user_id, message):
#     user = users_collection.find_one({'_id': ObjectId(user_id)})
#     if user:
#         smtp_server = os.getenv('SMTP_SERVER')
#         smtp_port = int(os.getenv('SMTP_PORT', 587))
#         sender = os.getenv('SENDER_EMAIL')
#         password = os.getenv('SENDER_PASSWORD')
        
#         msg = MIMEText(message)
#         msg['Subject'] = 'Auction Alert'
#         msg['From'] = sender
#         msg['To'] = user['email']
        
#         with smtplib.SMTP(smtp_server, smtp_port) as server:
#             server.starttls()
#             server.login(sender, password)
#             server.sendmail(sender, user['email'], msg.as_string())

# @app.route('/api/sold', methods=['GET'])
# @swag_from({
#     'tags': ['Auctions'],
#     'summary': 'Get sold prices archive',
#     'parameters': [
#         {'name': 'make', 'in': 'query', 'type': 'string'},
#         {'name': 'model', 'in': 'query', 'type': 'string'},
#         {'name': 'year', 'in': 'query', 'type': 'integer'}
#     ],
#     'responses': {
#         '200': {'description': 'Sold lots'}
#     }
# })
# def sold():
#     params = request.args.to_dict()
#     if 'year' in params:
#         params['year'] = int(params['year'])
#     query = build_query(params)
#     results = sold_collection.find(query).sort('auction_date', -1)
#     return jsonify([dict(r, **{'_id': str(r['_id'])}) for r in results])

# @app.route('/api/market_pulse', methods=['GET'])
# @swag_from({
#     'tags': ['Auctions'],
#     'summary': 'Get market pulse data',
#     'responses': {
#         '200': {'description': 'Top sales and risers'}
#     }
# })
# def market_pulse():
#     now = datetime.now()
#     month_start = now - timedelta(days=30)
#     top_sales = sold_collection.find({'auction_date': {'$gte': month_start}}).sort('total_price', -1).limit(10)
#     top_sales_list = [dict(s, **{'_id': str(s['_id'])}) for s in top_sales]
    
#     pipeline = [
#         {'$match': {'auction_date': {'$gte': month_start}}},
#         {'$group': {'_id': {'make': '$make', 'model': '$model'}, 'avg_price': {'$avg': '$total_price'}, 'count': {'$sum': 1}}},
#         {'$sort': {'avg_price': -1}},
#         {'$limit': 10}
#     ]
#     risers = list(sold_collection.aggregate(pipeline))
#     return jsonify({'top_sales': top_sales_list, 'risers': risers})

# @app.route('/api/on_the_block', methods=['GET'])
# @swag_from({
#     'tags': ['Auctions'],
#     'summary': 'Get lots closing soon',
#     'responses': {
#         '200': {'description': 'Live lots'}
#     }
# })
# def on_the_block():
#     now = datetime.now()
#     two_hours = now + timedelta(hours=2)
#     live = lots_collection.find({'auction_date': {'$gte': now, '$lt': two_hours}})
#     return jsonify([dict(l, **{'_id': str(l['_id'])}) for l in live])

# @app.route('/api/auction_houses', methods=['GET'])
# @swag_from({
#     'tags': ['Auctions'],
#     'summary': 'Get auction houses directory',
#     'responses': {
#         '200': {'description': 'List of auction houses'}
#     }
# })
# def auction_houses():
#     now = datetime.now()
#     houses = list(lots_collection.aggregate([{'$group': {'_id': '$source', 'upcoming': {'$sum': 1}}}]))
#     directory = []
#     for h in houses:
#         name = h['_id']
#         premium = house_premiums.get(name, 0.15) * 100
#         directory.append({
#             'name': name,
#             'upcoming': h['upcoming'],
#             'buyers_premium': f"{premium}%"
#         })
#     return jsonify(directory)

# # Initial scrape
# # scrape_all()

# if __name__ == '__main__':
#     app.run(debug=False)
import os
import datetime
from math import ceil
from datetime import timedelta
import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify, session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from pymongo import MongoClient
from apscheduler.schedulers.background import BackgroundScheduler
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
from flasgger import Swagger, swag_from
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dateutil.parser import parse
from datetime import datetime, timezone
from bson.objectid import ObjectId
import re
import time
import uuid

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your_secret_key')
CORS(app)

# JWT Setup
jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret')

# Login Manager
login_manager = LoginManager()
login_manager.init_app(app)

# Swagger Setup
swagger = Swagger(app, template={
    "swagger": "2.0",
    "info": {
        "title": "AusClassicAuctions API",
        "description": "API for Australian Classic Car Auctions Aggregator",
        "version": "1.0.0"
    },
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer {token}'"
        }
    }
})

# MongoDB Setup
client = MongoClient(os.getenv('MONGO_URI', 'mongodb://localhost:27017/'))
db = client['ausclassicauctions']
lots_collection = db['lots']  # Current and upcoming lots
sold_collection = db['sold']  # Sold archive
users_collection = db['users']
watchlists_collection = db['watchlists']
saved_searches_collection = db['saved_searches']

# Create indexes for fast queries
lots_collection.create_index([('auction_date', 1), ('source', 1), ('make', 1), ('model', 1), ('location', 1), ('scrape_time', 1)])
sold_collection.create_index([('auction_date', 1), ('source', 1), ('make', 1), ('model', 1), ('location', 1)])

# User Model
class User(UserMixin):
    def __init__(self, id, email):
        self.id = id
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    user = users_collection.find_one({'_id': ObjectId(user_id)})
    if user:
        return User(user['_id'], user['email'])
    return None

# Buyers Premiums (approximate percentages, update as needed)
house_premiums = {
    'tradinggarage': 0.12,
    'carbids': 0.15,
    'collectingcars': 0.06,
    'bennettsclassicauctions': 0.125,
    'burnsandco': 0.15,
    'lloydsonline': 0.20,
    'seven82motors': 0.10,
    'chicaneauctions': 0.12,
    'doningtonauctions': 0.125
}

# Scraping Sources (uncommented all for full coverage)
SOURCES = [
    {'url': 'https://www.tradinggarage.com', 'name': 'tradinggarage'},
    {'url': 'https://collectingcars.com/buy?refinementList%5BlistingStage%5D%5B0%5D=live&refinementList%5BregionCode%5D%5B0%5D=APAC&refinementList%5BcountryCode%5D%5B0%5D=AU', 'name': 'collectingcars'},
    {'url': 'https://www.bennettsclassicauctions.com.au', 'name': 'bennettsclassicauctions'},

    {'url': 'https://carbids.com.au/t/unique-and-classic-car-auctions#!?page=1&count=96&filter%5BDisplay%5D=true', 'name': 'carbids'},
     {'url': 'https://www.lloydsonline.com.au/AuctionLots.aspx?stype=0&stypeid=0&cid=410&smode=0', 'name': 'lloydsonline'},
        {'url': 'https://www.chicaneauctions.com.au', 'name': 'chicaneauctions'},

   
    {'url': 'https://www.seven82motors.com.au', 'name': 'seven82motors'},

    # {'url': 'https://www.doningtonauctions.com.au', 'name': 'doningtonauctions'},
        # {'url': 'https://burnsandcoauctions.com.au', 'name': 'burnsandco'},
]

# def get_driver():
#     options = Options()
#     options.headless = True
#     service = Service(ChromeDriverManager().install())
#     return webdriver.Chrome(service=service, options=options)

def get_driver():
    options = Options()
    options.add_argument('--headless')  # Modern way to set headless mode
    options.add_argument('--disable-gpu')  # Often needed for headless
    options.add_argument('--window-size=1920,1080')  # Avoids some rendering issues

    if platform.system() == 'Linux':
        options.add_argument('--no-sandbox')  # Critical for Linux servers
        options.add_argument('--disable-dev-shm-usage')  # Handles small /dev/shm in containers
        options.add_argument('--remote-debugging-port=9222')  # For stability in some envs

    service = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=service, options=options)

def parse_price(price_str):
    if not price_str or price_str == 'TBA':
        return None
    try:
        if isinstance(price_str, (int, float)):
            val = float(price_str)
            return {'low': val, 'high': val}
        price_str = str(price_str).replace(',', '').replace('$', '').strip()
        m = re.match(r'(\d+(?:\.\d+)?)\s*-\s*(\d+(?:\.\d+)?)', price_str)
        if m:
            return {'low': float(m.group(1)), 'high': float(m.group(2))}
        m = re.match(r'(\d+(?:\.\d+)?)', price_str)
        if m:
            val = float(m.group(1))
            return {'low': val, 'high': val}
    except:
        pass
    return None

def scrape_site(source):
    url = source['url']
    name = source['name']
    if name == 'bennettsclassicauctions':
        return scrape_bennetts(url)
    elif name == 'burnsandco':
        return scrape_burnsandco(url)
    elif name == 'carbids':
        return scrape_carbids(url)
    elif name == 'tradinggarage':
        return scrape_tradinggarage(url)    
    elif name == 'collectingcars':
        return scrape_collectingcars()
    elif name == 'lloydsonline':
        return scrape_lloydsonline()
    elif name == 'chicaneauctions':
        return scrape_chicane()
    elif name == 'seven82motors':
        return scrape_seven82motors()
    else:
        # Generic scraper for other sites
        try:
            driver = get_driver()
            driver.get(url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.quit()

            listings = []
            item_class = 'auction-item'  # Adjust per site as needed
            for item in soup.find_all('div', class_=item_class):
                lot = parse_lot(item, url)
                if lot and is_classic(lot):
                    lot['source'] = name
                    listings.append(lot)
            return listings
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            return []

def scrape_tradinggarage(base_url="https://www.tradinggarage.com"):
    listings = []
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Referer': 'https://www.tradinggarage.com/',
    })

    endpoints = {
        'live': 'https://portal.tradinggarage.com/api/v1/auctions?status=live',
        'coming_soon': 'https://portal.tradinggarage.com/api/v1/auctions?status=coming_soon'
    }

    for status, api_url in endpoints.items():
        try:
            r = session.get(api_url, timeout=12)
            if r.status_code != 200:
                continue
            data = r.json()
            auctions = data.get('data', []) or data.get('auctions', []) or []
            for auction in auctions:
                if auction.get('object_type') != 'vehicle':
                    continue
                title = auction.get('title', 'Unknown Car')
                year_str = ''
                make = ''
                model = ''
                m = re.search(r'(\d{4})\s*([a-zA-Z0-9\-() ]+)\s+(.+)', title)

                if m:
                    year_str = m.group(1)
                    make = m.group(2).strip()
                    model = m.group(3).strip()
                try:
                    year = int(year_str)
                except:
                    year = 0
                price_str = auction.get('last_bid', '0')
                auction_date = None
                try:
                    auction_date = parse(auction['auction_end_at'])
                except:
                    pass
                images = [auction.get('title_image', '')]
                url = f"https://www.tradinggarage.com/products/{auction.get('slug', '')}"
                reserve = 'No' if auction.get('no_reserve', False) else 'Yes'
                location = 'Online / Melbourne'
                description = ''
                odometer = ''
                lot = {
                    'source': 'tradinggarage',
                    'status': auction['status']['name'],
                    'auction_id': auction['id'],
                    'title': title,
                    'year': year,
                    'make': make,
                    'model': model,
                    'odometer': odometer,
                    'price_range': parse_price(price_str),
                    'auction_date': auction_date,
                    'location': location,
                    'images': images,
                    'url': url,
                    'description': description,
                    'reserve': reserve,
                    'scrape_time': datetime.now(timezone.utc)
                }
                if is_classic(lot):
                    listings.append(lot)
        except Exception as e:
            pass
    return listings

def scrape_collectingcars():
    listings = []
    api_url = "https://dora.production.collecting.com/multi_search"
    headers = {
        'x-typesense-api-key': 'aKIufK0SfYHMRp9mUBkZPR7pksehPBZq',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Referer': 'https://collectingcars.com/',
    }
    base_payload = {
        "searches": [
            {
                "query_by": "title,productMake,vehicleMake,productYear,tags,lotType,driveSide,location,collectionId,modelId",
                "query_by_weights": "9,8,7,6,5,4,3,2,1,0",
                "text_match_type": "sum_score",
                "sort_by": "rank:asc",
                "highlight_full_fields": "*",
                "facet_by": "lotType, regionCode, countryCode, saleFormat, noReserve, isBoosted, productMake, vendorType, driveSide, listingStage, tags",
                "max_facet_values": 999,
                "facet_counts": True,
                "facet_stats": True,
                "facet_distribution": True,
                "facet_return_parent": True,
                "collection": "production_cars",
                "q": "*",
                "filter_by": "listingStage:=[`live`] && countryCode:=[`AU`] && regionCode:=[`APAC`]",
                "page": 1,
                "per_page": 50
            }
        ]
    }
    page = 1
    while True:
        base_payload["searches"][0]["page"] = page
        try:
            response = requests.post(api_url, headers=headers, json=base_payload, timeout=15)
            if response.status_code != 200:
                break
            data = response.json()
            if "results" not in data or not data["results"]:
                break
            result = data["results"][0]
            hits = result.get("hits", [])
            if not hits:
                break
            for hit in hits:
                doc = hit.get("document", {})
                if doc.get('lotType') != 'car':
                    continue
                title = doc.get('title', 'Unknown Car')
                year_str = doc.get('productYear', '')
                try:
                    year = int(year_str)
                except:
                    year = 0
                make = doc.get('productMake', '') or doc.get('vehicleMake', '')
                model = doc.get('modelName', '') + ' ' + doc.get('variantName', '').strip()
                price_str = doc.get('currentBid', 0)
                auction_date = None
                try:
                    auction_date = parse(doc['dtStageEndsUTC'])
                except:
                    pass
                images = [doc.get('mainImageUrl', '')]
                url = f"https://collectingcars.com/for-sale/{doc.get('slug', '')}"
                reserve = 'No' if doc.get('noReserve') == "true" else 'Yes'
                location = doc.get('location', 'Australia')
                description = ''  # No description in data
                odometer = doc['features'].get('mileage', '')
                transmission = doc['features'].get('transmission', extract_transmission(title))
                body_style = extract_body_style(title)
                fuel_type = doc['features'].get('fuelType', '')
                lot = {
                    'source': 'collectingcars',
                    'status': doc['listingStage'],
                    'auction_id': doc['auctionId'],
                    'title': title,
                    'year': year,
                    'make': make,
                    'model': model,
                    'odometer': odometer,
                    'price_range': parse_price(price_str),
                    'auction_date': auction_date,
                    'location': location,
                    'images': images,
                    'url': url,
                    'description': description,
                    'reserve': reserve,
                    'body_style': body_style,
                    'transmission': transmission,
                    'fuel_type': fuel_type,
                    'scrape_time': datetime.now(timezone.utc)
                }
                if is_classic(lot):
                    listings.append(lot)
            page += 1
            time.sleep(1.2)
        except Exception as e:
            break
    return listings

def scrape_chicane(url='https://www.chicaneauctions.com.au/february-2026-classic-car-auction/'):


    """
    Scrape classic car auctions from chicaneauctions.com.au
    Updated: Jan 2026 - better link detection, stronger placeholder filtering
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    try:
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()
    except Exception as e:
        print(f"Error fetching Chicane page: {e}")
        return []

    soup = BeautifulSoup(resp.text, 'html.parser')
    listings = []
    base_url = 'https://www.chicaneauctions.com.au'

    for item in soup.select('.promo_box'):
        try:
            # ── Get the MAIN link (prefer the "MORE DETAILS" button) ──
            button = item.select_one('.desc_wrapper .button')
            link = button if button else item.select_one('.desc_wrapper a')
            
            if not link:
                continue
                
            relative_href = link.get('href', '').strip()
            if not relative_href:
                continue
                
            full_url = relative_href if relative_href.startswith('http') else base_url + relative_href

            # ── Early skip obvious placeholders ──
            if '/sell/' in full_url.lower():
                continue

            # Title
            title_tag = item.select_one('.desc_wrapper .title')
            title = title_tag.get_text(strip=True) if title_tag else ''
            if not title:
                continue

            title_upper = title.upper()
            if '- OPEN POSITION -' in title_upper or 'STAY TUNED' in title_upper:
                continue

            # ── Image ──
            img_tag = item.select_one('.photo_wrapper img')
            img_src = None
            if img_tag:
                img_src = img_tag.get('data-src') or img_tag.get('src')
                if img_src and img_src.startswith('//'):
                    img_src = 'https:' + img_src
            
            # Skip well-known placeholder image
            if not img_src or 'upcoming-classic-car-auction-house.png' in img_src:
                continue

            images = [img_src] if img_src else []

            # ── Lot number ──
            lot_num = None
            # Try from URL
            m = re.search(r'(?:lot[-_\s]*)(\d+)', full_url, re.IGNORECASE)
            if m:
                lot_num = m.group(1)
            # Fallback: try from title
            if not lot_num:
                m = re.search(r'(?:lot|Lot|LOT)\s*(\d+)', title, re.IGNORECASE)
                if m:
                    lot_num = m.group(1)

            # ── Year / Make / Model parsing ──
            year = None
            make = ''
            model = ''

            # Common pattern: "1970 FORD FALCON XY GT" or "1965 FORD MUSTANG FB GT - RHD"
            m = re.match(r'^(\d{4})\s+([A-Za-z0-9\-]+(?:\s+[A-Za-z0-9\-]+)*?)(?:\s+(.+?))?(?:\s*-|$)', title.strip())
            if m:
                try:
                    year = int(m.group(1))
                except:
                    pass
                make = (m.group(2) or '').strip()
                model = (m.group(3) or '').strip()

            # Fallback - at least try to get year anywhere in title
            if not year:
                ym = re.search(r'\b(19\d{2}|20\d{2})\b', title)
                if ym:
                    year = int(ym.group(1))

            # ── Build lot dictionary ──
            location = {
                'city': 'Melbourne',
                'state': 'VIC',
                'country': 'Australia'
            }

            lot = {
                'source': 'chicaneauctions',
                'auction_id': lot_num or title.lower().replace(' ', '-').replace('--', '-'),
                'title': title,
                'url': full_url,
                'year': year,
                'make': make,
                'model': model,
                'vehicle': {
                    'year': year,
                    'make': make,
                    'model': model,
                },
                'price': {
                    'current': None,        # not shown on pre-catalogue
                    'reserve': 'Unknown',
                },
                'auction_end': None,        # not shown yet
                'location': location,
                'images': images,
                'condition': {
                    'comment': title,       # can be improved later from detail page
                },
                'status': 'upcoming',
                'scrape_time': datetime.utcnow().isoformat(),
            }

            # Only add if it looks like a real classic car
            if is_classic(lot):
                listings.append(lot)

                # Optional: debug output (comment out when done)
                print(f"Added: {lot['title']} | {lot['url']} | Year: {year}")

        except Exception as e:
            print(f"Error parsing one Chicane promo_box: {e}")
            continue

    print(f"Total real listings found: {len(listings)}")
    return listings

# def scrape_lloydsonline(url='https://www.lloydsonline.com.au/AuctionLots.aspx?stype=0&stypeid=0&cid=410&smode=0'):
#     """
#     Scrape classic car auctions from lloydsonline.com.au
#     """
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
#     }
#     try:
#         resp = requests.get(url, headers=headers, timeout=20)
#         if resp.status_code != 200:
#             print(f"Lloyds returned {resp.status_code}")
#             return []
#         html_content = resp.text
#     except Exception as e:
#         print(f"Error fetching Lloyds: {e}")
#         return []

#     soup = BeautifulSoup(html_content, 'html.parser')
#     listings = []
#     base_url = 'https://www.lloydsonline.com.au'

#     for item in soup.select('.gallery_item.lot_list_item'):
#         try:
#             # Link and URL
#             link = item.select_one('a')
#             relative_href = link.get('href', None) if link else None
#             full_url = base_url + '/' + relative_href.lstrip('/') if relative_href else None

#             # Lot number
#             lot_num_elem = item.select_one('.lot_num')
#             lot_num = lot_num_elem.text.strip() if lot_num_elem else None

#             # Image
#             img_tag = item.select_one('.lot_img')
#             img_src = img_tag.get('src', None) if img_tag else None
#             if img_src and img_src.startswith('//'):
#                 img_src = 'https:' + img_src
#             images = [img_src] if img_src else []

#             # Title / Description
#             title_tag = item.select_one('.lot_desc h1')
#             title = title_tag.text.strip() if title_tag else ''

#             # Parse year, make, model from title (common pattern: "YYYY Make Model ...")
#             year = None
#             make = ''
#             model = ''
#             m = re.match(r'^(\d{4})\s+(.+?)\s+(.+?)(?:\s+|$)', title)
#             if m:
#                 year_str = m.group(1)
#                 try:
#                     year = int(year_str)
#                 except:
#                     pass
#                 make = m.group(2).strip()
#                 model = m.group(3).strip()

#             # Current bid
#             bid_tag = item.select_one('.lot_cur_bid span')
#             current_bid_str = bid_tag.text.strip() if bid_tag else '0'
#             current_bid = float(re.sub(r'[^\d.]', '', current_bid_str)) if current_bid_str else None

#             # Time remaining
#             time_rem_tag = item.select_one('.lot_time_rem span')
#             seconds_rem_str = time_rem_tag.get('data-seconds_rem', '0') if time_rem_tag else '0'
#             seconds_rem = int(seconds_rem_str) if seconds_rem_str.isdigit() else 0
#             auction_end = datetime.utcnow() + timedelta(seconds=seconds_rem) if seconds_rem > 0 else None

#             # Location (state from image src)
#             location_img = item.select_one('.auctioneer-location')
#             state_src = location_img.get('src', '').split('/')[-1] if location_img else ''
#             state_map = {
#                 's_1.png': 'ACT',
#                 's_2.png': 'NT',
#                 's_3.png': 'NSW',
#                 's_4.png': 'QLD',
#                 's_5.png': 'SA',
#                 's_6.png': 'TAS',
#                 's_7.png': 'WA',
#                 's_8.png': 'VIC',
#             }
#             state = state_map.get(state_src, '')

#             location = {
#                 'state': state,
#             }

#             # Reserve (check for UNRESERVED sash)
#             unreserved = item.select_one('.sash.ribbon-blue')
#             reserve = 'No' if unreserved and 'UNRESERVED' in (unreserved.text or '').upper() else 'Yes'

#             # Vehicle specs (limited, from title)
#             vehicle = {
#                 'year': year,
#                 'make': make,
#                 'model': model,
#                 # Add more if details available in list view (none visible)
#             }

#             # Price info
#             price = {
#                 'current': current_bid,
#                 # No starting bid visible
#             }

#             # Condition (use title as comment)
#             condition = {
#                 'comment': title,
#             }

#             # Build lot dict
#             lot = {
#                 'source': 'lloydsonline',
#                 'auction_id': time_rem_tag.get('data-lot_id', lot_num) if time_rem_tag else lot_num,
#                 'title': title,
#                 'url': full_url,
#                 'year': year,
#                 'make': make,
#                 'model': model,
#                 'vehicle': vehicle,
#                 'price': price,
#                 'auction_end': auction_end,
#                 'location': location,
#                 'images': images,
#                 'condition': condition,
#                 'reserve': reserve,
#                 'status': 'live',
#                 'scrape_time': datetime.utcnow(),
#             }

#             if is_classic(lot):  # Assume you have an is_classic function to filter classics
#                 listings.append(lot)

#         except Exception as e:
#             print(f"Error parsing Lloyds lot: {str(e)}")

#     return listings

def scrape_lloydsonline(url='https://www.lloydsonline.com.au/AuctionLots.aspx?stype=0&stypeid=0&cid=410&smode=0'):
    """
    Scrape classic car auctions from lloydsonline.com.au
    Special focus: clean imagedelivery.net image URLs without thumbnail params
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    try:
        resp = requests.get(url, headers=headers, timeout=20)
        resp.raise_for_status()
    except Exception as e:
        print(f"Error fetching Lloyds: {e}")
        return []

    soup = BeautifulSoup(resp.text, 'html.parser')
    listings = []
    base_url = 'https://www.lloydsonline.com.au'

    for item in soup.select('.gallery_item.lot_list_item'):
        try:
            # ── Link / URL ────────────────────────────────────────
            link_tag = item.select_one('a[href^="LotDetails.aspx"]')
            relative_href = link_tag.get('href') if link_tag else None
            full_url = base_url + '/' + relative_href.lstrip('/') if relative_href else None

            # ── Lot number ────────────────────────────────────────
            lot_num_elem = item.select_one('.lot_num')
            lot_num = lot_num_elem.get_text(strip=True) if lot_num_elem else None

            # ── Image ─────────────────────────────────────────────
            img_tag = item.select_one('.lot_img img')
            img_src = None
            if img_tag and img_tag.has_attr('src'):
                src = img_tag['src']
                if src.startswith('//'):
                    src = 'https:' + src
                
                # Prefer imagedelivery.net URLs and clean size params
                if 'imagedelivery.net' in src:
                    # Remove size/crop params to get cleaner / base version
                    clean_src = re.sub(r'/(w=\d+,h=\d+,fit=[^/]+)?$', '', src)
                    clean_src = re.sub(r'\?.*$', '', clean_src)  # remove any query string if unwanted
                    img_src = clean_src
                else:
                    img_src = src

            images = [img_src] if img_src else []

            # ── Title / Description ───────────────────────────────
            desc_container = item.select_one('.lot_desc')
            title = ''
            if desc_container:
                # Sometimes it's in <span>, <div>, or direct text
                title_tag = desc_container.find(['h1', 'span', 'div'], recursive=True)
                title = title_tag.get_text(strip=True) if title_tag else desc_container.get_text(strip=True)

            # Try to parse year/make/model (common pattern)
            year = make = model = None
            m = re.match(r'^(\d{4})\s+([^\s]+)\s+(.+?)(?:\s+|$)', title, re.IGNORECASE)
            if m:
                try:
                    year = int(m.group(1))
                except ValueError:
                    pass
                make  = m.group(2).strip()
                model = m.group(3).strip()

            # ── Current bid (if visible in list view) ─────────────
            bid_tag = item.select_one('.lot_bidding .lot_cur_bid span')  # adjust selector if needed
            current_bid_str = bid_tag.get_text(strip=True) if bid_tag else None
            current_bid = None
            if current_bid_str:
                cleaned = re.sub(r'[^\d.]', '', current_bid_str)
                try:
                    current_bid = float(cleaned)
                except ValueError:
                    pass

            # ── Time remaining / auction end (if present) ─────────
            time_tag = item.select_one('[data-seconds_rem]')
            auction_end = None
            if time_tag and time_tag.has_attr('data-seconds_rem'):
                try:
                    secs = int(time_tag['data-seconds_rem'])
                    if secs > 0:
                        auction_end = datetime.utcnow() + timedelta(seconds=secs)
                except ValueError:
                    pass

            # ── Build lot dictionary ──────────────────────────────
            lot = {
                'source':       'lloydsonline',
                'lot_number':   lot_num,
                'title':        title,
                'url':          full_url,
                'year':         year,
                'make':         make,
                'model':        model,
                'current_bid':  current_bid,
                'auction_end':  auction_end.isoformat() if auction_end else None,
                'images':       images,               # ← now contains clean imagedelivery.net URL
                'scrape_time':  datetime.utcnow().isoformat(),
                # Add more fields as needed: location, reserve, etc.
            }

            if is_classic(lot):
                listings.append(lot)

        except Exception as e:
            print(f"Error parsing lot: {e}")

    return listings

def scrape_carbids_api():
    """
    Scrape current auctions from carbids.com.au using the real /Search/Tags endpoint
    """
    listings = []
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://carbids.com.au/',
        'Origin': 'https://carbids.com.au',
    })

    # Try to get verification token first (some endpoints require it)
    try:
        home = session.get("https://carbids.com.au/t/unique-and-classic-car-auctions")
        soup = BeautifulSoup(home.text, 'html.parser')
        token_input = soup.find('input', {'name': '__RequestVerificationToken'})
        if token_input and token_input.get('value'):
            session.headers['__RequestVerificationToken'] = token_input['value']
    except:
        pass

    page = 0
    while True:
        payload = {
            "top": 96,
            "skip": page * 96,
            "sort": {"aucClose": "asc"},
            "tagName": "Unique and Classic Car Auctions",
            "filter": {"Display": True}
        }

        try:
            resp = session.post(
                "https://carbids.com.au/Search/Tags",
                json=payload,
                timeout=20
            )

            if resp.status_code != 200:
                print(f"Carbids API returned {resp.status_code}")
                break

            data = resp.json()
            auctions = data.get("auctions", [])
            if not auctions:
                break

            for auc in auctions:
                # ────────────────────────────────────────────────
                # Basic identification
                # ────────────────────────────────────────────────
                title       = auc.get("aucTitle", "").strip()
                title_text  = auc.get("aucTitleText", title).strip()
                short_title = auc.get("aucTitleShortText", title).strip()

                # Try to extract year/make/model from title
                year = None
                make = ""
                model = ""

                # Common pattern: "MM/YYYY Make Model ..."
                m = re.match(r'^(\d{1,2}/)?(\d{4})\s+(.+?)\s+(.+?)(?:\s+|$)', title_text)
                if m:
                    year_str = m.group(2)
                    make     = m.group(3).strip()
                    model    = m.group(4).strip()
                    try:
                        year = int(year_str)
                    except:
                        year = None

                # Fallback from explicit fields
                if not year and auc.get("aucYear"):
                    try:
                        year = int(auc["aucYear"])
                    except:
                        pass

                make  = auc.get("aucMake",  make).strip()
                model = auc.get("aucModel", model).strip()

                # ────────────────────────────────────────────────
                # Price & bidding
                # ────────────────────────────────────────────────
                current_bid = auc.get("aucCurrentBid", 0.0)
                starting_bid = auc.get("aucStartingBid", 1.0)
                price_info = {
                    "current": float(current_bid) if current_bid else None,
                    "starting": float(starting_bid) if starting_bid else None,
                    "increment": auc.get("aucBidIncrement", 0.0),
                    "buyers_premium_text": auc.get("aucBPText", ""),
                    "gst_note": auc.get("isGstApplicableWording", "")
                }

                # ────────────────────────────────────────────────
                # Auction timing
                # ────────────────────────────────────────────────
                end_date_str = auc.get("aucCloseUtc")
                auction_end = None
                if end_date_str:
                    try:
                        auction_end = datetime.fromisoformat(end_date_str.replace("Z", "+00:00"))
                    except:
                        try:
                            auction_end = parse(end_date_str)
                        except:
                            pass

                # ────────────────────────────────────────────────
                # Location
                # ────────────────────────────────────────────────
                location = {
                    "city": auc.get("aucCity", ""),
                    "state": auc.get("aucState", ""),
                    "address": auc.get("aucAddressLocation", ""),
                    "pickup": auc.get("aucPickupAvailable", False),
                    "freight": auc.get("aucFreightAvailable", False),
                    "freight_limits": auc.get("aucItemFreightLimits", "")
                }

                # ────────────────────────────────────────────────
                # Vehicle specs
                # ────────────────────────────────────────────────
                vehicle = {
                    "year": year,
                    "make": make,
                    "model": model,
                    "odometer_km": auc.get("aucOdometerNumber"),
                    "odometer_display": auc.get("aucOdometer", ""),
                    "transmission": auc.get("aucTransmission"),
                    "fuel_type": auc.get("aucFuelType"),
                    "engine_capacity": auc.get("aucCapacity"),
                    "cylinders": auc.get("aucCylinder"),
                    "drivetrain": auc.get("aucDrv"),
                }

                # ────────────────────────────────────────────────
                # Images
                # ────────────────────────────────────────────────
                images = []
                base = auc.get("aucCarsThumbnailUrl", auc.get("aucThumbnailUrl", ""))
                if base:
                    images.append(base)
                for size in ["small", "medium", "large"]:
                    key = f"aucCars{size.capitalize()}ThumbnailUrl"
                    if auc.get(key):
                        images.append(auc[key])

                # Also medium list if available
                medium_list = auc.get("aucMediumThumbnailUrlList", [])
                images.extend([url for url in medium_list if url])

                # ────────────────────────────────────────────────
                # Condition & history
                # ────────────────────────────────────────────────
                condition = {
                    "body": auc.get("aucBodyCondition"),
                    "paint": auc.get("aucPaintCondition"),
                    "features_text": auc.get("aucFeaturesText"),
                    "key_facts": auc.get("aucKeyFactsText"),
                    "comment": auc.get("aucComment"),
                    "service_history": auc.get("aucServiceHistory"),
                }

                # ────────────────────────────────────────────────
                # Build final document
                # ────────────────────────────────────────────────
                lot = {
                    "source": "carbids",
                    "auction_id": auc.get("aucID"),
                    "reference_number": auc.get("aucReferenceNo"),
                    "title": title_text,
                    "short_title": short_title,
                    "url": "https://carbids.com.au/" + auc.get("AucDetailsUrlLink", "").lstrip("/"),
                    "year": year,
                    "make": make,
                    "model": model,
                    "vehicle": vehicle,
                    "price": price_info,
                    "auction_end": auction_end,
                    "location": location,
                    "images": images[:8],  # limit to 8 for storage
                    "condition": condition,
                    "reserve": "Yes",       # currently no reserve field → assume Yes
                    "status": "live",       # we only get live auctions here
                    "scrape_time": datetime.utcnow(),
                }
                if is_classic(lot):
                    listings.append(lot)

            page += 1
            time.sleep(1.3)  # polite delay

        except Exception as e:
            print("Error in carbids API loop:", str(e))
            break

    return listings


def scrape_carbids(base_url):
    # Keep your existing browser-based scraper if you still want it
    # listings_browser = scrape_carbids_browser(base_url)   # your old function

    # Add the API scraper
    listings_api = scrape_carbids_api()
    # Combine (API tends to be more reliable and complete)
    combined = listings_api 

    # Remove exact duplicates by url
    seen_urls = set()
    unique = []
    for lot in combined:
        u = lot.get("url")
        if u and u not in seen_urls:
            seen_urls.add(u)
            unique.append(lot)

    return unique
# def scrape_bennetts(base_url):
    pages = [base_url, base_url + '/off-site.php']
    all_listings = []
    for page_url in pages:
        try:
            driver = get_driver()
            driver.get(page_url)
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            driver.quit()
            sitename = soup.find('div', id='sitename')
            h3 = sitename.find('h3') if sitename else None
            auction_text = h3.text.strip() if h3 else ''
            date_match = re.search(r'(\d{1,2}[ST|ND|RD|TH]{0,2} \w+ \d{4})', auction_text.upper())
            time_match = re.search(r'@ (\d{1,2}[AP]M)', auction_text.upper())
            auction_date_str = ''
            if date_match:
                date_str = re.sub(r'([ST|ND|RD|TH])', '', date_match.group(1))
                auction_date_str += date_str
            if time_match:
                auction_date_str += ' ' + time_match.group(1)
            auction_date = None
            try:
                auction_date = parse(auction_date_str)
            except:
                pass
            sections = soup.find_all('div', class_='clear')
            for section in sections:
                column = section.find('div', class_='column column-600 column-left')
                if column:
                    h3_cat = column.find('h3')
                    category = h3_cat.text.strip() if h3_cat else ''
                    table = column.find('table')
                    if table:
                        tbody = table.find('tbody')
                        trs = tbody.find_all('tr') if tbody else table.find_all('tr')
                        for tr in trs[1:]:
                            tds = tr.find_all('td')
                            if len(tds) == 7:
                                photo_td = tds[0]
                                a = photo_td.find('a')
                                detail_url = base_url + '/' + a['href'].lstrip('/') if a else ''
                                img = photo_td.find('img')
                                image_src = base_url + '/' + img['src'].lstrip('/') if img and img['src'].startswith('images') else img['src']
                                make = tds[1].text.strip()
                                stock_model = tds[2].text.strip()
                                parts = stock_model.split('/')
                                stock_ref = parts[0].strip() if parts else ''
                                model = parts[1].strip() if len(parts) > 1 else stock_model
                                year_str = tds[3].text.strip()
                                try:
                                    year = int(year_str)
                                except:
                                    year = 0
                                options = tds[4].text.strip()
                                location_td = tds[5]
                                location = location_td.text.strip().replace('\n', '').replace('br /', '')
                                lot = {
                                    'source': 'bennettsclassicauctions',
                                    'make': make,
                                    'model': model,
                                    'year': year,
                                    'price_range': None,
                                    'auction_date': auction_date,
                                    'location': location,
                                    'images': [image_src] if image_src else [],
                                    'url': detail_url,
                                    'description': options,
                                    'reserve': 'Yes',
                                    'body_style': extract_body_style(options),
                                    'transmission': extract_transmission(options),
                                    'scrape_time': datetime.now()
                                }
                                if is_classic(lot):
                                    all_listings.append(lot)
        except Exception as e:
            pass
    return all_listings

def scrape_bennetts(base_url="https://www.bennettsclassicauctions.com.au"):
    pages = [base_url, base_url + '/off-site.php']
    all_listings = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    for page_url in pages:
        try:
            resp = requests.get(page_url, headers=headers, timeout=20)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')

            # Extract auction text for date
            sitename = soup.find('div', id='sitename')
            h3 = sitename.find('h3') if sitename else None
            auction_text = h3.text.strip() if h3 else ''
            date_match = re.search(r'(\d{1,2}[ST|ND|RD|TH]{0,2} \w+ \d{4})', auction_text.upper())
            time_match = re.search(r'@ (\d{1,2}[AP]M)', auction_text.upper())
            auction_date_str = ''
            if date_match:
                date_str = re.sub(r'([ST|ND|RD|TH])', '', date_match.group(1))
                auction_date_str += date_str
            if time_match:
                auction_date_str += ' ' + time_match.group(1)
            auction_date = None
            try:
                auction_date = parse(auction_date_str)
            except:
                pass

            # Find sections with listings
            sections = soup.find_all('div', class_='clear')
            for section in sections:
                column = section.find('div', class_='column column-600 column-left')
                if column:
                    h3_cat = column.find('h3')
                    category = h3_cat.text.strip() if h3_cat else ''
                    table = column.find('table')
                    if table:
                        tbody = table.find('tbody')
                        trs = tbody.find_all('tr') if tbody else table.find_all('tr')
                        for tr in trs[1:]:  # Skip header
                            tds = tr.find_all('td')
                            if len(tds) >= 7:  # Ensure enough columns
                                photo_td = tds[0]
                                a = photo_td.find('a')
                                detail_url = base_url + '/' + a['href'].lstrip('/') if a else ''
                                img = photo_td.find('img')
                                image_src = base_url + '/' + img['src'].lstrip('/') if img and img['src'].startswith('images') else (img['src'] if img else '')

                                make = tds[1].text.strip()
                                stock_model = tds[2].text.strip()
                                parts = stock_model.split('/')
                                stock_ref = parts[0].strip() if parts else ''
                                model = parts[1].strip() if len(parts) > 1 else stock_model

                                year_str = tds[3].text.strip()
                                try:
                                    year = int(year_str)
                                except:
                                    year = 0

                                options = tds[4].text.strip()
                                location_td = tds[5]
                                location = location_td.text.strip().replace('\n', '').replace('br /', '')

                                lot = {
                                    'source': 'bennettsclassicauctions',
                                    'make': make,
                                    'model': model,
                                    'year': year,
                                    'price_range': None,
                                    'auction_date': auction_date,
                                    'location': location,
                                    'images': [image_src] if image_src else [],
                                    'url': detail_url,
                                    'description': options,
                                    'reserve': 'Yes',
                                    'body_style': extract_body_style(options),
                                    'transmission': extract_transmission(options),
                                    'scrape_time': datetime.now(timezone.utc)
                                }
                                if is_classic(lot):
                                    all_listings.append(lot)
        except Exception as e:
            print(f"Error scraping Bennetts ({page_url}): {str(e)}")
            import traceback
            traceback.print_exc()
    return all_listings


from urllib.parse import urljoin

def scrape_burnsandco(base_url="https://burnsandcoauctions.com.au"):
    pages = [base_url + '/current-auctions/', base_url + '/upcoming-auctions/']
    all_listings = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    for page_url in pages:
        try:
            resp = requests.get(page_url, headers=headers, timeout=20)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, 'html.parser')
            articles = soup.find_all('article', class_='regular masonry-blog-item')
            for article in articles:
                img_link = article.find('a', class_='img-link')
                detail_url = img_link['href'] if img_link else ''
                img = img_link.find('img') if img_link else None
                image_src = img['src'] if img else ''
                meta_category = article.find('span', class_='meta-category')
                category = meta_category.text.strip() if meta_category else ''
                date_item = article.find('span', class_='date-item')
                auction_date_str = date_item.text.strip() if date_item else ''
                auction_date = None
                try:
                    auction_date = parse(auction_date_str)
                except:
                    pass
                title_a = article.find('h3', class_='title').find('a') if article.find('h3', class_='title') else None
                title = title_a.text.strip() if title_a else ''
                excerpt = article.find('div', class_='excerpt').text.strip() if article.find('div', class_='excerpt') else ''
                place = article.find('p', class_='place').text.strip() if article.find('p', class_='place') else ''
                bid_links = article.find_all('p', class_='registration_bidding_link')
                for bid_p in bid_links:
                    bid_a = bid_p.find('a')
                    bid_url = bid_a['href'] if bid_a else ''
                    catalogue_lots = scrape_catalogue(bid_url)
                    for cat_lot in catalogue_lots:
                        cat_lot['auction_date'] = auction_date or cat_lot.get('auction_date')
                        cat_lot['location'] = place or cat_lot.get('location')
                        cat_lot['source'] = 'burnsandco'
                        all_listings.append(cat_lot)
        except Exception as e:
            print(f"Error scraping Burns and Co ({page_url}): {str(e)}")
            import traceback
            traceback.print_exc()
    return all_listings

from datetime import datetime, timezone, timedelta
import requests
import re
from dateutil.parser import parse

# def scrape_seven82motors():
#     """
#     Scrape upcoming lots from seven82motors.com.au using their JSON feed.
#     Example endpoint: https://seven82-json-sb.manage.auction/listings/auctions/march-29th-2026?amt=100
    
#     Returns list of lot dictionaries matching your existing schema.
#     """
#     listings = []
    
#     # For now using a known upcoming auction slug
#     # In production: you should discover current/upcoming slugs dynamically
#     auction_slug = "march-29th-2026"
#     api_url = f"https://seven82-json-sb.manage.auction/listings/auctions/{auction_slug}?amt=100"
    
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
#                       '(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
#         'Accept': 'application/json',
#         'Referer': 'https://www.seven82motors.com.au/',
#     }
    
#     try:
#         resp = requests.get(api_url, headers=headers, timeout=20)
#         resp.raise_for_status()
#         data = resp.json()
        
#         auction_title = data.get("heading", "Unknown Auction Date")
        
#         # Try to parse auction date from breadcrumbs or heading
#         auction_date = None
#         try:
#             bc_title = data.get("breadcrumbs", [{}])[0].get("title", "")
#             if bc_title and any(m in bc_title.lower() for m in ["mar", "march", "apr", "may"]):
#                 # e.g. "Mar 29, 2026"
#                 auction_date = parse(f"{bc_title} 2026", fuzzy=True)
#         except:
#             pass
        
#         if not auction_date:
#             try:
#                 auction_date = parse(auction_title, fuzzy=True)
#             except:
#                 auction_date = datetime.now(timezone.utc) + timedelta(days=45)  # reasonable fallback
        
#         items = data.get("items", [])
        
#         for item in items:
#             # Skip advertising / consignment slots
#             if item.get("dummy_lot", 0) == 1:
#                 continue
                
#             title = (item.get("title") or "").strip()
#             if not title:
#                 continue
                
#             # Skip obvious non-car listings
#             if any(phrase in title.upper() for phrase in [
#                 "SELL YOUR CAR", "CONSIGN", "REGISTER AND BID", "LEARN HOW TO"
#             ]):
#                 continue
                
#             # ────────────────────────────────────────────────
#             # Year / Make / Model parsing
#             # ────────────────────────────────────────────────
#             year = None
#             make = ""
#             model = ""
            
#             # Remove common prefixes
#             clean_title = re.sub(
#                 r'^(NO RESERVE!?\s*|RARE\s*|FULLY RESTORED\s*|CUSTOM\s*)',
#                 '', title, flags=re.IGNORECASE
#             ).strip()
            
#             # Common patterns: "1969 Holden HT 350 GTS Monaro"
#             #                 "1972 Ford 4x4 Bronco"
#             m = re.match(r'^(\d{4})\s+(.+?)(?:\s+(.+?))?(?:\s+|$)', clean_title)
#             if m:
#                 try:
#                     year = int(m.group(1))
#                 except:
#                     pass
#                 make_model_part = (m.group(2) or "").strip()
#                 extra = (m.group(3) or "").strip()
                
#                 # Simple split - will not be perfect but good enough for filtering
#                 parts = make_model_part.split(maxsplit=1)
#                 if parts:
#                     make = parts[0].strip()
#                     if len(parts) > 1:
#                         model = parts[1].strip()
#                     model = f"{model} {extra}".strip()
            
#             # Reserve status from title (very reliable on this site)
#             reserve = "No" if "NO RESERVE" in title.upper() else "Yes"
            
#             # ────────────────────────────────────────────────
#             # Images
#             # ────────────────────────────────────────────────
#             images = []
            
#             # 1. media_featured → list of dicts
#             featured = item.get("media_featured", [])
#             if isinstance(featured, list):
#                 for img_obj in featured:
#                     if isinstance(img_obj, dict):
#                         src = img_obj.get("src")
#                         if src:
#                             if src.startswith("/"):
#                                 src = "https://www.seven82motors.com.au" + src
#                             elif not src.startswith("http"):
#                                 src = "https://www.seven82motors.com.au/" + src
#                             if src not in images:
#                                 images.append(src)
            
#             # 2. fallback to main image field
#             main_img = item.get("image")
#             if main_img and main_img not in images:
#                 if main_img.startswith("catalog/"):
#                     main_img = "https://www.seven82motors.com.au/" + main_img
#                 images.insert(0, main_img)
            
#             # Deduplicate while preserving order
#             seen = set()
#             images = [x for x in images if x not in seen and not seen.add(x)]
            
#             # ────────────────────────────────────────────────
#             # Coming soon flag – safely handled
#             # ────────────────────────────────────────────────
#             is_coming_soon = False
#             coming_soon_data = item.get("coming_soon", [])
#             if isinstance(coming_soon_data, list):
#                 for entry in coming_soon_data:
#                     if isinstance(entry, dict):
#                         settings = entry.get("settings", {})
#                         if settings.get("coming_soon") in (True, "1", 1, "true"):
#                             is_coming_soon = True
#                             break
            
#             # ────────────────────────────────────────────────
#             # Build lot document
#             # ────────────────────────────────────────────────
#             lot_url = f"https://www.seven82motors.com.au/auctions/{item.get('path', '').lstrip('/')}"
            
#             lot = {
#                 'source': 'seven82motors',
#                 'status': 'upcoming',
#                 'auction_id': item.get("id"),
#                 'lot_number': item.get("number"),
#                 'title': title,
#                 'year': year,
#                 'make': make,
#                 'model': model,
#                 'odometer': None,                    # detail page only
#                 'price_range': None,                 # not visible in list
#                 'auction_date': auction_date,
#                 'location': "Brisbane, QLD (Online)",
#                 'images': images[:12],               # reasonable limit
#                 'url': lot_url,
#                 'description': (item.get("description_short") or "").strip(),
#                 'reserve': reserve,
#                 'body_style': None,
#                 'transmission': None,
#                 'fuel_type': None,
#                 'scrape_time': datetime.now(timezone.utc),
                
#                 # Optional / diagnostic fields
#                 'coming_soon': is_coming_soon,
#                 'buyers_premium_pct': 8.8,           # hard-coded from feed
#                 'raw_filters': item.get("filters", {}),
#             }
            
#             # Only keep if it passes your classic car filter
#             if is_classic(lot):
#                 listings.append(lot)
        
#         print(f"[seven82motors] Scraped {len(listings)} potential classic lots from '{auction_title}'")
        
#     except Exception as e:
#         print(f"[seven82motors] Error scraping {auction_slug}: {e}")
#         import traceback
#         traceback.print_exc()
    
#     return listings


def scrape_seven82motors():
    """
    Scrape upcoming lots from seven82motors.com.au using their JSON feed.
    Uses high-quality image URLs from mymedia.delivery CDN.
    
    Returns list of lot dictionaries matching your existing schema.
    """
    listings = []
    
    # Hardcoded for the known upcoming auction as of Jan 2026
    # In production: implement dynamic slug discovery (see notes below)
    auction_slug = "march-29th-2026"
    api_url = f"https://seven82-json-sb.manage.auction/listings/auctions/{auction_slug}?amt=100"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'Accept': 'application/json',
        'Referer': 'https://www.seven82motors.com.au/',
    }
    
    try:
        resp = requests.get(api_url, headers=headers, timeout=20)
        resp.raise_for_status()
        data = resp.json()
        
        auction_title = data.get("heading", "Unknown Auction Date")
        print(f"[seven82motors] Processing auction: {auction_title}")
        
        # ────────────────────────────────────────────────
        # Improved auction date parsing
        # ────────────────────────────────────────────────
        auction_date = None
        date_str_candidates = [
            auction_title,
            data.get("breadcrumbs", [{}])[0].get("title", ""),
            f"{auction_title} 2026",
            auction_slug.replace("-", " ").title()
        ]
        
        for candidate in date_str_candidates:
            if not candidate:
                continue
            try:
                auction_date = dateparse(candidate, fuzzy=True, dayfirst=False)
                if auction_date.year >= 2025:  # reasonable sanity check
                    break
            except:
                continue
        
        if not auction_date:
            auction_date = datetime.now(timezone.utc) + timedelta(days=60)
            print("[seven82motors] Using fallback auction date")
        
        items = data.get("items", [])
        
        for item in items:
            # Skip advertising / placeholder / consignment slots
            if item.get("dummy_lot", 0) == 1:
                continue
                
            title = (item.get("title") or "").strip()
            if not title:
                continue
                
            # Skip non-vehicle promo listings
            if any(phrase in title.upper() for phrase in [
                "SELL YOUR CAR", "CONSIGN", "REGISTER AND BID", "LEARN HOW TO"
            ]):
                continue
            
            # ────────────────────────────────────────────────
            # Year / Make / Model parsing
            # ────────────────────────────────────────────────
            year = None
            make = ""
            model = ""
            
            clean_title = re.sub(
                r'^(NO RESERVE!?\s*|RARE\s*|FULLY RESTORED\s*|CUSTOM\s*)',
                '', title, flags=re.IGNORECASE
            ).strip()
            
            m = re.match(r'^(\d{4})\s+(.+?)(?:\s+(.+?))?(?:\s+|$)', clean_title)
            if m:
                try:
                    year = int(m.group(1))
                except:
                    pass
                make_model_part = (m.group(2) or "").strip()
                extra = (m.group(3) or "").strip()
                
                parts = make_model_part.split(maxsplit=1)
                if parts:
                    make = parts[0].strip()
                    if len(parts) > 1:
                        model = parts[1].strip()
                    model = f"{model} {extra}".strip()
            
            # Reserve status (very reliable on this site)
            reserve = "No" if "NO RESERVE" in title.upper() else "Yes"
            
            # ────────────────────────────────────────────────
            # High-quality images via mymedia.delivery CDN
            # ────────────────────────────────────────────────
            images = []
            
            # Preferred source: media_featured
            featured = item.get("media_featured", [])
            if isinstance(featured, list):
                for img_obj in featured:
                    if isinstance(img_obj, dict):
                        src = img_obj.get("src")
                        if src and "catalog/" in src:
                            # Rewrite to full high-res CDN URL
                            clean_src = src.lstrip('/')
                            full_url = f"https://seven82motors.mymedia.delivery/{clean_src}"
                            if full_url not in images:
                                images.append(full_url)
            
            # Fallback: main image field
            main_img = item.get("image")
            if main_img and "catalog/" in main_img:
                clean_main = main_img.lstrip('/')
                full_main = f"https://seven82motors.mymedia.delivery/{clean_main}"
                if full_main not in images:
                    images.insert(0, full_main)
            
            # Deduplicate and filter obvious low-quality
            seen = set()
            clean_images = []
            for url in images:
                if url and url not in seen:
                    seen.add(url)
                    if not any(x in url.lower() for x in ["thumb", "small", "placeholder", "watermark"]):
                        clean_images.append(url)
            
            images = clean_images[:12]
            
            # ────────────────────────────────────────────────
            # Coming soon flag
            # ────────────────────────────────────────────────
            is_coming_soon = False
            coming_soon_data = item.get("coming_soon", [])
            if isinstance(coming_soon_data, list):
                for entry in coming_soon_data:
                    if isinstance(entry, dict):
                        if entry.get("settings", {}).get("coming_soon") in (True, "1", 1, "true"):
                            is_coming_soon = True
                            break
            
            # ────────────────────────────────────────────────
            # Build lot document
            # ────────────────────────────────────────────────
            lot_path = item.get('path', '').lstrip('/')
            lot_url = f"https://www.seven82motors.com.au/lot/{lot_path}" if lot_path else ""
            
            lot = {
                'source': 'seven82motors',
                'status': 'upcoming',
                'auction_id': item.get("id"),
                'lot_number': item.get("number"),
                'title': title,
                'year': year,
                'make': make,
                'model': model,
                'odometer': None,           # detail page only
                'price_range': None,        # not in list view
                'auction_date': auction_date,
                'location': "Brisbane, QLD (Online)",
                'images': images,
                'url': lot_url,
                'description': (item.get("description_short") or "").strip(),
                'reserve': reserve,
                'body_style': None,
                'transmission': None,
                'fuel_type': None,
                'scrape_time': datetime.now(timezone.utc),
                
                # Optional fields
                'coming_soon': is_coming_soon,
                'buyers_premium_pct': 8.8,  # known from site
                'auction_title': auction_title,
                'raw_filters': item.get("filters", {}),
            }
            
            if is_classic(lot):
                listings.append(lot)
        
        print(f"[seven82motors] Scraped {len(listings)} potential classic lots from '{auction_title}'")
        
    except Exception as e:
        print(f"[seven82motors] Error scraping {auction_slug}: {e}")
        import traceback
        traceback.print_exc()
    
    return listings

# def scrape_catalogue(catalogue_url):
#     listings = []
#     try:
#         driver = get_driver()
#         driver.get(catalogue_url)
#         soup = BeautifulSoup(driver.page_source, 'html.parser')
#         driver.quit()
#         lot_items = soup.find_all('div', class_='lot-item')  # Placeholder, adjust based on site inspection
#         for item in lot_items:
#             lot_number = item.find('span', class_='lot-number').text.strip() if item.find('span', class_='lot-number') else ''
#             desc = item.find('div', class_='lot-description').text.strip() if item.find('div', class_='lot-description') else ''
#             match = re.match(r'(\d{4})? ?(.*?) (.*)', desc)
#             year_str = match.group(1) if match and match.group(1) else ''
#             try:
#                 year = int(year_str)
#             except:
#                 year = 0
#             make = match.group(2) if match else ''
#             model = match.group(3) if match else desc
#             images = [img['src'] for img in item.find_all('img')]
#             detail_a = item.find('a', class_='lot-detail')
#             detail_url = catalogue_url + detail_a['href'] if detail_a else ''
#             current_bid = item.find('span', class_='current-bid').text.strip() if item.find('span', class_='current-bid') else ''
#             lot = {
#                 'lot_number': lot_number,
#                 'make': make,
#                 'model': model,
#                 'year': year,
#                 'price_range': parse_price(current_bid),
#                 'auction_date': None,
#                 'location': None,
#                 'images': images,
#                 'url': detail_url,
#                 'description': desc,
#                 'reserve': 'Yes',
#                 'body_style': extract_body_style(desc),
#                 'transmission': extract_transmission(desc),
#                 'scrape_time': datetime.now()
#             }
#             if is_classic(lot):
#                 listings.append(lot)
#     except Exception as e:
#         pass
#     return listings

from urllib.parse import urljoin

def scrape_catalogue(catalogue_url):
    listings = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        resp = requests.get(catalogue_url, headers=headers, timeout=20)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, 'html.parser')
        # Assume lots are in a table; adjust if needed based on inspection
        table = soup.find('table')  # Or find('table', class_='catalogue-table') if specific class
        if table:
            trs = table.find_all('tr')
            for tr in trs[1:]:  # Skip header row
                tds = tr.find_all('td')
                if len(tds) < 4:
                    continue
                lot_number = tds[0].text.strip()
                desc_td = tds[1]
                desc = desc_td.text.strip()
                match = re.match(r'(\d{4})? ?(.*?) (.*)', desc)
                year_str = match.group(1) if match and match.group(1) else ''
                try:
                    year = int(year_str)
                except:
                    year = 0
                make = match.group(2) if match else ''
                model = match.group(3) if match else desc
                images = [urljoin(catalogue_url, img['src']) for img in tr.find_all('img') if 'src' in img.attrs]
                detail_a = desc_td.find('a')
                detail_url = urljoin(catalogue_url, detail_a['href']) if detail_a else ''
                current_bid = tds[2].text.strip()
                # bids = tds[3].text.strip() if len(tds) > 3 else ''
                lot = {
                    'lot_number': lot_number,
                    'make': make,
                    'model': model,
                    'year': year,
                    'price_range': parse_price(current_bid),
                    'auction_date': None,
                    'location': None,
                    'images': images,
                    'url': detail_url,
                    'description': desc,
                    'reserve': 'Yes',
                    'body_style': extract_body_style(desc),
                    'transmission': extract_transmission(desc),
                    'scrape_time': datetime.now(timezone.utc)
                }
                if is_classic(lot):
                    listings.append(lot)
    except Exception as e:
        print(f"Error scraping catalogue ({catalogue_url}): {str(e)}")
        import traceback
        traceback.print_exc()
    return listings
def parse_lot(item, url):
    try:
        description = item.find('p', class_='desc') or item.find('div', class_='description')
        description_text = description.text.strip() if description else ''
        year_elem = item.find('span', class_='year') or item.find('h3')
        year_str = year_elem.text.strip() if year_elem else '0'
        try:
            year = int(year_str)
        except:
            year = 0
        make_elem = item.find('span', class_='make') or item.find('h2')
        model_elem = item.find('span', class_='model')
        price_elem = item.find('span', class_='estimate') or item.find('div', class_='price')
        price_str = price_elem.text.strip() if price_elem else None
        date_elem = item.find('span', class_='date')
        location_elem = item.find('span', class_='location')
        link_elem = item.find('a', class_='lot-link') or item.find('a')
        lot = {
            'make': make_elem.text.strip() if make_elem else None,
            'model': model_elem.text.strip() if model_elem else None,
            'year': year,
            'price_range': parse_price(price_str),
            'auction_date': parse_date(date_elem.text.strip()) if date_elem else None,
            'location': location_elem.text.strip() if location_elem else 'Online',
            'images': [img['src'] for img in item.find_all('img', class_='thumbnail')][:6],
            'url': link_elem['href'] if link_elem else url,
            'description': description_text,
            'reserve': 'No' if 'no reserve' in description_text.lower() else 'Yes',
            'body_style': extract_body_style(description_text),
            'transmission': extract_transmission(description_text),
            'scrape_time': datetime.now()
        }
        return lot
    except:
        return None

def parse_date(date_str):
    try:
        return parse(date_str)
    except:
        return None

def extract_body_style(desc):
    lower_desc = desc.lower()
    styles = ['coupe', 'convertible', 'sedan', 'wagon', 'ute', 'truck']
    for style in styles:
        if style in lower_desc:
            return style.capitalize()
    return None

def extract_transmission(desc):
    lower_desc = desc.lower()
    if 'manual' in lower_desc:
        return 'Manual'
    if 'auto' in lower_desc or 'automatic' in lower_desc:
        return 'Automatic'
    return None
def is_classic(lot):
    """
    Determine if a lot should be considered a 'classic' car.
    Safe against missing/invalid year values.
    """
    year = lot.get('year')
    
    # If year is missing or not a number → treat as non-classic (or adjust logic)
    if year is None or not isinstance(year, (int, float)):
        # Optional: look in title/description for clues
        text = (lot.get('title', '') + ' ' + lot.get('description', '')).lower()
        has_classic_hint = any(word in text for word in [
            'classic', 'muscle', 'vintage', 'hot rod', 'restored', 'collector',
            'holden', 'falcon gt', 'monaro', 'charger', 'mustang', 'corvette'
        ])
        return has_classic_hint
    
    # Normal year-based rule
    if year < 2005:
        return True
    
    # Bonus: some newer cars are "future classics" or muscle
    text = (lot.get('title', '') + ' ' + lot.get('description', '')).lower()
    modern_classic_keywords = [
        'hellcat', 'demon', 'supercharged', 'stroker', 'r8', 'gts-r', 'boss 302',
        'shelby', 'a9x', 'fpv', 'gtr', 'torana', 'monaro'
    ]
    
    return any(kw in text for kw in modern_classic_keywords)
# def is_classic(lot):
#     year = lot.get('year', 0)
#     desc = lot.get('description', '').lower() + ' ' + lot.get('title', '').lower()
#     if year < 2005:
#         return True
#     elif any(word in desc for word in ['collector', 'classic', 'future classic', 'modern classic', 'muscle']):
#         return True
#     return False
# def is_classic(lot):
#     year = lot.get('year', 0)
#     text = (lot['description'].lower() if lot['description'] else '') + ' ' + (lot['title'].lower() if lot['title'] else '')
#     return year < 1990 or any(word in text for word in ['collector', 'classic', 'future classic', 'modern classic', 'muscle'])
def normalize_auction_date(ad):
    if not ad:
        return None
    if isinstance(ad, datetime):
        return ad
    if isinstance(ad, str):
        try:
            return parse(ad)
        except:
            return None
    try:
        return parse(str(ad))
    except:
        return None

def extract_provenance(desc):
    # Simple placeholder: return full desc or parse key phrases
    return desc

def build_query(params):
    query = {}
    if 'make' in params:
        query['make'] = {'$regex': params['make'], '$options': 'i'}
    if 'model' in params:
        query['model'] = {'$regex': params['model'], '$options': 'i'}
    if 'variant' in params:
        query['description'] = {'$regex': params['variant'], '$options': 'i'}  # Assume variant in desc
    if 'year_min' in params or 'year_max' in params:
        query['year'] = {}
        if 'year_min' in params:
            query['year']['$gte'] = int(params['year_min'])
        if 'year_max' in params:
            query['year']['$lte'] = int(params['year_max'])
    if 'price_min' in params or 'price_max' in params:
        if 'price_min' in params:
            query['price_range.low'] = {'$gte': int(params['price_min'])}
        if 'price_max' in params:
            query['price_range.high'] = {'$lte': int(params['price_max'])}
    if 'state' in params:
        query['location'] = {'$regex': params['state'], '$options': 'i'}
    if 'auction_house' in params:
        query['source'] = {'$regex': params['auction_house'], '$options': 'i'}
    if 'no_reserve' in params and params['no_reserve']:
        query['reserve'] = 'No'
    if 'body_style' in params:
        query['body_style'] = {'$regex': params['body_style'], '$options': 'i'}
    if 'transmission' in params:
        query['transmission'] = {'$regex': params['transmission'], '$options': 'i'}
    if 'newly_added' in params:
        try:
            hours = int(params['newly_added'][:-1])
            time_ago = datetime.now() - timedelta(hours=hours)
            query['scrape_time'] = {'$gte': time_ago}
        except:
            pass
    if 'title' in params and params['title'].strip():
        # Case-insensitive partial match on title
        query['title'] = {'$regex': params['title'].strip(), '$options': 'i'}
    return query

def scrape_all():
    all_lots = []
    scrape_start = datetime.utcnow()
    for source in SOURCES:
        lots = scrape_site(source)
        all_lots.extend(lots)
    
    for lot in all_lots:
        lot['scrape_time'] = datetime.utcnow()
        lot['auction_date'] = normalize_auction_date(lot.get('auction_date'))
        if not lot.get('url'):
            lot['url'] = f"{lot.get('source','unknown')}/{uuid.uuid4()}"
        lots_collection.update_one(
            {'url': lot['url']},
            {'$set': lot, '$setOnInsert': {'first_scraped': scrape_start}},
            upsert=True
        )
    
    now = datetime.now()
    ended = lots_collection.find({'auction_date': {'$lt': now}})
    for end in list(ended):
        house = end['source']
        prem = house_premiums.get(house, 0.15)
        hammer = end.get('price_range', {}).get('high', 0)  # Placeholder for final hammer
        total = hammer * (1 + prem)
        sold_doc = dict(end)
        sold_doc['hammer_price'] = hammer
        sold_doc['buyers_premium'] = prem * 100
        sold_doc['total_price'] = total
        sold_collection.insert_one(sold_doc)
        lots_collection.delete_one({'_id': end['_id']})
    
    two_years_ago = now - timedelta(days=730)
    sold_collection.delete_many({'auction_date': {'$lt': two_years_ago}})
    
    check_alerts(scrape_start)

def check_alerts(scrape_start):
    for saved in saved_searches_collection.find():
        user_id = saved['user_id']
        params = {k: v for k, v in saved.items() if k not in ['_id', 'user_id']}
        query = build_query(params)
        matches = lots_collection.find({**query, 'first_scraped': {'$gte': scrape_start}})
        match_list = list(matches)
        if match_list:
            titles = [m.get('title', m.get('make', '') + ' ' + m.get('model', '')) for m in match_list]
            message = f"New matching cars added: {', '.join(titles)}\nView at AusClassicAuctions.com.au"
            send_alert(user_id, message)

# Scheduler
scheduler = BackgroundScheduler()
scheduler.add_job(scrape_all, 'interval', hours=4)
scheduler.start()

@app.route('/api/scrape', methods=['POST'])
@swag_from({
    'tags': ['Admin'],
    'summary': 'Trigger manual scrape',
    'security': [{'Bearer': []}],
    'responses': {
        '200': {'description': 'Scraping completed'}
    }
})
# @jwt_required()
def manual_scrape():
    scrape_all()
    return jsonify({'message': 'Scraping completed'})

@app.route('/api/register', methods=['POST'])
@swag_from({
    'tags': ['Users'],
    'summary': 'Register a new user',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['email', 'password']
            }
        }
    ],
    'responses': {
        '200': {'description': 'User registered'},
        '400': {'description': 'User already exists'}
    }
})
def register():
    data = request.json
    email = data['email']
    password = data['password']  # Hash in production
    if users_collection.find_one({'email': email}):
        return jsonify({'error': 'User exists'}), 400
    user_id = users_collection.insert_one({'email': email, 'password': password}).inserted_id
    user = User(str(user_id), email)
    login_user(user)
    return jsonify({'message': 'Registered'})

@app.route('/api/login', methods=['POST'])
@swag_from({
    'tags': ['Users'],
    'summary': 'Login user',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string'},
                    'password': {'type': 'string'}
                },
                'required': ['email', 'password']
            }
        }
    ],
    'responses': {
        '200': {'description': 'Login successful, token returned'},
        '401': {'description': 'Invalid credentials'}
    }
})
def login():
    data = request.json
    email = data['email']
    password = data['password']
    user_doc = users_collection.find_one({'email': email, 'password': password})
    if user_doc:
        user = User(str(user_doc['_id']), email)
        login_user(user)
        access_token = create_access_token(identity=str(user_doc['_id']))
        return jsonify({'token': access_token})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/logout')
@swag_from({
    'tags': ['Users'],
    'summary': 'Logout user',
    'responses': {
        '200': {'description': 'Logged out'}
    }
})
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out'})

@app.route('/api/calendar', methods=['GET'])
@swag_from({
    'tags': ['Auctions'],
    'summary': 'Get auction calendar',
    'parameters': [
        {'name': 'state', 'in': 'query', 'type': 'string', 'description': 'Filter by state'},
        {'name': 'month', 'in': 'query', 'type': 'string', 'description': 'Filter by month (YYYY-MM)'},
        {'name': 'auction_house', 'in': 'query', 'type': 'string', 'description': 'Filter by auction house'},
        {'name': 'online_only', 'in': 'query', 'type': 'boolean', 'description': 'Filter online only'}
    ],
    'responses': {
        '200': {'description': 'List of upcoming auctions'}
    }
})
def calendar():
    now = datetime.now()
    match = {'auction_date': {'$gte': now, '$lt': now + timedelta(days=90)}}
    if state := request.args.get('state'):
        match['location'] = {'$regex': state, '$options': 'i'}
    if month := request.args.get('month'):
        try:
            start = datetime.strptime(month + '-01', '%Y-%m-%d')
            end = (start.replace(month=start.month % 12 + 1) if start.month == 12 else start.replace(month=start.month + 1)) - timedelta(days=1)
            match['auction_date'] = {'$gte': start, '$lte': end}
        except:
            pass
    if auction_house := request.args.get('auction_house'):
        match['source'] = {'$regex': auction_house, '$options': 'i'}
    if request.args.get('online_only') == 'true':
        match['location'] = 'Online'
    
    pipeline = [
        {'$match': match},
        {'$group': {'_id': {'date': '$auction_date', 'source': '$source', 'location': '$location'}, 'num_lots': {'$sum': 1}}},
        {'$sort': {'_id.date': 1}}
    ]
    results = list(lots_collection.aggregate(pipeline))
    formatted = [
        {
            'date': r['_id']['date'],
            'house': r['_id']['source'],
            'location': r['_id']['location'],
            'num_lots': r['num_lots']
        } for r in results
    ]
    return jsonify(formatted)
@app.route('/api/search', methods=['GET'])
@swag_from({
    'tags': ['Auctions'],
    'summary': 'Search for lots with pagination',
    'parameters': [
        {'name': 'make', 'in': 'query', 'type': 'string'},
        {'name': 'model', 'in': 'query', 'type': 'string'},
        {'name': 'title', 'in': 'query', 'type': 'string', 'description': 'Search in lot title (partial match, case-insensitive)'},
        {'name': 'variant', 'in': 'query', 'type': 'string'},
        {'name': 'year_min', 'in': 'query', 'type': 'integer'},
        {'name': 'year_max', 'in': 'query', 'type': 'integer'},
        {'name': 'price_min', 'in': 'query', 'type': 'integer'},
        {'name': 'price_max', 'in': 'query', 'type': 'integer'},
        {'name': 'state', 'in': 'query', 'type': 'string'},
        {'name': 'auction_house', 'in': 'query', 'type': 'string'},
        {'name': 'no_reserve', 'in': 'query', 'type': 'boolean'},
        {'name': 'body_style', 'in': 'query', 'type': 'string'},
        {'name': 'transmission', 'in': 'query', 'type': 'string'},
        {'name': 'newly_added', 'in': 'query', 'type': 'string', 'description': 'e.g., 24h'},
        
        # Sorting
        {'name': 'sort', 'in': 'query', 'type': 'string', 'description': 'e.g., auction_date asc, price desc'},
        
        # ← Pagination parameters (NEW)
        {'name': 'page', 'in': 'query', 'type': 'integer', 'default': 1, 'description': 'Page number (starts from 1)'},
        {'name': 'limit', 'in': 'query', 'type': 'integer', 'default': 20, 'description': 'Items per page (max 100 recommended)'},
    ],
    'responses': {
        '200': {
            'description': 'Paginated search results',
            'schema': {
                'type': 'object',
                'properties': {
                    'results': {'type': 'array', 'items': {'type': 'object'}},
                    'pagination': {
                        'type': 'object',
                        'properties': {
                            'page': {'type': 'integer'},
                            'limit': {'type': 'integer'},
                            'total': {'type': 'integer'},
                            'pages': {'type': 'integer'},
                            'has_next': {'type': 'boolean'},
                            'has_prev': {'type': 'boolean'}
                        }
                    }
                }
            }
        }
    }
})
def search():
    params = request.args.to_dict()

    # ── Pagination parameters ───────────────────────────────
    try:
        page = int(params.get('page', 1))
        limit = int(params.get('limit', 20))
    except ValueError:
        page = 1
        limit = 20

    # Safety limits
    page = max(1, page)
    limit = max(1, min(100, limit))  # don't allow crazy values

    skip = (page - 1) * limit

    # ── Build query & sorting ────────────────────────────────
    query = build_query(params)

    sort_str = params.get('sort', 'auction_date asc')
    sort_parts = sort_str.split()

    # Support multiple fields sorting (price desc, year asc, etc)
    sort_list = []
    i = 0
    while i < len(sort_parts):
        field = sort_parts[i]
        direction = 1  # asc by default

        if i + 1 < len(sort_parts) and sort_parts[i + 1].lower() in ('asc', 'desc'):
            direction = 1 if sort_parts[i + 1].lower() == 'asc' else -1
            i += 2
        else:
            i += 1

        sort_list.append((field, direction))

    if not sort_list:
        sort_list = [('auction_date', 1)]  # fallback

    # ── Execute query with pagination ────────────────────────
    total = lots_collection.count_documents(query)
    cursor = (
        lots_collection
        .find(query)
        .sort(sort_list)
        .skip(skip)
        .limit(limit)
    )

    results = [
        {**doc, '_id': str(doc['_id'])}
        for doc in cursor
    ]

    # ── Prepare response ─────────────────────────────────────
    total_pages = ceil(total / limit) if limit > 0 else 1

    response = {
        "results": results,
        "pagination": {
            "page": page,
            "limit": limit,
            "total": total,
            "pages": total_pages,
            "has_next": page < total_pages,
            "has_prev": page > 1
        }
    }

    return jsonify(response), 200
@app.route('/api/lot/<lot_id>', methods=['GET'])
@swag_from({
    'tags': ['Auctions'],
    'summary': 'Get individual lot details',
    'parameters': [
        {'name': 'lot_id', 'in': 'path', 'type': 'string', 'required': True}
    ],
    'responses': {
        '200': {'description': 'Lot details'},
        '404': {'description': 'Not found'}
    }
})
def get_lot(lot_id):
    lot = lots_collection.find_one({'_id': ObjectId(lot_id)})
    if not lot:
        return jsonify({'error': 'Not found'}), 404
    lot['_id'] = str(lot['_id'])
    lot['provenance'] = extract_provenance(lot.get('description', ''))
    related = sold_collection.find({
        'make': lot['make'],
        'model': lot['model'],
        'year': lot['year']
    }).limit(5)
    lot['related'] = [dict(rel, **{'_id': str(rel['_id'])}) for rel in related]
    return jsonify(lot)

@app.route('/api/watchlist', methods=['GET', 'POST'])
@swag_from({
    'tags': ['Users'],
    'summary': 'Manage watchlist',
    'security': [{'Bearer': []}],
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': False,
            'schema': {
                'type': 'object',
                'properties': {
                    'lot_id': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        '200': {'description': 'Watchlist or added message'}
    }
})
@jwt_required()
def watchlist():
    user_id = get_jwt_identity()
    if request.method == 'POST':
        lot_id = request.json.get('lot_id')
        watchlists_collection.update_one(
            {'user_id': user_id},
            {'$addToSet': {'lots': ObjectId(lot_id)}},
            upsert=True
        )
        return jsonify({'message': 'Added'})
    
    watch = watchlists_collection.find_one({'user_id': user_id})
    if watch:
        lot_ids = watch['lots']
        upcoming = list(lots_collection.find({'_id': {'$in': lot_ids}}))
        sold = list(sold_collection.find({'_id': {'$in': lot_ids}}))
        all_lots = upcoming + sold
        now = datetime.now()
        for l in all_lots:
            l['_id'] = str(l['_id'])
            if l.get('auction_date', now) < now:
                l['status'] = 'sold'
            else:
                l['status'] = 'upcoming'
        return jsonify(all_lots)
    return jsonify([])

@app.route('/api/saved_searches', methods=['GET', 'POST'])
@swag_from({
    'tags': ['Users'],
    'summary': 'Manage saved searches',
    'security': [{'Bearer': []}],
    'responses': {
        '200': {'description': 'Saved searches or saved message'}
    }
})
@jwt_required()
def saved_searches():
    user_id = get_jwt_identity()
    if request.method == 'POST':
        search_params = request.json
        saved_searches_collection.insert_one({'user_id': user_id, **search_params})
        return jsonify({'message': 'Saved'})
    
    searches = saved_searches_collection.find({'user_id': user_id})
    return jsonify([dict(s, **{'_id': str(s['_id'])}) for s in searches])

def send_alert(user_id, message):
    user = users_collection.find_one({'_id': ObjectId(user_id)})
    if user:
        smtp_server = os.getenv('SMTP_SERVER')
        smtp_port = int(os.getenv('SMTP_PORT', 587))
        sender = os.getenv('SENDER_EMAIL')
        password = os.getenv('SENDER_PASSWORD')
        
        msg = MIMEText(message)
        msg['Subject'] = 'Auction Alert'
        msg['From'] = sender
        msg['To'] = user['email']
        
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender, password)
            server.sendmail(sender, user['email'], msg.as_string())

@app.route('/api/sold', methods=['GET'])
@swag_from({
    'tags': ['Auctions'],
    'summary': 'Get sold prices archive',
    'parameters': [
        {'name': 'make', 'in': 'query', 'type': 'string'},
        {'name': 'model', 'in': 'query', 'type': 'string'},
        {'name': 'year', 'in': 'query', 'type': 'integer'}
    ],
    'responses': {
        '200': {'description': 'Sold lots'}
    }
})
def sold():
    params = request.args.to_dict()
    if 'year' in params:
        params['year'] = int(params['year'])
    query = build_query(params)
    results = sold_collection.find(query).sort('auction_date', -1)
    return jsonify([dict(r, **{'_id': str(r['_id'])}) for r in results])

@app.route('/api/market_pulse', methods=['GET'])
@swag_from({
    'tags': ['Auctions'],
    'summary': 'Get market pulse data',
    'responses': {
        '200': {'description': 'Top sales and risers'}
    }
})
def market_pulse():
    now = datetime.now()
    month_start = now - timedelta(days=30)
    top_sales = sold_collection.find({'auction_date': {'$gte': month_start}}).sort('total_price', -1).limit(10)
    top_sales_list = [dict(s, **{'_id': str(s['_id'])}) for s in top_sales]
    
    pipeline = [
        {'$match': {'auction_date': {'$gte': month_start}}},
        {'$group': {'_id': {'make': '$make', 'model': '$model'}, 'avg_price': {'$avg': '$total_price'}, 'count': {'$sum': 1}}},
        {'$sort': {'avg_price': -1}},
        {'$limit': 10}
    ]
    risers = list(sold_collection.aggregate(pipeline))
    return jsonify({'top_sales': top_sales_list, 'risers': risers})

@app.route('/api/on_the_block', methods=['GET'])
@swag_from({
    'tags': ['Auctions'],
    'summary': 'Get lots closing soon',
    'responses': {
        '200': {'description': 'Live lots'}
    }
})
def on_the_block():
    now = datetime.now()
    two_hours = now + timedelta(hours=2)
    live = lots_collection.find({'auction_date': {'$gte': now, '$lt': two_hours}})
    return jsonify([dict(l, **{'_id': str(l['_id'])}) for l in live])

@app.route('/api/auction_houses', methods=['GET'])
@swag_from({
    'tags': ['Auctions'],
    'summary': 'Get auction houses directory',
    'responses': {
        '200': {'description': 'List of auction houses'}
    }
})
def auction_houses():
    now = datetime.now()
    houses = list(lots_collection.aggregate([{'$group': {'_id': '$source', 'upcoming': {'$sum': 1}}}]))
    directory = []
    for h in houses:
        name = h['_id']
        premium = house_premiums.get(name, 0.15) * 100
        directory.append({
            'name': name,
            'upcoming': h['upcoming'],
            'buyers_premium': f"{premium}%"
        })
    return jsonify(directory)

# Initial scrape
# scrape_all()

if __name__ == '__main__':
    app.run(debug=False, port=9007)