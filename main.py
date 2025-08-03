import subprocess
subprocess.Popen(["python", "listener.py"])  # הפעלת listener ברקע

from core.fetcher import get_price, get_rating, get_rsi, get_macd, get_ema, get_volume_spike, get_news
from core.strategy import decide_action
from core.ai_scorer import score
from core.sentiment import get_sentiment
from core.trends import get_trend_score
from core.notifier import notify
from core.utils import get_active_market
from runtime_manager import save_runtime_data, load_runtime_data
from settings import stocks, FILTER_NO_SIGNAL
from core.utils import should_run_now

import time
from core.utils import calculate_buy_amount

from settings import TOTAL_BUDGET


already_sent = {}
last_save_time = time.time()

def main_loop():
    load_runtime_data(stocks)
    
    from core.utils import should_run_now


    while True:
        if not should_run_now():
            print("⏳ שוק סגור – המתנה של דקה...")
            time.sleep(60)
            continue
            active_market = get_active_market()
            if active_market == "CLOSED":
                print("Markets closed – waiting...")
                time.sleep(60)
                continue

        for symbol in stocks:
            if active_market == "IL" and not symbol.endswith(".TA"):
                continue
            if active_market == "US" and symbol.endswith(".TA"):
                continue

            price = get_price(symbol)
            rating = get_rating(symbol)
            rsi = get_rsi(symbol)
            macd = get_macd(symbol)
            ema20 = get_ema(symbol, 20)
            ema50 = get_ema(symbol, 50)
            ema200 = get_ema(symbol, 200)
            volume_spike = get_volume_spike(symbol)
            news = get_news(symbol)

            if price:
                stocks[symbol]["last"] = price
                stocks[symbol]["prices"].append(price)
                if len(stocks[symbol]["prices"]) > 50:
                    stocks[symbol]["prices"] = stocks[symbol]["prices"][-50:]

            action, reasons = decide_action(symbol, price, rating, rsi, macd, ema20, ema50, ema200, volume_spike)
            score = score({
                "price": price,
                "low": stocks[symbol]["low"],
                "high": stocks[symbol]["high"],
                "sentiment": get_sentiment(symbol, news),
                "trend_score": get_trend_score(symbol)
            }, prices=stocks[symbol].get("prices", []))

            print(f"{symbol} | Price: {price} | Action: {action} | Score: {score}")
            if action and (not FILTER_NO_SIGNAL or "no strong signal" not in action):
                if already_sent.get(symbol) != action:
                    notify(symbol, price, rating, rsi, action, news, score, reasons)
                    already_sent[symbol] = action

            time.sleep(5)

        global last_save_time
        if time.time() - last_save_time > 600:
            save_runtime_data(stocks)
            last_save_time = time.time()

if __name__ == "__main__":
    main_loop()
