# settings.py – קובץ הגדרות בלבד

# ✅ מפתחות API (נטענים מ־.env או ישירות לבדיקות)
import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
#CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
CHAT_IDS = [int(id.strip()) for id in os.getenv("TELEGRAM_CHAT_IDS", "").split(",") if id.strip()]
TWELVE_API = os.getenv("TWELVE_DATA_API_KEY")
FINNHUB_API = os.getenv("FINNHUB_API_KEY")
ALPHA_VANTAGE_API = os.getenv("ALPHA_VANTAGE_API")
NEWS_API = os.getenv("NEWS_API_KEY")

# ✅ תקציב וסכומים
TOTAL_BUDGET = 50000
ALLOCATED = {}

# ✅ מניות למעקב – ניתן להוסיף/לערוך
stocks = {
    "BBAI": {"low": 7.18, "high": 7.80, "buy_price": 7.20, "last": None, "prices": []},
    "SOUN": {"low": 11.40, "high": 12.00, "buy_price": 11.60, "last": None, "prices": []},
    "QS":   {"low": 12.00, "high": 13.00, "buy_price": 12.10, "last": None, "prices": []},
    "REKR": {"low": 1.30,  "high": 1.48,  "buy_price": 1.35,  "last": None, "prices": []},
    "QUIK": {"low": 6.10,  "high": 6.35,  "buy_price": 6.15,  "last": None, "prices": []},
    "GDX":  {"low": 52.50, "high": 54.00, "buy_price": 53.00, "last": None, "prices": []},
    "NVDA": {"low": 125.00, "high": 138.00, "buy_price": 130.00, "last": None, "prices": []},
    "TSLA": {"low": 450.00, "high": 480.00, "buy_price": 465.00, "last": None, "prices": []},
    "SHLD": {"low": 52.00, "high": 56.00, "buy_price": 53.50, "last": None, "prices": []},
    "SPY":  {"low": 550.00, "high": 575.00, "buy_price": 560.00, "last": None, "prices": []},
    "JOBY": {"low": 4.60, "high": 5.20, "buy_price": 4.90, "last": None, "prices": []},
    "RGTI": {"low": 1.10, "high": 1.40, "buy_price": 1.20, "last": None, "prices": []},
    "ENVX": {"low": 8.80, "high": 9.60, "buy_price": 9.10, "last": None, "prices": []}
}

# ✅ פיצ'רים מתקדמים – הפעל/כבה לפי הצורך
USE_ANALYST_RATING = True
USE_RSI = False
USE_NEWS = False
TEST_MODE = False
