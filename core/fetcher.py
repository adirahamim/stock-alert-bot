
import requests
import yfinance as yf
from settings import TWELVE_API

def get_price(symbol):
    try:
        return get_price_yfinance(symbol)
    except Exception as e:
        print(f"[ERROR] get_price({symbol}): {e}")
        return None

def get_price_yfinance(symbol):
    try:
        yf_symbol = symbol.replace(".TA", "") + ".TA" if symbol.endswith(".TA") else symbol
        data = yf.Ticker(yf_symbol).history(period="1d")
        if not data.empty:
            return round(data["Close"].iloc[-1], 2)
    except Exception as e:
        print(f"[ERROR] get_price_yfinance({symbol}): {e}")
    return None

def get_rating(symbol):
    if symbol.endswith(".TA"):
        return {"buy": 0, "sell": 0}
    return {"buy": 6, "sell": 0}

def get_rsi(symbol):
    try:
        response = requests.get(f"https://api.twelvedata.com/rsi?symbol={symbol}&interval=1day&apikey={TWELVE_API}")
        data = response.json()
        return float(data["value"])
    except Exception as e:
        print(f"[ERROR] get_rsi({symbol}): {e}")
        return None

def get_macd(symbol):
    try:
        response = requests.get(f"https://api.twelvedata.com/macd?symbol={symbol}&interval=1day&apikey={TWELVE_API}")
        data = response.json()
        return float(data["macd"])
    except Exception as e:
        print(f"[ERROR] get_macd({symbol}): {e}")
        return None

def get_ema(symbol, period):
    try:
        response = requests.get(f"https://api.twelvedata.com/ema?symbol={symbol}&interval=1day&time_period={period}&apikey={TWELVE_API}")
        data = response.json()
        return float(data["value"])
    except Exception as e:
        print(f"[ERROR] get_ema({symbol}, {period}): {e}")
        return None

def get_volume_spike(symbol):
    return False  # Placeholder

def get_news(symbol):
    return [{"headline": f"{symbol} sees strong movement amid market shift"}]
