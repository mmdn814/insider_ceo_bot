import requests
import time

class FintelStructureScorer:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({'User-Agent': 'Mozilla/5.0'})

    def get_fintel_data(self, ticker):
        url = f"https://fintel.io/s/us/{ticker.lower()}"
        try:
            resp = self.session.get(url, timeout=10)
            resp.raise_for_status()
            html = resp.text

            insider = self.extract_percentage(html, 'Insider Ownership</a></td><td class="report">')
            institutional = self.extract_percentage(html, 'Institutional Ownership</a></td><td class="report">')
            float_val = self.extract_float(html, 'Float</a></td><td class="report">')
            short_interest = self.extract_percentage(html, 'Short Interest</a></td><td class="report">')

            # ✅ 容忍部分字段缺失
            data = {
                'insider': insider if insider is not None else 0,
                'institutional': institutional if institutional is not None else 0,
                'float': float_val if float_val is not None else 0,
                'short_interest': short_interest if short_interest is not None else 0
            }
            return data

        except Exception as e:
            print(f"Fintel 获取失败: {e}")
            return None

    def extract_percentage(self, html, label):
        try:
            idx = html.index(label) + len(label)
            percent_str = html[idx:idx+30].split('%')[0].strip().replace(',', '')
            return float(percent_str)
        except:
            return None

    def extract_float(self, html, label):
        try:
            idx = html.index(label) + len(label)
            val_str = html[idx:idx+30].split('M')[0].strip().replace(',', '')
            return float(val_str)
        except:
            return None

    def compute_structure_score(self, data):
        score = 0
        if data['insider'] > 60:
            score += 1
        if data['institutional'] < 20:
            score += 1
        if data['float'] < 20:
            score += 1
        return score

    def compute_squeeze_score(self, data):
        score = 0
        if data['short_interest'] > 10:
            score += 1
        if data['short_interest'] > 20:
            score += 1
        if data['float'] < 20:
            score += 1
        if data['insider'] > 60:
            score += 1
        return score
