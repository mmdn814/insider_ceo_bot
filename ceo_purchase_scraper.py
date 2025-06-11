import requests
from bs4 import BeautifulSoup
from datetime import datetime
import time

class CEOPurchaseScraper:
    def __init__(self, pages=10):
        self.base_url = "http://openinsider.com/screener"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        self.pages = pages

    def get_today_date(self):
        return datetime.now().strftime('%Y-%m-%d')

    def parse_value(self, val_str):
        if not val_str or val_str == '--':
            return 0
        clean_str = val_str.replace('$', '').replace(',', '').replace('+', '')
        try:
            return float(clean_str)
        except:
            return 0

    def parse_shares(self, qty_str):
        try:
            return int(qty_str.replace(',', '').replace('+', ''))
        except:
            return 0

    def fetch_data(self):
        today = self.get_today_date()
        results = []

        for page in range(1, self.pages+1):
            params = {
                'fd': '1',
                'td': '0',
                'xp': '1',
                'xs': '1',
                'vl': '100',
                'insider': 'CEO',
                'sortcol': 0,
                'cnt': 100,
                'page': page
            }

            try:
                resp = requests.get(self.base_url, params=params, headers=self.headers)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.content, 'html.parser')
                table = soup.find('table', {'class': 'tinytable'})
                if not table:
                    break

                rows = table.find_all('tr')[1:]
                if not rows:
                    break

                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) < 10:
                        continue

                    trade_date = cells[2].get_text(strip=True)
                    ticker = cells[3].get_text(strip=True)
                    insider_name = cells[5].get_text(strip=True)
                    title = cells[6].get_text(strip=True)
                    trade_type = cells[7].get_text(strip=True)
                    price = cells[8].get_text(strip=True)
                    qty = cells[9].get_text(strip=True)
                    value = cells[12].get_text(strip=True) if len(cells) > 12 else ''
                    detail_link = ''
                    link_cell = cells[0].find('a')
                    if link_cell:
                        detail_link = 'http://openinsider.com' + link_cell['href']

                    if ('CEO' not in title.upper()) or ('P' not in trade_type):
                        continue

                    if today not in trade_date:
                        continue

                    shares_int = self.parse_shares(qty)
                    value_float = self.parse_value(value)

                    results.append({
                        'trade_date': trade_date,
                        'ticker': ticker,
                        'ceo': insider_name,
                        'shares': qty,
                        'shares_int': shares_int,
                        'price': price,
                        'value': value_float,
                        'detail_link': detail_link
                    })

            except Exception as e:
                print(f"Error parsing page {page}: {e}")
                time.sleep(1)
                continue

            time.sleep(0.5)

        results.sort(key=lambda x: x['shares_int'], reverse=True)
        return results
