import sys
import colorama
from colorama import Fore, Style
from core.ai_scorer import score
from core.fetcher import get_price
from settings import stocks
from core.scanner import get_stock_candidates
from core.notifier import send_candidate_to_telegram

colorama.init()

print(f"{'Symbol':<8} {'Price':<10} {'AI Score':<10}")
print("-" * 30)

symbols = get_stock_candidates()

for symbol in symbols:
    try:
        if symbol not in stocks:
            continue  # דילוג על סימבול שלא מופיע ב־settings

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

        if score_val >= 85:
            score_str = Fore.GREEN + str(score_val) + Style.RESET_ALL
        elif score_val >= 50:
            score_str = Fore.YELLOW + str(score_val) + Style.RESET_ALL
        else:
            score_str = Fore.RED + str(score_val) + Style.RESET_ALL

        print(f"{symbol:<8} ${price:<9.2f} {score_str:<10}")

        if score_val >= 85:
            send_candidate_to_telegram(symbol, price, score_val)

    except Exception as e:
        print(f"[ERROR] Scan error for {symbol}: {e}")
