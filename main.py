import os
import instaloader
import requests
from datetime import datetime

# Instagram credentials
USERNAME = "anilkumar65483"
TARGET_USERS = [
    "priya_raj_455ps",
    "chhoti_queen_paswan",
    "annu_238q",
    "akhsuna_raj_",
    "mr_king_sani_302",
    "singerguriyaraj",
    "sinnu_sharma_2796",
    "arjun_raja_4758_",
    "miss__you__jan_91",
    "piyush_king_8377",
    "mr__surya____702"
]

# Telegram credentials
TELEGRAM_BOT_TOKEN = "6579507408:AAFsFtDKUZVAuJIRldZ3StYpOrO7oV9qPp4"
TELEGRAM_CHAT_ID = "2037302383"

# Instaloader setup
L = instaloader.Instaloader()
L.load_session_from_file(USERNAME)

def download_and_send_stories(username):
    try:
        profile = instaloader.Profile.from_username(L.context, username)

        for story in L.get_stories(userids=[profile.userid]):
            for item in story.get_items():
                # स्टोरी का टाइम फॉर्मेट
                story_time = datetime.fromtimestamp(item.date_utc.timestamp()).strftime("%Y-%m-%d %H:%M:%S")
                
                # स्टोरी डाउनलोड करें
                L.download_storyitem(item, username)

                # डाउनलोड फाइल को सेंड करें
                for file in os.listdir(f"{username}"):
                    if file.endswith(".jpg") or file.endswith(".mp4"):
                        file_path = os.path.join(username, file)

                        # टेलीग्राम पर कैप्शन के साथ सेंड करें
                        caption = f"📷 *{username}* ki story\n🕒 Post time: {story_time}"
                        send_to_telegram(file_path, caption)

                        os.remove(file_path)  # स्टोरी भेजने के बाद फाइल डिलीट करें

    except Exception as e:
        print(f"Error downloading {username}'s story: {e}")

def send_to_telegram(file_path, caption):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendDocument"
    
    with open(file_path, "rb") as f:
        response = requests.post(
            url,
            data={"chat_id": TELEGRAM_CHAT_ID, "caption": caption, "parse_mode": "Markdown"},
            files={"document": f}
        )
    print(response.json())

# सभी यूज़र्स की स्टोरी को डाउनलोड और सेंड करें
for user in TARGET_USERS:
    download_and_send_stories(user)
