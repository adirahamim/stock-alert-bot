import statistics

def calculate_std(prices):
    if len(prices) < 2:
        return 0
    return round(statistics.stdev(prices), 2)

def score_signal(price, low, rsi, macd, rating, volume_spike):
    score = 0
    if price is not None and low is not None and price <= low:
        score += 25
    if rsi is not None and rsi < 30:
        score += 20
    if macd is not None and macd > 0:
        score += 15
    if rating is not None and rating.get("buy", 0) >= 5:
        score += 20
    if volume_spike:
        score += 20
    return min(score, 100)

def score(stock_data):
    price = stock_data.get("price")
    low = stock_data.get("low")
    high = stock_data.get("high")
    sentiment = stock_data.get("sentiment", 0)
    trend_score = stock_data.get("trend_score", 0)

    if not price or not low or not high:
        return 0

    distance_to_buy = max(0, 1 - ((price - low) / (high - low)))
    base_score = distance_to_buy * 100

    sentiment_boost = sentiment * 10
    trend_boost = trend_score * 5

    final_score = base_score + sentiment_boost + trend_boost
    return round(final_score, 2)
