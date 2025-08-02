
import time
from core.fetcher import get_price
from core.ai_scorer import score
from core.notifier import send_alert
from core.trends import get_trending_tickers

def explore_market():
    print("🔍 Scanning market for hot stocks...")
    tickers = get_trending_tickers()
    for symbol in tickers:
        try:
            price = get_price(symbol)
            data = {
                "price": price,
                "low": price * 0.93,
                "high": price * 1.07,
                "sentiment": 1,
                "trend_score": 1
            }
            stock_score = score(data)
            if stock_score >= 85:
                send_alert(symbol, price, stock_score, reason="איתות חם מהשוק")
        except Exception as e:
            print(f"⚠️ שגיאה בסריקת {symbol}: {e}")

if __name__ == "__main__":
    explore_market()


# tickers = ["NVDA"]  # בדיקה ידנית
# for symbol in tickers:
#     price = 135.0
#     data = {
#         "price": price,
#         "low": 130.0,
#         "high": 150.0,
#         "sentiment": 1,
#         "trend_score": 1
#     }
#     stock_score = score(data)
#     print(f"ציון עבור {symbol}: {stock_score}")
#     if stock_score >= 85:
#         send_alert(symbol, price, stock_score, reason="איתות בדיקה ידני")
