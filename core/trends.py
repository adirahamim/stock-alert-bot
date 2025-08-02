
def get_trending_tickers():
    # סימולציה זמנית – בפועל יש לפרוס כאן חיבור ל-Google Trends או Finviz
    return ["NVDA", "AAPL", "AMD"]


def get_trend_score(symbol):
    trending = get_trending_tickers()
    return 1 if symbol in trending else 0
