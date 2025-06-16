# insider_ceo_bot v3.2.2




🚀 新版修订说明：
- ✅ 核心逻辑使用 Filing Date 精准过滤每日披露，避免漏单与时间误差；
- ✅ 其它逻辑稳定继承 v3.2.1 全部评分与推送机制。
- ✅ 修改时间 6/16/2025
- ✅ 修改文件 ceo_purchase_scraper.py



🚀 **全自动 CEO Insider Buy 筛选系统 + 结构评分 + Squeeze评分 (稳定生产版)**

> 实时追踪美股市场 CEO 买入行为，结合结构评分与逼空评分，自动推送到 Telegram，每日扫描潜力股，寻找下一只 RGC。

---

## 🌟 系统功能亮点

- ✅ 每日自动抓取最新 CEO 公开市场买入（OpenInsider 数据源）
- ✅ 兜底防漏逻辑（抓取最近 3 天 Filing Date 避免漏单）
- ✅ 买入数量前 20 名筛选
- ✅ 结构评分 (Structure Score) 自动计算
- ✅ 逼空评分 (Squeeze Score) 自动计算
- ✅ 完整容错、自动重试、防反爬虫机制
- ✅ Telegram 实时推送提醒
- ✅ 云端 GitHub Actions 定时调度

---

## 📊 评分逻辑详解

### 结构评分 (Structure Score)

| 条件 | 评分逻辑 |
|--|--|
| Insider Ownership > 60% | +1 |
| Institutional Ownership < 20% | +1 |
| Float < 20M shares | +1 |
| **满分：3/3** | 越高控盘性越强 |

### 逼空评分 (Squeeze Score)

| 条件 | 评分逻辑 |
|--|--|
| Short Interest > 10% | +1 |
| Short Interest > 20% | 再+1 |
| Float < 20M shares | +1 |
| Insider Ownership > 60% | +1 |
| **满分：4/4** | 越高越可能短线逼空爆发 |

---

## 📦 文件结构

```bash
insider_ceo_bot/
│
├── .github/workflows/run-daily.yml   # GitHub Actions 定时任务配置
├── requirements.txt                  # Python依赖包
├── config.py                         # Telegram 配置文件 (含 TOKEN & CHAT_ID)
├── ceo_purchase_scraper.py           # 爬虫核心逻辑 (OpenInsider)
├── fintel_structure.py               # 结构评分逻辑 (Fintel数据抓取与评分)
├── telegram_push.py                  # Telegram 推送模块
├── main.py                           # 主控逻辑文件
└── README.md                         # 当前文档

💻 GitHub Actions 定时调度
配置文件：.github/workflows/run-daily.yml
默认每天 UTC 13:30（美东 8:30 开盘前 1 小时）

🚀 运行效果示例
Telegram 每日推送样式：
🚨 今日 CEO 买入数量前 20 名
📈 Ticker: RGC
👤 CEO: Yat-Gai Au
🧮 Shares: +652,982
💰 Buy Price: $9.50
💰 Buy Amount: $6,203,329
🏦 Insider: 65.4%
🏦 Institutional: 21.7%
🧮 Float: 12.8M
🔻 Short Interest: 18.5%
⭐ Structure Score: 3/3
🔥 Squeeze Score: 3/4
📅 Date: 2025-03-10
🔗 [Fintel Link](https://fintel.io/s/us/rgc)

