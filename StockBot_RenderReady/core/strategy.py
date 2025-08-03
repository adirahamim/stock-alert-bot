def decide_action(symbol, price, rating, rsi, macd, ema20, ema50, ema200, volume_spike):
    reasons = []
    recommendation = ""

    if price is None:
        return "אין מחיר זמין", reasons

    if ema200 is not None and price <= ema200 and macd and macd > 0 and volume_spike:
        reasons.append("📈 MACD חיובי + spike בנפח")
        recommendation = "איתות קנייה חזק – פריצה מתחת ל־EMA200"

    if rsi is not None and rsi < 30:
        reasons.append("📉 RSI נמוך – ייתכן oversold")

    if ema50 is not None and price <= ema50:
        reasons.append("🔽 ירידה לאזור קנייה – מתחת EMA50")

    if rating and rating.get("buy", 0) >= 7 and rating.get("sell", 0) == 0:
        reasons.append(f"✅ המלצת אנליסטים חזקה – {rating['buy']} קנייה")

    if volume_spike:
        reasons.append("🔁 נפח גבוה מהרגיל")

    if not reasons:
        return "אין איתות חזק כרגע", reasons

    return recommendation or "📊 נרשמו מספר תנאים חיוביים", reasons


def score_signal(price, low, rsi, macd, rating, volume_spike, ema20, ema50, ema200):
    score = 0
    if price is None:
        return score

    if price <= low:
        score += 2
    if rsi is not None and rsi < 30:
        score += 1
    if macd is not None and macd > 0:
        score += 1
    if volume_spike:
        score += 1
    if rating and rating.get("buy", 0) >= 5 and rating.get("sell", 0) == 0:
        score += 1

    return score
