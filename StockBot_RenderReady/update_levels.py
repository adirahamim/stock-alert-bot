
import os
import json
import time
from datetime import datetime
from settings import stocks
from core.fetcher import get_price, get_ema
import yfinance as yf

def calculate_atr(symbol, period=14):
    try:
        data = yf.download(symbol, period=f"{period+1}d", interval="1d")
        if data.empty:
            return None
        data["H-L"] = data["High"] - data["Low"]
        data["H-PC"] = abs(data["High"] - data["Close"].shift(1))
        data["L-PC"] = abs(data["Low"] - data["Close"].shift(1))
        tr = data[["H-L", "H-PC", "L-PC"]].max(axis=1)
        atr = tr.rolling(window=period).mean()
        return round(atr.iloc[-1], 3)
    except Exception as e:
        print(f"[ERROR] ATR calculation failed for {symbol}: {e}")
        return None

def update_levels():
    updated = {}
    for symbol in stocks:
        price = get_price(symbol)
        atr = calculate_atr(symbol)
        ema50 = get_ema(symbol, 50)

        if price is None or atr is None or ema50 is None:
            print(f"[SKIP] {symbol} – missing data")
            continue

        low = round(price - atr, 2)
        high = round(ema50 * 1.015, 2)
        if high < low:
            high = round(price + (atr * 0.5), 2)
        buy_price = round(price - (atr / 2), 2)

        updated[symbol] = {
            "low": low,
            "high": high,
            "buy_price": buy_price,
            "last": None,
            "prices": [],
            "updated_at": datetime.utcnow().isoformat()
        }
        print(f"[OK] {symbol}: low={low}, high={high}, buy={buy_price}")

    with open("stocks_runtime.json", "w", encoding="utf-8") as f:
        json.dump(updated, f, indent=2)

if __name__ == "__main__":
    update_levels()
