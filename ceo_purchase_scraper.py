import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

class CEOPurchaseScraper:
    def __init__(self):
        self.base_url = "http://openinsider.com/screener"
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        self.max_retries = 3

    def get_today_date(self):
        return datetime.now().strftime('%Y-%m-%d')

    def get_valid_trade_dates(self):
        """
        生成允许的 Trade Date 日期区间（最近 7 天），防止因 SEC 延迟披露而漏单
        """
        today = datetime.now().date()
        valid_dates = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(8)]
        return valid_dates

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
        valid_trade_dates = self.get_valid_trade_dates()
        results = []

        params = {
            'fd': '3',  # Filing Date：最近3天
            'td': '0',
            'xp': '1',
            'xs': '1',
            'vl': '100',
            'insider': 'CEO',
            'sortcol': 0,
            'cnt': 500,
            'page': 1
        }

        session = requests.Session()
        retries = Retry(total=self.max_retries, backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retries)
        session.mount("http://", adapter)

        try:
            resp = session.get(self.base_url, params=params, headers=self.headers, timeout=10)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.content, 'html.parser')
            table = soup.find('table', {'class': 'tinytable'})
            if not table:
                return []

            rows = table.find_all('tr')[1:]
            if not rows:
                return []

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

                # 仍然做 CEO + P-Purchase 筛选
                if ('CEO' not in title.upper()) or ('P' not in trade_type):
                    continue

                # Trade Date 容错处理 (最近 4 天内的才接受)
                if trade_date not in valid_trade_dates:
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

            time.sleep(0.5)
        except Exception as e:
            print(f"爬虫异常: {e}")

        # 按买入数量排序，取前20名
        results.sort(key=lambda x: x['shares_int'], reverse=True)
        return results

