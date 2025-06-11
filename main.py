from ceo_purchase_scraper import CEOPurchaseScraper
from telegram_push import send_telegram_message

def main():
    scraper = CEOPurchaseScraper()
    try:
        results = scraper.fetch_data()
    except Exception as e:
        send_telegram_message(f"🚨 爬取发生严重错误: {e}")
        return

    if not results:
        send_telegram_message("😕 今天没有 CEO 买入记录")
        return

    messages = ["🚨 *今日 CEO 买入数量前 20 名*"]
    for stock in results[:20]:
        msg = f"""\n📈 *Ticker:* `{stock['ticker']}`
👤 *CEO:* {stock['ceo']}
🧮 *Shares:* +{stock['shares']}
💰 *Buy Price:* ${stock['price']}
📅 *Date:* {stock['trade_date']}
🔗 [查看 Fintel](https://fintel.io/s/us/{stock['ticker'].lower()})"""
        messages.append(msg)

    final_msg = "\n\n".join(messages)
    send_telegram_message(final_msg)

if __name__ == "__main__":
    main()
