# core.py – כולל את הלוגיקה של הבוט

import requests
import time
import datetime
import pytz
import matplotlib.pyplot as plt
from settings import TELEGRAM_TOKEN, CHAT_ID, TWELVE_API, FINNHUB_API, TOTAL_BUDGET, ALLOCATED, stocks, USE_ANALYST_RATING, TEST_MODE

last_summary_time = None
already_reported = {}
MAX_PRICE_HISTORY = 50  # שמור עד 50 נקודות מחיר אחרונות בלבד

def is_market_open():
    if TEST_MODE:
        return True
    now = datetime.datetime.now(pytz.timezone('America/New_York'))
    return now.weekday() < 5 and datetime.time(9, 30) <= now.time() <= datetime.time(16, 0)

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    print(f"🔄 שולח טלגרם: {msg}")
    response = requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
    print(f"🔍 תגובת טלגרם: {response.text}")

def get_rating(symbol):
    url = f"https://finnhub.io/api/v1/stock/recommendation?symbol={symbol}&token={FINNHUB_API}"
    res = requests.get(url).json()
    return res[0] if res else {"buy": 0, "hold": 0, "sell": 0}

def create_graph(symbol, prices):
    if len(prices) < 2:
        return
    plt.figure()
    plt.plot(prices, marker='o')
    plt.title(f"{symbol} – Last Prices")
    plt.axhline(y=stocks[symbol]["low"], color='green', linestyle='--', label='Support')
    plt.axhline(y=stocks[symbol]["high"], color='red', linestyle='--', label='Resistance')
    plt.legend()
    plt.savefig(f"{symbol}.png")
    plt.close()

def get_price(symbol):
    url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={TWELVE_API}"
    res = requests.get(url).json()
    return float(res["price"]) if "price" in res else None

def decide_action(symbol, price, rating):
    recommendation = ""
    available = TOTAL_BUDGET - sum(ALLOCATED.values())
    amount_to_buy = min(available, 1000)

    if price <= stocks[symbol]["low"]:
        recommendation = f"🖍️ ירידה לאזור קנייה - שקול לרכוש ב־${amount_to_buy:.0f}"
        ALLOCATED[symbol] = ALLOCATED.get(symbol, 0) + amount_to_buy

    elif price >= stocks[symbol]["high"]:
        recommendation = "📈 פריצה מעל התנגדות - אפשרות לכניסה (לסוחרים אגרסיביים)"

    elif USE_ANALYST_RATING and rating.get("buy", 0) >= 7 and rating.get("sell", 0) == 0:
        recommendation = f"✅ המלצת אנליסטים חזקה – {rating['buy']} קנייה, מומלץ לשקול רכישה"

    elif rating.get("sell", 0) >= 4:
        recommendation = "🚨 המלצת מכירה חזקה – שקול לצאת מהפוזיציה"

    return recommendation or "🕒 המתנה – אין איתות חזק כרגע"

def run_bot():
    global last_summary_time
    print("✅ הבוט פועל... בודק מניות")

    # שליחת בדיקת חיבור בתחילת הריצה
    send_telegram("🚀 הבוט התחיל לרוץ – מבצע בדיקת תקשורת")

    for symbol in stocks:
        already_reported[symbol] = None  # אתחול סטטוס קודם

    while True:
        if not is_market_open():
            time.sleep(60)
            continue

        for symbol in stocks:
            price = get_price(symbol)
            if not price:
                continue
            stocks[symbol]["last"] = price
            stocks[symbol]["prices"].append(price)

            if len(stocks[symbol]["prices"]) > MAX_PRICE_HISTORY:
                stocks[symbol]["prices"] = stocks[symbol]["prices"][-MAX_PRICE_HISTORY:]

            rating = get_rating(symbol)
            action = decide_action(symbol, price, rating)

            current_summary = (
                f"📌 {symbol} – ${price:.2f} (ממוצע: ${price:.2f})\n"
                f"אנליסטים 🔍 – קנייה: {rating['buy']} | המתנה: {rating['hold']} | מכירה: {rating['sell']}\n"
                f"{action}"
            )

            send_telegram(current_summary)
            already_reported[symbol] = current_summary

            create_graph(symbol, stocks[symbol]["prices"])
            time.sleep(10)

        now = datetime.datetime.now(pytz.timezone('America/New_York'))
        if not last_summary_time or (now - last_summary_time).seconds > 3600:
            last_summary_time = now
            send_telegram("✅ עדכון בוצע – כל המניות נבדקו שוב")

        time.sleep(60)
