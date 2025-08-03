
import json
import os

RUNTIME_FILE = "stocks_runtime.json"

def save_runtime_data(stocks):
    try:
        data_to_save = {s: {"last": stocks[s]["last"], "prices": stocks[s]["prices"]} for s in stocks}
        with open(RUNTIME_FILE, "w", encoding="utf-8") as f:
            json.dump(data_to_save, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Failed to save runtime data: {e}")

def load_runtime_data(stocks):
    if not os.path.exists(RUNTIME_FILE):
        print("[INFO] No previous runtime file found – starting fresh.")
        return
    try:
        with open(RUNTIME_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for symbol in stocks:
            if symbol in data:
                stocks[symbol]["last"] = data[symbol].get("last")
                stocks[symbol]["prices"] = data[symbol].get("prices", [])
    except Exception as e:
        print(f"[ERROR] Failed to load runtime data: {e}")
