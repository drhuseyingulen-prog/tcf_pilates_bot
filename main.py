import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
from telegram import Bot

# Secrets üzerinden alıyoruz
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
TCF_URL = "https://www.tcf.gov.tr/branslar/pilates/"

bot = Bot(token=TELEGRAM_BOT_TOKEN)

# 08.08.2025 sonrası kurslar
REFERENCE_DATE = datetime.strptime("08.08.2025", "%d.%m.%Y")

def fetch_courses():
    response = requests.get(TCF_URL)
    soup = BeautifulSoup(response.text, "html.parser")
    
    table = soup.find("table", id="kurs")
    upcoming_courses = []

    if not table:
        return upcoming_courses

    for row in table.tbody.find_all("tr"):
        cols = row.find_all("td")
        if len(cols) < 3:
            continue
        
        title = cols[0].text.strip()
        city = cols[1].text.strip()
        date_text = cols[2].text.strip()  # Örn: "08.09.2025 - 13.09.2025"
        link = cols[3].find("a")["href"] if cols[3].find("a") else ""

        start_date_str = date_text.split(" - ")[0]
        start_date = datetime.strptime(start_date_str, "%d.%m.%Y")
        
        if start_date > REFERENCE_DATE:
            upcoming_courses.append(f"{title}\n{city}\nTarih: {date_text}\n{link}")

    return upcoming_courses

def send_telegram(messages):
    for msg in messages:
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)

if __name__ == "__main__":
    # 🔹 Test mesajı
    send_telegram(["✅ Test: Bot çalışıyor ve mesaj gönderebiliyor!"])

    # 🔹 Asıl kurs kontrolü
    courses = fetch_courses()
    if courses:
        send_telegram(courses)
