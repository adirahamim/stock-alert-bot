import json
import os

RUNTIME_PATH = "stocks_runtime.json"

def save_runtime_data(stocks):
    to_save = {k: {"last": v["last"], "prices": v["prices"]} for k, v in stocks.items()}
    with open(RUNTIME_PATH, "w") as f:
        json.dump(to_save, f)

def load_runtime_data(stocks):
    if not os.path.exists(RUNTIME_PATH):
        return
    with open(RUNTIME_PATH, "r") as f:
        saved = json.load(f)
    for k, v in saved.items():
        if k in stocks:
            stocks[k]["last"] = v.get("last")
            stocks[k]["prices"] = v.get("prices", [])
