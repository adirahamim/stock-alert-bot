
import yfinance as yf
import re

SETTINGS_FILE = "settings.py"

def fetch_price_range(symbol):
    try:
        t = yf.Ticker(symbol)
        hist = t.history(period="1mo")
        if hist.empty:
            return None, None, None
        low = round(hist["Low"].min(), 2)
        high = round(hist["High"].max(), 2)
        buy = round((low + high) / 2, 2)
        return low, high, buy
    except:
        return None, None, None

def add_stock_to_settings(symbol):
    try:
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        # Check if symbol already exists
        if f'"{symbol}":' in content:
            return False, "Already exists"

        low, high, buy = fetch_price_range(symbol)
        if not all([low, high, buy]):
            low, high, buy = 10.0, 20.0, 15.0  # Fallback default

        new_entry = f'"{symbol}": {{"low": {low}, "high": {high}, "buy_price": {buy}, "last": None, "prices": []}},\n'

        # Insert before the closing bracket of stocks dict
        pattern = r"(stocks\s*=\s*\{)(.*?)(\})"
        match = re.search(pattern, content, flags=re.DOTALL)
        if not match:
            return False, "Could not find stocks structure in settings.py"

        before = match.group(1)
        body = match.group(2)
        after = match.group(3)

        updated = before + body + "    " + new_entry + after

        with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
            f.write(updated)

        return True, f"{symbol} added successfully"
    except Exception as e:
        return False, str(e)
