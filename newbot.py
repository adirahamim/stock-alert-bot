import requests
import time
import datetime
import pytz
import matplotlib.pyplot as plt
import os
from dotenv import load_dotenv
from settings import TELEGRAM_TOKEN, CHAT_ID, TWELVE_API, FINNHUB_API, TOTAL_BUDGET, ALLOCATED, stocks, USE_ANALYST_RATING, USE_RSI, USE_NEWS

# טען משתני סביבה מהקובץ .env
load_dotenv()

last_summary_time = None


def is_market_open():
    now = datetime.datetime.now(pytz.timezone('America/New_York'))
    return now.weekday() < 5 and datetime.time(9, 30) <= now.time() <= datetime.time(16, 0)


def send_telegram(msg):
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        res = requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
        if res.status_code != 200:
            print(f"Telegram error: {res.text}")
    except Exception as e:
        print(f"❗ שגיאה בשליחת הודעת טלגרם: {e}")


def get_rating(symbol):
    try:
        if not USE_ANALYST_RATING:
            return {"buy": 0, "hold": 0, "sell": 0}
        url = f"https://finnhub.io/api/v1/stock/recommendation?symbol={symbol}&token={FINNHUB_API}"
        res = requests.get(url).json()
        return res[0] if res else {"buy": 0, "hold": 0, "sell": 0}
    except Exception as e:
        print(f"❗ שגיאה ב־get_rating({symbol}): {e}")
        return {"buy": 0, "hold": 0, "sell": 0}


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
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={TWELVE_API}"
        res = requests.get(url).json()
        return float(res["price"]) if "price" in res else None
    except Exception as e:
        print(f"❗ שגיאה ב־get_price({symbol}): {e}")
        return None


def decide_action(symbol, price, rating):
    recommendation = ""
    available = TOTAL_BUDGET - sum(ALLOCATED.values())
    amount_to_buy = min(available, 1000)

    if price <= stocks[symbol]["low"]:
        recommendation = f"📉 ירידה לאזור קנייה - שקול לרכוש ב־${amount_to_buy:.0f}"
        ALLOCATED[symbol] = ALLOCATED.get(symbol, 0) + amount_to_buy

    elif price >= stocks[symbol]["high"]:
        recommendation = "📈 פריצה מעל התנגדות - אפשרות לכניסה (לסוחרים אגרסיביים)"

    elif rating.get("buy", 0) >= 7 and rating.get("sell", 0) == 0:
        recommendation = f"✅ המלצת אנליסטים חזקה – {rating['buy']} קנייה, מומלץ לשקול רכישה"

    elif rating.get("sell", 0) >= 4:
        recommendation = "🚨 המלצת מכירה חזקה – שקול לצאת מהפוזיציה"

    return recommendation or "🕒 המתנה – אין איתות חזק כרגע"


def run():
    global last_summary_time
    print("✅ הבוט פועל... בודק מניות")

    while True:
        if not is_market_open():
            print("📴 הבורסה סגורה. ממתין...")
            time.sleep(300)
            continue

        for symbol in stocks:
            price = get_price(symbol)
            if not price:
                continue
            stocks[symbol]["last"] = price
            stocks[symbol]["prices"].append(price)
            rating = get_rating(symbol)
            avg_price = sum(stocks[symbol]["prices"]) / len(stocks[symbol]["prices"])
            action = decide_action(symbol, price, rating)

            msg = (
                f"📌 {symbol} – ${price:.2f} (ממוצע: ${avg_price:.2f})\n"
                f"אנליסטים 🔍 – קנייה: {rating['buy']} | המתנה: {rating['hold']} | מכירה: {rating['sell']}\n"
                f"{action}"
            )
            send_telegram(msg)
            create_graph(symbol, stocks[symbol]["prices"])
            time.sleep(10)

        now = datetime.datetime.now(pytz.timezone('America/New_York'))
        if not last_summary_time or (now - last_summary_time).seconds > 3600:
            last_summary_time = now
            send_telegram("✅ עדכון בוצע – כל המניות נבדקו שוב")
        time.sleep(60)


if __name__ == "__main__":
    run()
