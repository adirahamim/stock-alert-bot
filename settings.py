import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_IDS = [int(id.strip()) for id in os.getenv("TELEGRAM_CHAT_IDS", "").split(",") if id.strip()]
OWNER_CHAT_ID = 755385373
TWELVE_API = os.getenv("TWELVE_API")
FINNHUB_API = os.getenv("FINNHUB_API")
NEWS_API = os.getenv("NEWS_API")

VERBOSE_MODE = False  # אם True – הבוט ישלח גם "אין איתות"
TOTAL_BUDGET = 50000  # 💰 תקציב כולל לבוט
stocks = {
    "BBAI": {"low": 6.01, "high": 8.72, "buy_price": 7.36, "last": None, "prices": []},
    "SOUN": {"low": 9.71, "high": 13.56, "buy_price": 11.64, "last": None, "prices": []},
    "QS": {"low": 6.28, "high": 15.03, "buy_price": 10.66, "last": None, "prices": []},
    "REKR": {"low": 1.07, "high": 1.42, "buy_price": 1.25, "last": None, "prices": []},
    "QUIK": {"low": 5.88, "high": 7.24, "buy_price": 6.56, "last": None, "prices": []},
    "GDX": {"low": 50.35, "high": 54.78, "buy_price": 52.56, "last": None, "prices": []},
    "NVDA": {"low": 152.97, "high": 183.3, "buy_price": 168.14, "last": None, "prices": []},
    "TSLA": {"low": 288.77, "high": 338.0, "buy_price": 313.38, "last": None, "prices": []},
    "SHLD": {"low": 58.08, "high": 62.44, "buy_price": 60.26, "last": None, "prices": []},
    "SPY": {"low": 616.61, "high": 639.85, "buy_price": 628.23, "last": None, "prices": []},
    "JOBY": {"low": 9.56, "high": 18.55, "buy_price": 14.06, "last": None, "prices": []},
    "RGTI": {"low": 11.43, "high": 17.39, "buy_price": 14.41, "last": None, "prices": []},
    "ENVX": {"low": 9.9, "high": 16.49, "buy_price": 13.2, "last": None, "prices": []},
    "BMNR": {"low": 30.3, "high": 161.0, "buy_price": 95.65, "last": None, "prices": []},
    "ETH": {"low": 23.01, "high": 36.45, "buy_price": 29.73, "last": None, "prices": []},
    "AAPL": {"low": 201.5, "high": 216.23, "buy_price": 208.86, "last": None, "prices": []},
    "AMCR": {"low": 9.2, "high": 10.0, "buy_price": 9.6, "last": None, "prices": []},
    "AMD": {"low": 133.5, "high": 182.5, "buy_price": 158.0, "last": None, "prices": []},
    "AMZN": {"low": 212.8, "high": 236.53, "buy_price": 224.67, "last": None, "prices": []},
    "AVGO": {"low": 262.73, "high": 306.95, "buy_price": 284.84, "last": None, "prices": []},
    "BAC": {"low": 45.01, "high": 49.31, "buy_price": 47.16, "last": None, "prices": []},
    "BAX": {"low": 21.33, "high": 31.44, "buy_price": 26.38, "last": None, "prices": []},
    "BMY": {"low": 42.96, "high": 49.28, "buy_price": 46.12, "last": None, "prices": []},
    "CAG": {"low": 18.18, "high": 20.92, "buy_price": 19.55, "last": None, "prices": []},
    "CCL": {"low": 28.07, "high": 31.01, "buy_price": 29.54, "last": None, "prices": []},
    "CMCSA": {"low": 32.39, "high": 36.4, "buy_price": 34.39, "last": None, "prices": []},
    "CMG": {"low": 42.46, "high": 58.42, "buy_price": 50.44, "last": None, "prices": []},
    "CNC": {"low": 25.11, "high": 37.78, "buy_price": 31.44, "last": None, "prices": []},
    "CSX": {"low": 32.97, "high": 36.38, "buy_price": 34.67, "last": None, "prices": []},
    "CVS": {"low": 58.5, "high": 68.36, "buy_price": 63.43, "last": None, "prices": []},
    "DOW": {"low": 21.79, "high": 30.93, "buy_price": 26.36, "last": None, "prices": []},
    "EBAY": {"low": 75.12, "high": 92.79, "buy_price": 83.96, "last": None, "prices": []},
    "F": {"low": 10.68, "high": 11.97, "buy_price": 11.32, "last": None, "prices": []},
    "FCX": {"low": 38.34, "high": 48.96, "buy_price": 43.65, "last": None, "prices": []},
    "GOOG": {"low": 173.88, "high": 198.97, "buy_price": 186.42, "last": None, "prices": []},
    "TEVA.TA": {"low": 5500, "high": 5800, "buy_price": 5600, "last": None, "prices": []},
    "BEZQ.TA": {"low": 550, "high": 631.27, "buy_price": 560, "last": None, "prices": []},
    "POLI.TA": {"low": 6263.67, "high": 6600, "buy_price": 6400, "last": None, "prices": []},
    "LUMI.TA": {"low": 6200, "high": 6500, "buy_price": 6300, "last": None, "prices": []},
    "DSCT.TA": {"low": 3200, "high": 3400, "buy_price": 3300, "last": None, "prices": []},
    "CLIS.TA": {"low": 2200, "high": 17063.33, "buy_price": 2300, "last": None, "prices": []},
    "ICL.TA": {"low": 2200, "high": 2400, "buy_price": 2300, "last": None, "prices": []}
}

USE_ANALYST_RATING = True
USE_RSI = True
USE_MACD = True
USE_NEWS = True
USE_VOLUME_SPIKE = True

TEST_MODE = False  # אם True – הבוט לא ישלח התראות, רק ידפיס למסך
TRADER_PROFILE = "aggressive"
OWNER_CHAT_ID = 755385373 # מזהה הצ'אט של בעל הבוט
FILTER_NO_SIGNAL = True  # שליטה אם לסנן הודעות "אין איתות"
