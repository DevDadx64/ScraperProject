import requests
from bs4 import BeautifulSoup

def fetch_html(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/'
    }

    with requests.Session() as session:
        session.headers.update(headers)
        try:
            response = session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        except requests.HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')

def extract_prices(soup):
    prices = []
    for price in soup.find_all('span', 'PropertyCardWrapper__StyledPriceLine-srp__sc-16e8gqd-1 iMKTKr'):
        prices.append(price.text)
    return prices

def extract_locations(soup):
    locations = []
    for location in soup.find_all('a', 'StyledPropertyCardDataArea-c11n-8-84-3__sc-yipmu-0 jnnxAW property-card-link'):
        locations.append(location.text)
    return locations

def extract_size_sqft(soup):
    lot_sizes = []
    for lot_size in soup.find_all('ul', 'StyledPropertyCardHomeDetailsList-c11n-8-84-3__sc-1xvdaej-0 eYPFID'):
        parts = lot_size.text.split(' ')
        if len(parts) >= 3:
            # Adding commas between the elements
            formatted_text = ', '.join(parts)
            lot_sizes.append(formatted_text)
        else:
            lot_sizes.append(lot_size.text)  # In case of non-standard formats
    return lot_sizes


zip_code = '64776'
url = f'https://www.zillow.com/homes/{zip_code}/'
html_content = fetch_html(url)
prices = extract_prices(html_content)
locations = extract_locations(html_content)
sizeSqft = extract_size_sqft(html_content)
print(prices, locations, sizeSqft)