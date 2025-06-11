# insider_ceo_bot v3.2.1

🚀 **全自动 CEO Insider Buy 筛选系统 + 结构评分 + Squeeze评分**

> 实时追踪美股市场 CEO 买入行为，结合结构评分与逼空评分，自动推送到 Telegram，每日帮你扫描潜力股，寻找下一只 RGC。

---

## 🌟 系统功能亮点

- ✅ 每天自动抓取最新 CEO 公开市场买入（OpenInsider 数据）
- ✅ 对买入数量前 20 名进行结构评分 (Structure Score)
- ✅ 自动计算逼空评分 (Squeeze Score)
- ✅ 集成完整容错、自动重试、防反爬机制
- ✅ Telegram 实时推送提醒
- ✅ 长期稳定运行、支持云端 GitHub Actions 定时调度

---

## 📊 评分逻辑详解

### 结构评分 (Structure Score)

| 条件 | 评分逻辑 |
|--|--|
| Insider Ownership > 60% | +1 |
| Institutional Ownership < 20% | +1 |
| Float < 20M shares | +1 |
| **满分：3/3** | 越高结构控盘性越强 |

### Squeeze评分 (简化版)

| 条件 | 评分逻辑 |
|--|--|
| Short Interest > 10% | +1 |
| Short Interest > 20% | 再+1 |
| Float < 20M shares | +1 |
| Insider Ownership > 60% | +1 |
| **满分：4/4** | 越高越可能短线逼空爆发 |

---

## 📦 文件结构
.github/workflows/run-daily.yml # GitHub Actions定时任务
requirements.txt # Python依赖文件
config.py # Telegram 配置文件
main.py # 主控制逻辑
ceo_purchase_scraper.py # 爬取OpenInsider数据
fintel_structure.py # 爬取Fintel并计算结构评分
telegram_push.py # 发送Telegram通知
README.md # 当前文档

3️⃣ GitHub Actions 定时调度
示例文件已包含 .github/workflows/run-daily.yml，可设置为每天固定时间自动运行。

推荐时间：
美东时间 8:30 (美股开盘前1小时)


🚨 容错与防反爬设计
| 模块             | 容错设计                       |
| -------------- | -------------------------- |
| OpenInsider 爬虫 | 重试 3 次 + 超时控制              |
| Fintel 爬虫      | 重试 3 次 + 单票失败不影响整体执行       |
| 全局异常           | 任何异常自动 Telegram 报警         |
| 频率控制           | 每票请求间隔 0.5 秒，防止被 Fintel 风控 |

🚀 运行效果示例
Telegram 每日推送示例：
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


🔒 免责声明
本项目仅供学习研究，数据来源为公开站点，实际投资请谨慎使用。
请勿高频恶意爬取以避免违反数据源站点服务协议。
