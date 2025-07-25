import requests import time import datetime import pytz import matplotlib.pyplot as plt import csv from settings import TELEGRAM_TOKEN, CHAT_IDS, TWELVE_API, FINNHUB_API, TOTAL_BUDGET, ALLOCATED, stocks, USE_ANALYST_RATING, USE_RSI, USE_MACD, USE_VOLUME_SPIKE, TEST_MODE, TRADER_PROFILE

last_summary_time = None already_reported = {} MAX_PRICE_HISTORY = 50 CSV_LOG_PATH = "signals_log.csv"

def is_market_open(): if TEST_MODE: return True now = datetime.datetime.now(pytz.timezone('America/New_York')) return now.weekday() < 5 and datetime.time(9, 30) <= now.time() <= datetime.time(16, 0)

def send_telegram(msg): url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage" for chat_id in CHAT_IDS: requests.post(url, data={"chat_id": chat_id, "text": msg})

def is_price_valid(price): return price is not None and 0 < price < 5000

def get_price(symbol): url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={TWELVE_API}" res = requests.get(url).json() return float(res["price"]) if "price" in res else None

def get_rating(symbol): url = f"https://finnhub.io/api/v1/stock/recommendation?symbol={symbol}&token={FINNHUB_API}" res = requests.get(url).json() return res[0] if res else {"buy": 0, "hold": 0, "sell": 0}

def get_rsi(symbol): url = f"https://finnhub.io/api/v1/indicator?symbol={symbol}&resolution=1&indicator=rsi&timeperiod=14&token={FINNHUB_API}" r = requests.get(url).json() if "rsi" in r and "values" in r["rsi"] and r["rsi"]["values"]: return round(r["rsi"]["values"][-1], 2) return None

def get_macd(symbol): url = f"https://finnhub.io/api/v1/indicator?symbol={symbol}&resolution=1&indicator=macd&token={FINNHUB_API}" r = requests.get(url).json() try: macd_val = r["macd"]["macd"][-1] signal_val = r["macd"]["signal"][-1] return round(macd_val - signal_val, 4) except: return None

def get_volume_spike(symbol): url = f"https://finnhub.io/api/v1/stock/candle?symbol={symbol}&resolution=1&count=30&token={FINNHUB_API}" r = requests.get(url).json() if r.get("v") and len(r["v"]) >= 2: last_volume = r["v"][-1] avg_volume = sum(r["v"][-10:-1]) / 9 return last_volume > avg_volume * 1.5 return False

def get_ema(symbol, period=20): url = f"https://finnhub.io/api/v1/indicator?symbol={symbol}&resolution=1&indicator=ema&timeperiod={period}&token={FINNHUB_API}" r = requests.get(url).json() try: return round(r["ema"]["values"][-1], 2) except: return None

def create_graph(symbol, prices): if len(prices) < 2: return plt.figure() plt.plot(prices, marker='o') plt.title(f"{symbol} – Last Prices") plt.axhline(y=stocks[symbol]["low"], color='green', linestyle='--', label='Support') plt.axhline(y=stocks[symbol]["high"], color='red', linestyle='--', label='Resistance') plt.legend() plt.savefig(f"{symbol}.png") plt.close()

def log_to_csv(symbol, price, action): with open(CSV_LOG_PATH, mode='a', newline='') as file: writer = csv.writer(file) writer.writerow([datetime.datetime.now().isoformat(), symbol, price, action])

def decide_action(symbol, price, rating): recommendation = "" available = TOTAL_BUDGET - sum(ALLOCATED.values()) amount_to_buy = min(available, 1000)

rsi = get_rsi(symbol) if USE_RSI else None
macd_diff = get_macd(symbol) if USE_MACD else None
volume_spike = get_volume_spike(symbol) if USE_VOLUME_SPIKE else False
ema20 = get_ema(symbol, 20)
ema50 = get_ema(symbol, 50)
ema200 = get_ema(symbol, 200)

if rsi and rsi < 30:
    recommendation = f"📉 RSI נמוך ({rsi}) – אולי במכירת יתר"
elif rsi and rsi > 70:
    recommendation = f"📈 RSI גבוה ({rsi}) – אולי קניית יתר"
elif macd_diff and macd_diff > 0.1 and volume_spike:
    recommendation = f"🚀 MACD חיובי ({macd_diff}), spike בנפח – מומנטום עולה, אפשרות קנייה"
elif ema20 and ema50 and ema200 and ema20 > ema50 > ema200:
    recommendation = f"📊 ממוצעים EMA20 > EMA50 > EMA200 – טרנד שורי קלאסי, אפשרות קנייה"
elif price <= stocks[symbol]["low"]:
    recommendation = f"🖍️ ירידה לאזור קנייה - שקול לרכוש ב־${amount_to_buy:.0f}"
    ALLOCATED[symbol] = ALLOCATED.get(symbol, 0) + amount_to_buy
elif price >= stocks[symbol]["high"]:
    if TRADER_PROFILE == "aggressive":
        recommendation = "💥 פריצה מעל התנגדות – כניסה אפשרית לסוחרים אגרסיביים"
    else:
        recommendation = "📈 פריצה – שקול כניסה רק באישור נוסף"
elif USE_ANALYST_RATING and rating.get("buy", 0) >= 7 and rating.get("sell", 0) == 0:
    recommendation = f"✅ המלצת אנליסטים חזקה – {rating['buy']} קנייה"
elif rating.get("sell", 0) >= 4:
    recommendation = "🚨 המלצת מכירה חזקה – שקול לצאת מהפוזיציה"

return recommendation or "🕒 המתנה – אין איתות חזק כרגע"

def run_bot(): global last_summary_time print("✅ הבוט מדויק – מופעל עם מצב דיוק מקסימלי") send_telegram("🚀 הבוט החל לרוץ (מצב דיוק מקסימלי)")

for symbol in stocks:
    already_reported[symbol] = None

while True:
    if not is_market_open():
        time.sleep(60)
        continue

    for symbol in stocks:
        price = get_price(symbol)
        if not is_price_valid(price):
            send_telegram(f"⚠️ מחיר לא תקין ל־{symbol}: {price}")
            continue

        stocks[symbol]["last"] = price
        stocks[symbol]["prices"].append(price)
        if len(stocks[symbol]["prices"]) > MAX_PRICE_HISTORY:
            stocks[symbol]["prices"] = stocks[symbol]["prices"][-MAX_PRICE_HISTORY:]

        rating = get_rating(symbol)
        action = decide_action(symbol, price, rating)
        log_to_csv(symbol, price, action)

        rsi = get_rsi(symbol) if USE_RSI else None
        rsi_display = f"RSI: {rsi}" if rsi else "RSI לא זמין"

        current_summary = (
            f"📌 {symbol} – ${price:.2f}\n"
            f"{rsi_display}\n"
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

