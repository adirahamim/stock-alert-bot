core.py – כולל את הלוגיקה של הבוט (גרסה משודרגת)

import requests import time import datetime import pytz import matplotlib.pyplot as plt import csv from settings import TELEGRAM_TOKEN, CHAT_IDS, TWELVE_API, FINNHUB_API, TOTAL_BUDGET, ALLOCATED, stocks, USE_ANALYST_RATING, TEST_MODE, USE_RSI, ALPHA_VANTAGE_API, USE_NEWS, NEWS_API, USE_MACD, USE_VOLUME_SPIKE, TRADER_PROFILE

last_summary_time = None already_reported = {} MAX_PRICE_HISTORY = 50 CSV_LOG_PATH = "signals_log.csv"

def is_market_open(): if TEST_MODE: return True now = datetime.datetime.now(pytz.timezone('America/New_York')) return now.weekday() < 5 and datetime.time(9, 30) <= now.time() <= datetime.time(16, 0)

def send_telegram(msg): url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage" for chat_id in CHAT_IDS: requests.post(url, data={"chat_id": chat_id, "text": msg})

def send_telegram_image(image_path, caption=""): url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendPhoto" for chat_id in CHAT_IDS: with open(image_path, "rb") as image_file: requests.post(url, files={"photo": image_file}, data={"chat_id": chat_id, "caption": caption})

def get_price(symbol): try: url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={TWELVE_API}" res = requests.get(url).json() return float(res["price"]) if "price" in res else None except: return None

def get_rating(symbol): try: url = f"https://finnhub.io/api/v1/stock/recommendation?symbol={symbol}&token={FINNHUB_API}" res = requests.get(url).json() return res[0] if res else {"buy": 0, "hold": 0, "sell": 0} except: return {"buy": 0, "hold": 0, "sell": 0}

def get_rsi(symbol): if not USE_RSI: return None try: url = f"https://taapi.p.sulu.sh/rsi?exchange=NASDAQ&symbol={symbol}&interval=1d" res = requests.get(url).json() return float(res.get("value", 50)) except: return None

def get_macd(symbol): try: url = f"https://finnhub.io/api/v1/indicator?symbol={symbol}&resolution=1&indicator=macd&token={FINNHUB_API}" r = requests.get(url).json() macd_val = r["macd"]["macd"][-1] signal_val = r["macd"]["signal"][-1] return round(macd_val - signal_val, 4) except: return None

def get_volume_spike(symbol): try: url = f"https://finnhub.io/api/v1/stock/candle?symbol={symbol}&resolution=1&count=30&token={FINNHUB_API}" r = requests.get(url).json() if r.get("v") and len(r["v"]) >= 10: last_volume = r["v"][-1] avg_volume = sum(r["v"][-10:-1]) / 9 return last_volume > avg_volume * 1.5 return False except: return False

def get_ema(symbol, period): try: url = f"https://finnhub.io/api/v1/indicator?symbol={symbol}&resolution=1&indicator=ema&timeperiod={period}&token={FINNHUB_API}" r = requests.get(url).json() return round(r["ema"]["values"][-1], 2) except: return None

def get_news_summary(symbol): if not USE_NEWS: return None try: url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API}&language=en&sortBy=publishedAt&pageSize=1" res = requests.get(url).json() if res["articles"]: return res["articles"][0]["title"] except: return None

def create_graph(symbol, prices): if len(prices) < 2: return plt.figure() plt.plot(prices, marker='o') plt.title(f"{symbol} – Last Prices") plt.axhline(y=stocks[symbol]["low"], color='green', linestyle='--', label='Support') plt.axhline(y=stocks[symbol]["high"], color='red', linestyle='--', label='Resistance') plt.legend() path = f"{symbol}.png" plt.savefig(path) plt.close() return path

def log_to_csv(symbol, price, action): with open(CSV_LOG_PATH, mode='a', newline='') as file: writer = csv.writer(file) writer.writerow([datetime.datetime.now().isoformat(), symbol, price, action])

def decide_action(symbol, price, rating, rsi): recommendation = "" available = TOTAL_BUDGET - sum(ALLOCATED.values()) amount_to_buy = min(available, 1000)

macd = get_macd(symbol) if USE_MACD else None
volume_spike = get_volume_spike(symbol) if USE_VOLUME_SPIKE else False
ema20 = get_ema(symbol, 20)
ema50 = get_ema(symbol, 50)
ema200 = get_ema(symbol, 200)

if macd and macd > 0 and volume_spike:
    recommendation = "🚀 MACD חיובי + spike בנפח – אפשרות קנייה חזקה"
elif ema20 and ema50 and ema200 and ema20 > ema50 > ema200:
    recommendation = "📊 EMA20 > EMA50 > EMA200 – מגמת עלייה ברורה"
elif price <= stocks[symbol]["low"]:
    recommendation = f"🖍️ ירידה לאזור קנייה - שקול לרכוש ב־${amount_to_buy:.0f}"
    ALLOCATED[symbol] = ALLOCATED.get(symbol, 0) + amount_to_buy
elif price >= stocks[symbol]["high"]:
    if TRADER_PROFILE == "aggressive":
        recommendation = "💥 פריצה מעל התנגדות – כניסה אגרסיבית"
    else:
        recommendation = "📈 פריצה – כניסה מותנית באישור נוסף"
elif USE_ANALYST_RATING and rating.get("buy", 0) >= 7 and rating.get("sell", 0) == 0:
    recommendation = f"✅ המלצת אנליסטים חזקה – {rating['buy']} קנייה"
elif rating.get("sell", 0) >= 4:
    recommendation = "🚨 המלצת מכירה חזקה – שקול לצאת"

if USE_RSI and rsi is not None:
    if rsi < 30:
        recommendation += "\n📉 RSI נמוך – ייתכן oversold"
    elif rsi > 70:
        recommendation += "\n📈 RSI גבוה – ייתכן overbought"

return recommendation or "🕒 המתנה – אין איתות חזק כרגע"

def run_bot(): global last_summary_time print("✅ הבוט פועל... בודק מניות בדיוק מקסימלי") send_telegram("🚀 הבוט התחיל לרוץ – מצב דיוק מקסימלי פעיל")

for symbol in stocks:
    already_reported[symbol] = None

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
        rsi = get_rsi(symbol)
        news = get_news_summary(symbol)
        action = decide_action(symbol, price, rating, rsi)

        log_to_csv(symbol, price, action)

        msg = (
            f"📌 {symbol} – ${price:.2f}\n"
            f"אנליסטים 🔍 – קנייה: {rating['buy']} | המתנה: {rating['hold']} | מכירה: {rating['sell']}\n"
            f"RSI: {rsi if rsi is not None else 'N/A'}\n"
            f"{action}"
        )
        if news:
            msg += f"\n🗞️ חדשות אחרונות: {news}"

        graph_path = create_graph(symbol, stocks[symbol]["prices"])
        if graph_path:
            send_telegram_image(graph_path, msg)
        else:
            send_telegram(msg)

        already_reported[symbol] = msg
        time.sleep(10)

    now = datetime.datetime.now(pytz.timezone('America/New_York'))
    if not last_summary_time or (now - last_summary_time).seconds > 3600:
        last_summary_time = now
        send_telegram("✅ עדכון בוצע – כל המניות נבדקו שוב")

    time.sleep(60)

