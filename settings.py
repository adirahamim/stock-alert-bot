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
    "ENVX": {"low": 8.80, "high": 9.60, "buy_price": 9.10, "last": None, "prices": []},
    "BMNR": {"low": 32.45, "high": 47.95, "buy_price": 35.55, "last": None, "prices": []},
    "ETH": {"low": 33.31, "high": 36.56, "buy_price": 33.96, "last": None, "prices": []},
    "AAPL": {"low": None, "high": None, "buy_price": None, "last": None, "prices": []},
    "AMCR": {"low": None, "high": None, "buy_price": None, "last": None, "prices": []},
    "AMD":  {"low": None, "high": None, "buy_price": None, "last": None, "prices": []},
    "AMZN": {"low": None, "high": None, "buy_price": None, "last": None, "prices": []},
    "AVGO": {"low": None, "high": None, "buy_price": None, "last": None, "prices": []},
    "BAC":  {"low": None, "high": None, "buy_price": None, "last": None, "prices": []},
    "BAX":  {"low": None, "high": None, "buy_price": None, "last": None, "prices": []},
    "BMY":  {"low": None, "high": None, "buy_price": None, "last": None, "prices": []},
    "CAG":  {"low": None, "high": None, "buy_price": None, "last": None, "prices": []},
    "CCL":  {"low": None, "high": None, "buy_price": None, "last": None, "prices": []},
    "CMCSA":{"low": None, "high": None, "buy_price": None, "last": None, "prices": []},
    "CMG":  {"low": None, "high": None, "buy_price": None, "last": None, "prices": []},
    "CNC":  {"low": None, "high": None, "buy_price": None, "last": None, "prices": []},
    "CSX":  {"low": None, "high": None, "buy_price": None, "last": None, "prices": []},
    "CVS":  {"low": None, "high": None, "buy_price": None, "last": None, "prices": []},
    "DOW":  {"low": None, "high": None, "buy_price": None, "last": None, "prices": []},
    "EBAY": {"low": None, "high": None, "buy_price": None, "last": None, "prices": []},
    "F":    {"low": None, "high": None, "buy_price": None, "last": None, "prices": []},
    "FCX":  {"low": None, "high": None, "buy_price": None, "last": None, "prices": []},
    "GOOG": {"low": None, "high": None, "buy_price": None, "last": None, "prices": []},
    
    "TEVA.TA": {"low": 5500, "high": 5800, "buy_price": 5600, "last": None, "prices": []},
    "BEZQ.TA": {"low": 550, "high": 631.27, "buy_price": 560, "last": None, "prices": []},
    #"POLI.TA": {"low": 6263.67, "high": 6600, "buy_price": 6400, "last": None, "prices": []},
    #"LUMI.TA": {"low": 6200, "high": 6500, "buy_price": 6300, "last": None, "prices": []},
    #"DSCT.TA": {"low": 3200, "high": 3400, "buy_price": 3300, "last": None, "prices": []},
    #"CLIS.TA": {"low": 2200, "high": 17063.33, "buy_price": 2300, "last": None, "prices": []},
    #"ICL.TA": {"low": 2200, "high": 2400, "buy_price": 2300, "last": None, "prices": []}
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
