from core.notifier import notify

notify(
    symbol="TEST",
    price=123.45,
    rating={"buy": 8, "sell": 0},
    rsi=25.1,
    action="🚨 הודעת בדיקה בלבד",
    news="This is a simulated alert for test purposes",
    score=5,
    reasons=[
        "📉 RSI נמוך",
        "✅ המלצת אנליסטים",
        "🔁 נפח חריג"
    ]
)
