import requests
import os

TOKEN = os.environ["TELEGRAM_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
APIFY_TOKEN = os.environ["APIFY_TOKEN"]

DATASET_ID = "Mgj9b1lgpnjVRa42Q"

url = f"https://api.apify.com/v2/datasets/{DATASET_ID}/items?token={APIFY_TOKEN}"

data = requests.get(url).json()

if not data:
    print("No data")
    exit()

latest_video = data[0]["id"]

with open("last_video.txt", "r") as f:
    old_video = f.read().strip()

if latest_video != old_video:

    profile = data[0]["authorMeta"]["profileUrl"]

    message = f"🎉 คลิปใหม่จาก TikTok\n\n{profile}"

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
