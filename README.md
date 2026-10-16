# autoskill

云端自动跑的日报邮件任务（Gitee Go 定时触发）。

## 任务列表

| 任务 | 频率 | 脚本 |
|---|---|---|
| 每日全球新闻图文邮件 | 每天 08:00 | `daily_global_news.py` |
| 密炼机与自动化配料日报 | 每天 08:00 | `daily_rubber_report.py` |

## 环境变量（在 Gitee Go → 设置 → 私有变量里配置）

- `QQ_AUTH_CODE`：QQ 邮箱 SMTP 授权码
- `RECIPIENTS`：收件人，逗号分隔，例如 `290704926@qq.com,vivien.zhang@adson-tech.com`

## 本地测试

```powershell
$env:QQ_AUTH_CODE="你的授权码"
$env:RECIPIENTS="290704926@qq.com,vivien.zhang@adson-tech.com"
python daily_global_news.py
python daily_rubber_report.py
```
