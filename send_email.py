"""通用发信函数：从环境变量读配置，发 HTML 邮件。"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
from email.utils import formataddr


def send_html_email(subject: str, html_body: str, from_name: str = "豆包行业日报"):
    smtp_host = "smtp.qq.com"
    smtp_port = 465
    sender = "290704926@qq.com"
    auth_code = os.environ.get("QQ_AUTH_CODE", "")
    recipients = os.environ.get("RECIPIENTS", "290704926@qq.com").split(",")
    recipients = [r.strip() for r in recipients if r.strip()]

    if not auth_code:
        raise RuntimeError("环境变量 QQ_AUTH_CODE 未设置")

    msg = MIMEMultipart()
    msg["From"] = formataddr((str(Header(from_name, "utf-8")), sender))
    msg["To"] = ", ".join(recipients)
    msg["Subject"] = Header(subject, "utf-8")
    msg.attach(MIMEText(html_body, "html", "utf-8"))

    with smtplib.SMTP_SSL(smtp_host, smtp_port) as s:
        s.login(sender, auth_code)
        s.sendmail(sender, recipients, msg.as_string())

    print(f"[send] OK -> {recipients}")
