import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os
from telegram import Bot
import asyncio

# 🔑 Secrets (Render / Google Cloud Run için environment variable üzerinden alınıyor)
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
TCF_URL = "https://www.tcf.gov.tr/branslar/pilates/#kurs"

bot = Bot(token=TELEGRAM_BOT_TOKEN)

# 🔹 08.08.2025 sonrası kurslar dikkate alınacak
REFERENCE_DATE = datetime.strptime("08.08.2025", "%d.%m.%Y")


def fetch_courses():
    response = requests.get(TCF_URL, timeout=10)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")

    # Kurs bölümündeki satırları bul
    kurslar = soup.select("tr")  # tabloda <tr> direkt var
    upcoming_courses = []

    for row in kurslar:
        cols = [c.get_text(strip=True) for c in row.find_all("td")]
        if not cols or len(cols) < 3:
            continue

        title = cols[0]
        city = cols[1]
        date_text = cols[2]  # Örn: "15.09.2025 - 20.09.2025"

        # Link varsa al
        link = ""
        if len(cols) > 3:
            a_tag = row.find("a")
            if a_tag and a_tag.get("href"):
                link = a_tag["href"]

        # Tarih ayıklama
        try:
            start_date_str = date_text.split(" - ")[0]
            start_date = datetime.strptime(start_date_str, "%d.%m.%Y")
        except Exception:
            continue

        # Filtre: referans tarihinden sonraki kurslar
        if start_date >= REFERENCE_DATE:
            msg = f"{title}\n{city}\nTarih: {date_text}\n{link}"
            upcoming_courses.append(msg)

    return upcoming_courses


async def send_telegram(messages):
    for msg in messages:
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=msg)


if __name__ == "__main__":
    courses = fetch_courses()
    print("Bulunan kurs sayısı:", len(courses))  # debug çıktısı

    if courses:
        asyncio.run(send_telegram(courses))
    else:
        # Eğer hiç kurs bulunmazsa burası isteğe bağlı
        # asyncio.run(send_telegram(["Yeni kurs bulunamadı."]))
        pass
