# insider_ceo_bot
🚨 自动化抓取 CEO Insider 买入行为并推送至 Telegram 的系统。
| 功能                                       | 说明 |
| ---------------------------------------- | -- |
| ⏰ 每天美东时间 8:30（UTC 13:30）自动运行             |    |
| 📥 抓取 OpenInsider 上 CEO 最新买入记录           |    |
| 🧠 自动分析结构特征（低价 / low float / insider 控盘） |    |
| 📤 把潜在“RGC 式”股票推送到你的 Telegram            |    |


## 功能
- 每日美股开盘前 1 小时（美东时间 08:30）自动运行
- 获取 OpenInsider 中 CEO 买入记录
- 可扩展结构分析逻辑（float、short interest 等）
- 推送消息到 Telegram 个人账户

## 使用
1. Fork 本项目
2. 在 GitHub Actions 中启用 workflow
3. 修改 `config.py` 以使用你自己的 Telegram Token 与 Chat ID


1、main.py：实现如下功能：
抓取 OpenInsider CEO 买入记录（过去24小时）
过滤出低价小市值票（<20美元，买入股数较大）
调用 Fintel 页面爬取：float、insider ownership
对每个标的评分、排序
将前几名结果推送至你的 Telegram

2、config.py：
Telegram Bot Token
Chat ID

3、.github/workflows/run-daily.yml：
每天美东时间 8:30 运行脚本（UTC 13:30）
