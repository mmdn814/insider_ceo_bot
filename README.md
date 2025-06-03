# insider_ceo_bot
| 功能                                       | 说明 |
| ---------------------------------------- | -- |
| ⏰ 每天美东时间 8:30（UTC 13:30）自动运行             |    |
| 📥 抓取 OpenInsider 上 CEO 最新买入记录           |    |
| 🧠 自动分析结构特征（低价 / low float / insider 控盘） |    |
| 📤 把潜在“RGC 式”股票推送到你的 Telegram            |    |

1、main.py：实现如下功能：
抓取 OpenInsider CEO 买入记录（过去24小时）
过滤出低价小市值票（<20美元，买入股数较大）
调用 Fintel 页面爬取：float、insider ownership
对每个标的评分、排序
将前几名结果推送至你的 Telegram

2、config.py：你只需填写你的：
Telegram Bot Token
Chat ID（我会告诉你怎么获取）

3、.github/workflows/run-daily.yml：

每天美东时间 8:30 运行脚本（UTC 13:30）
