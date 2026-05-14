import requests
import os

LINE_TOKEN = os.getenv("LINE_TOKEN")
USER_ID = os.getenv("USER_ID")

sites = [
    {
        "name": "楽天ブックス",
        "url": "https://books.rakuten.co.jp/search?sitem=Switch+2"
    },
    {
        "name": "ビックカメラ",
        "url": "https://www.biccamera.com/"
    }
]

headers = {
    "User-Agent": "Mozilla/5.0"
}

found = []

for site in sites:
    try:
        r = requests.get(site["url"], headers=headers, timeout=10)

        text = r.text

        keywords = [
            "在庫あり",
            "カートに入れる",
            "注文可能"
        ]

        for k in keywords:
            if k in text:
                found.append(f'{site["name"]}\n{site["url"]}')
                break

    except Exception as e:
        print(e)

if found:
    msg = "Switch2 在庫復活！\n\n" + "\n\n".join(found)

    requests.post(
        "https://api.line.me/v2/bot/message/push",
        headers={
            "Authorization": f"Bearer {LINE_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "to": USER_ID,
            "messages": [
                {
                    "type": "text",
                    "text": msg
                }
            ]
        }
    )

    print("通知送信")
else:
    print("在庫なし")
