
import requests
import os
from settings import TWELVE_API, FINNHUB_API, NEWS_API

try:
    import yfinance as yf
except ImportError:
    yf = None

def get_price(symbol):
    try:
        if symbol.endswith(".TA"):
            price = get_price_yahoo(symbol)
            if price is None and yf:
                price = get_price_yfinance(symbol)
        else:
            price = get_price_yfinance(symbol, prepost=True) if yf else None
            if price is None:
                price = get_price_twelvedata(symbol)
        return round(price, 2) if price else None
    except Exception as e:
        print(f"[ERROR] get_price({symbol}): {e}")
        return None

def get_price_twelvedata(symbol):
    try:
        url = f"https://api.twelvedata.com/price?symbol={symbol}&apikey={TWELVE_API}"
        res = requests.get(url).json()
        return float(res.get("price")) if "price" in res else None
    except Exception as e:
        print(f"[ERROR] get_price_twelvedata({symbol}): {e}")
        return None

def get_price_yahoo(symbol):
    try:
        url = f"https://query1.finance.yahoo.com/v7/finance/quote?symbols={symbol}"
        headers = {"User-Agent": "Mozilla/5.0"}
        res = requests.get(url, headers=headers).json()
        return res['quoteResponse']['result'][0].get('regularMarketPrice')
    except Exception as e:
        print(f"[ERROR] get_price_yahoo({symbol}): {e}")
        return None

def get_price_yfinance(symbol, prepost=False):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.history(period="1d", interval="1m", prepost=prepost)
        if not data.empty and "Close" in data.columns:
            return data["Close"].iloc[-1]
    except Exception as e:
        print(f"[ERROR] get_price_yfinance({symbol}): {e}")
    return None

def get_rating(symbol):
    if symbol.endswith(".TA"):
        return {"buy": 0, "hold": 0, "sell": 0}
    try:
        url = f"https://finnhub.io/api/v1/stock/recommendation?symbol={symbol}&token={FINNHUB_API}"
        res = requests.get(url).json()
        return res[0] if res else {"buy": 0, "hold": 0, "sell": 0}
    except Exception as e:
        print(f"[WARN] No rating found for {symbol}: {e}")
        return {"buy": 0, "hold": 0, "sell": 0}

def get_rsi(symbol):
    if symbol.endswith(".TA"):
        return None
    try:
        url = f"https://taapi.p.sulu.sh/rsi?exchange=NASDAQ&symbol={symbol}&interval=1d"
        res = requests.get(url).json()
        return float(res.get("value", 50))
    except Exception as e:
        print(f"[ERROR] get_rsi({symbol}): {e}")
        return None

def get_macd(symbol):
    try:
        url = f"https://finnhub.io/api/v1/indicator?symbol={symbol}&resolution=1&indicator=macd&token={FINNHUB_API}"
        r = requests.get(url).json()
        if "macd" in r:
            return r["macd"]["macd"][-1] - r["macd"]["signal"][-1]
        else:
            print(f"[ERROR] get_macd({symbol}): {r}")
    except Exception as e:
        print(f"[ERROR] get_macd({symbol}): {e}")
    return None

def get_ema(symbol, period):
    try:
        url = f"https://finnhub.io/api/v1/indicator?symbol={symbol}&resolution=1&indicator=ema&timeperiod={period}&token={FINNHUB_API}"
        r = requests.get(url).json()
        if "ema" in r:
            return r["ema"]["values"][-1]
        else:
            print(f"[ERROR] get_ema({symbol}, {period}): {r}")
    except Exception as e:
        print(f"[ERROR] get_ema({symbol}, {period}): {e}")
    return None

def get_volume_spike(symbol):
    try:
        url = f"https://finnhub.io/api/v1/stock/candle?symbol={symbol}&resolution=1&count=30&token={FINNHUB_API}"
        r = requests.get(url).json()
        volumes = r.get("v", [])
        if len(volumes) >= 10:
            return volumes[-1] > sum(volumes[-10:-1]) / 9 * 1.5
    except Exception as e:
        print(f"[ERROR] get_volume_spike({symbol}): {e}")
    return False

def get_news(symbol):
    try:
        url = f"https://newsapi.org/v2/everything?q={symbol}&apiKey={NEWS_API}&language=en&pageSize=1"
        r = requests.get(url).json()
        if "articles" in r and r["articles"]:
            return r["articles"][0].get("title")
        else:
            print(f"[ERROR] get_news({symbol}): {r}")
    except Exception as e:
        print(f"[ERROR] get_news({symbol}): {e}")
    return None
