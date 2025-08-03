
def get_sentiment(symbol, news_items):
    positive_words = ["gain", "rise", "strong", "positive", "growth", "up", "upgrade", "buy", "beat"]
    negative_words = ["fall", "drop", "weak", "negative", "loss", "down", "cut", "sell", "miss"]

    score = 0
    count = 0
    for item in news_items or []:
        text = (item.get("headline") or "").lower()
        if any(word in text for word in positive_words):
            score += 1
        elif any(word in text for word in negative_words):
            score -= 1
        count += 1

    if count == 0:
        return 0

    return round(score / count, 2)
