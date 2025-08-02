from core.ai_scorer import score
from core.fetcher import get_price
from settings import stocks

print("🔍 Scanning market for hot stocks...")

symbols = ["NVDA", "AAPL", "AMD"]  # תוכל להרחיב כרצונך

for symbol in symbols:
    try:
        price = get_price(symbol)
        if not price:
            continue

        if "prices" not in stocks[symbol]:
            stocks[symbol]["prices"] = []
        stocks[symbol]["prices"].append(price)
        if len(stocks[symbol]["prices"]) > 50:
            stocks[symbol]["prices"] = stocks[symbol]["prices"][-50:]

        prices = stocks[symbol].get("prices", [])

        score_val = score({
            "price": price,
            "low": stocks[symbol]["low"],
            "high": stocks[symbol]["high"],
            "sentiment": 0,
            "trend_score": 0
        }, prices=prices)

        print(f"{symbol} → ${price} | AI Score: {score_val}")

    except Exception as e:
        print(f"⚠️ שגיאה בסריקת {symbol}: {e}")
