
from core.ai_scorer import score
from core.fetcher import get_price
from core.scanner import get_stock_candidates
from core.notifier import send_candidate_to_telegram
from settings import stocks

print("🔍 Scanning market for hot stocks...")

symbols = get_stock_candidates()

for symbol in symbols:
    try:
        price = get_price(symbol)
        if not price:
            continue

        # If stock doesn't exist in settings, create a temporary entry
        if symbol not in stocks:
            stocks[symbol] = {
                "low": None,
                "high": None,
                "buy_price": None,
                "last": None,
                "prices": []
            }

        stocks[symbol]["prices"].append(price)
        if len(stocks[symbol]["prices"]) > 50:
            stocks[symbol]["prices"] = stocks[symbol]["prices"][-50:]

        prices = stocks[symbol]["prices"]

        score_val = score({
            "price": price,
            "low": stocks[symbol]["low"],
            "high": stocks[symbol]["high"],
            "sentiment": 0,
            "trend_score": 0
        }, prices=prices)

        if score_val >= 85:
            print(f"{symbol} → ${price} | AI Score: {score_val} ✅")
            send_candidate_to_telegram(symbol, price, score_val)
        else:
            print(f"{symbol} → ${price} | AI Score: {score_val}")

    except Exception as e:
        print(f"⚠️ שגיאה בסריקת {symbol}: {e}")
