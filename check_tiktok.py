import requests
import os

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
APIFY_TOKEN = os.environ["APIFY_TOKEN"]

DATASET_ID = "wETdToDlHeo9et657"

url = f"https://api.apify.com/v2/datasets/{DATASET_ID}/items?token={APIFY_TOKEN}&format=json&clean=true"

data = requests.get(url).json()

print(data)

if isinstance(data, dict):
    print("Data is dict, not list")
    exit()

if not data:
    print("No data")
    exit()

latest = data[0]
latest_video = latest.get("id")

with open("last_video.txt", "r") as f:
    old_video = f.read().strip()

if latest_video != old_video:
    profile = latest.get("authorMeta", {}).get("profileUrl", "https://www.tiktok.com/@mokjuri")
    text = latest.get("text", "")

    message = f"🎉 คลิปใหม่จาก TikTok\n\nช่อง: @mokjuri\n{text}\n\n{profile}"

    requests.post(
        f"https://api.telegram.org/bot{TOKEN}/sendMessage",
        data={
            "chat_id": CHAT_ID,
            "text": message
        }
    )

    with open("last_video.txt", "w") as f:
        f.write(latest_video)

    print("New video detected")
else:
    print("No new video")
