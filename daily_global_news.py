"""每日全球新闻日报：抓 RSS 源，生成 HTML，发邮件。"""
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime

from send_email import send_html_email


RSS_SOURCES = [
    ("BBC 中文", "https://feeds.bbci.co.uk/zhongwen/simp/rss.xml"),
    ("路透中文", "https://www.reuters.com/arc/outboundfeeds/rss/?outputType=xml"),
    ("联合早报", "https://www.zaobao.com.sg/rss/realtime"),
]


def fetch_rss(url: str, timeout: int = 15):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def parse_items(xml_bytes: str, max_items: int = 10):
    items = []
    try:
        root = ET.fromstring(xml_bytes)
        for item in root.iter("item"):
            title = item.findtext("title", "").strip()
            link = item.findtext("link", "").strip()
            desc = item.findtext("description", "").strip()
            pub = item.findtext("pubDate", "").strip()
            if title and link:
                items.append({"title": title, "link": link, "desc": desc[:200], "pub": pub})
            if len(items) >= max_items:
                break
    except Exception as e:
        print(f"[warn] parse failed: {e}", file=sys.stderr)
    return items


def build_html(all_news: dict) -> str:
    today = datetime.now().strftime("%Y-%m-%d")
    total = sum(len(v) for v in all_news.values())
    cards = []
    for source, items in all_news.items():
        cards.append(f'<div style="margin-bottom:18px;">')
        cards.append(f'<div style="font-size:13px;font-weight:bold;color:#14283d;margin-bottom:8px;border-left:3px solid #ff6a1a;padding-left:8px;">{source}（{len(items)} 条）</div>')
        for it in items:
            cards.append(
                f'<div style="margin-bottom:10px;padding:6px 0;">'
                f'<a href="{it["link"]}" style="color:#14283d;font-size:13px;font-weight:bold;text-decoration:underline;">{it["title"]}</a>'
                f'</div>'
            )
        cards.append("</div>")

    return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"></head>
<body style="margin:0;padding:0;background:#f4f5f7;font-family:'Microsoft YaHei',Arial;">
<div style="max-width:720px;margin:0 auto;background:#fff;padding:28px;">
  <div style="border-bottom:3px solid #14283d;padding-bottom:14px;margin-bottom:20px;">
    <div style="font-size:12px;color:#ff6a1a;letter-spacing:2px;font-weight:bold;">DAILY GLOBAL NEWS · {today}</div>
    <h1 style="margin:8px 0 6px 0;font-size:22px;color:#14283d;">每日全球新闻 · {total} 条要闻</h1>
  </div>
  {''.join(cards)}
  <div style="margin-top:24px;padding-top:14px;border-top:1px solid #e0e0e0;font-size:11px;color:#999;">
    来源：BBC 中文 / 路透中文 / 联合早报 RSS · {today} · Gitee Go 云端自动生成
  </div>
</div></body></html>"""


def main():
    today = datetime.now().strftime("%Y-%m-%d")
    all_news = {}
    for name, url in RSS_SOURCES:
        try:
            xml_bytes = fetch_rss(url)
            items = parse_items(xml_bytes, max_items=10)
            if items:
                all_news[name] = items
                print(f"[ok] {name}: {len(items)} items")
        except Exception as e:
            print(f"[fail] {name}: {e}", file=sys.stderr)

    total = sum(len(v) for v in all_news.values())
    if total == 0:
        print("[error] no news fetched", file=sys.stderr)
        sys.exit(1)

    html = build_html(all_news)
    send_html_email(
        subject=f"【每日全球新闻】{today} · {total} 条要闻速递",
        html_body=html,
        from_name="每日全球新闻",
    )


if __name__ == "__main__":
    main()
