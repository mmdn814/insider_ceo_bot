import requests
from bs4 import BeautifulSoup
from config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
from datetime import datetime

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    response = requests.post(url, data=data)
    return response.json()

def fetch_ceo_buys():
    url = "http://openinsider.com/screener?s=&o=&pl=&ph=&ll=&lh=&fd=1&td=0&xp=1&vl=&vh=&sicMin=&sicMax=&insider=CEO&sortcol=0&cnt=50"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    resp = requests.get(url, headers=headers)
    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.find("table", class_="tinytable")

    results = []

    if not table:
        return results

    rows = table.find_all("tr")[1:]  # Skip header
    for row in rows:
        cols = row.find_all("td")
        if len(cols) < 10:
            continue

        ticker = cols[1].text.strip()
        owner = cols[5].text.strip()
        title = cols[6].text.strip()
        trade_type = cols[7].text.strip()
        price = cols[8].text.strip()
        qty = cols[9].text.strip()
        date = cols[0].text.strip()

        if trade_type != "P - Purchase":
            continue  # 只保留公开市场买入

        results.append({
            "ticker": ticker,
            "ceo": owner,
            "buy_price": price,
            "shares": qty,
            "date": date
        })

    return results

def main():
    ceo_buys = fetch_ceo_buys()

    if not ceo_buys:
        send_telegram_message("😕 今天没有 CEO 买入记录")
        return

    messages = ["🚨 *今日 CEO 买入股票列表*"]
    for stock in ceo_buys[:5]:  # 取前 5 条展示
        msg = f"""\n*Ticker:* {stock['ticker']}
*CEO:* {stock['ceo']}
*Buy Price:* {stock['buy_price']}
*Shares:* {stock['shares']}
*Date:* {stock['date']}
[查看 Fintel](https://fintel.io/s/us/{stock['ticker'].lower()})"""
        messages.append(msg)

    final_msg = "\n\n".join(messages)
    send_telegram_message(final_msg)

if __name__ == "__main__":
    main()
