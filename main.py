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
        city = cols[1].t
if __name__ == "__main__":
    send_telegram(["Test mesajı - bot doğru çalışıyor mu?"])
