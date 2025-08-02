import yfinance as yf
import re

SETTINGS_FILE = "settings.py"

def fetch_new_prices(symbol):
    try:
        t = yf.Ticker(symbol)
        hist = t.history(period="1mo")
        low = round(hist["Low"].min(), 2)
        high = round(hist["High"].max(), 2)
        buy = round((low + high) / 2, 2)
        return low, high, buy
    except:
        return None, None, None

def update_settings_file():
    with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
        content = f.read()

    def replace_line(match):
        symbol = match.group(1)
        if ".TA" in symbol:
            return match.group(0)  # Skip Israeli stocks
        low, high, buy = fetch_new_prices(symbol)
        if low is None:
            print(f"⚠️ Skipping {symbol} – failed to fetch")
            return match.group(0)
        print(f"✅ {symbol}: low={low}, high={high}, buy_price={buy}")
        return f'"{symbol}": {{"low": {low}, "high": {high}, "buy_price": {buy}, "last": None, "prices": []}},'

    pattern = r'"([A-Z\.]+)": \{[^}]+?\},'
    updated = re.sub(pattern, replace_line, content)

    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        f.write(updated)

    print("\n✅ settings.py updated successfully.")

if __name__ == "__main__":
    update_settings_file()
