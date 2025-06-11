import requests
from bs4 import BeautifulSoup
import time

class FintelStructureScorer:

    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        self.max_retries = 3

    def get_fintel_data(self, ticker):
        url = f"https://fintel.io/s/us/{ticker.lower()}"
        attempt = 0

        while attempt < self.max_retries:
            try:
                resp = requests.get(url, headers=self.headers, timeout=10)
                resp.raise_for_status()
                soup = BeautifulSoup(resp.text, 'html.parser')

                insider = self.extract_percent(soup, 'Insider Ownership')
                institutional = self.extract_percent(soup, 'Institutional Ownership')
                float_shares = self.extract_float(soup, 'Float Shares')
                short_interest = self.extract_percent(soup, 'Short Interest')

                # 成功返回数据
                return {
                    'insider': insider,
                    'institutional': institutional,
                    'float': float_shares,
                    'short_interest': short_interest
                }

            except Exception as e:
                print(f"⚠ 抓取 {ticker} Fintel 失败 (第 {attempt+1} 次): {e}")
                attempt += 1
                time.sleep(1)

        # 超过最大重试次数仍失败，返回 None
        return None

    def extract_percent(self, soup, label):
        try:
            tag = soup.find("div", string=lambda x: x and label in x)
            if not tag: return None
            value = tag.find_next("div").get_text(strip=True)
            return float(value.replace('%','').replace(',',''))
        except:
            return None

    def extract_float(self, soup, label):
        try:
            tag = soup.find("div", string=lambda x: x and label in x)
            if not tag: return None
            value = tag.find_next("div").get_text(strip=True)
            return float(value.replace('M','').replace(',',''))
        except:
            return None

    def compute_structure_score(self, data):
        score = 0
        if data['insider'] and data['insider'] > 60: score += 1
        if data['institutional'] and data['institutional'] < 20: score += 1
        if data['float'] and data['float'] < 20: score += 1
        return score

    def compute_squeeze_score(self, data):
        score = 0
        if data['short_interest'] and data['short_interest'] > 10: score += 1
        if data['short_interest'] and data['short_interest'] > 20: score += 1
        if data['float'] and data['float'] < 20: score += 1
        if data['insider'] and data['insider'] > 60: score += 1
        return score
