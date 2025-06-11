from ceo_purchase_scraper import CEOPurchaseScraper
from telegram_push import send_telegram_message
from fintel_structure import FintelStructureScorer

def main():
    scraper = CEOPurchaseScraper()
    scorer = FintelStructureScorer()

    try:
        results = scraper.fetch_data()
    except Exception as e:
        send_telegram_message(f"🚨 爬虫整体失败: {e}")
        return

    if not results:
        send_telegram_message("😕 今天没有 CEO 买入记录")
        return

    messages = ["🚨 *今日 CEO 买入数量前 20 名*"]
    for stock in results[:20]:
        try:
            fintel_data = scorer.get_fintel_data(stock['ticker'])
            if fintel_data:
                structure_score = scorer.compute_structure_score(fintel_data)
                squeeze_score = scorer.compute_squeeze_score(fintel_data)
                msg = f"""\n📈 *Ticker:* `{stock['ticker']}`
👤 *CEO:* {stock['ceo']}
🧮 *Shares:* +{stock['shares']}
💰 *Buy Price:* ${stock['price']}
💰 *Buy Amount:* ${stock['value']:,.0f}
🏦 Insider: {fintel_data['insider']}%
🏦 Institutional: {fintel_data['institutional']}%
🧮 Float: {fintel_data['float']}M
🔻 Short Interest: {fintel_data['short_interest']}%
⭐ Structure Score: {structure_score}/3
🔥 Squeeze Score: {squeeze_score}/4
📅 Date: {stock['trade_date']}
🔗 [Fintel Link](https://fintel.io/s/us/{stock['ticker'].lower()})"""
            else:
                msg = f"\n📈 *Ticker:* `{stock['ticker']}`\n⚠ 无法获取结构评分数据"

            messages.append(msg)

        except Exception as e:
            send_telegram_message(f"🚨 Fintel 抓取异常: {stock['ticker']} -> {e}")
            continue

    final_msg = "\n\n".join(messages)
    send_telegram_message(final_msg)

if __name__ == "__main__":
    main()
