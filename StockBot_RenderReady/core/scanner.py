
import pandas as pd
import requests
from bs4 import BeautifulSoup

# ✅ Option 1 – Recommended: Load from public S&P 500 list (stable CSV)
def get_stock_candidates():
    try:
        url = "https://datahub.io/core/s-and-p-500-companies/r/constituents.csv"
        df = pd.read_csv(url)
        symbols = df["Symbol"].tolist()
        print(f"[INFO] Loaded {len(symbols)} tickers from S&P 500 list")
        return symbols[:50]  # Limit to 50 for performance
    except Exception as e:
        print(f"[ERROR] Failed to load S&P500 list: {e}")
        return []

# --------------------------------------
# 🔒 Option 2 – Yahoo Finance: Most Active (commented for future)

# def get_stock_candidates():
#     try:
#         url = "https://query1.finance.yahoo.com/v1/finance/screener/predefined/saved?scrIds=most_actives"
#         headers = {"User-Agent": "Mozilla/5.0"}
#         response = requests.get(url, headers=headers)
#         data = response.json()
#         quotes = data.get("finance", {}).get("result", [])[0].get("quotes", [])
#         symbols = [q["symbol"] for q in quotes]
#         print(f"[INFO] Loaded {len(symbols)} most active stocks from Yahoo Finance")
#         return symbols
#     except Exception as e:
#         print(f"[ERROR] Yahoo API failed: {e}")
#         return []

# --------------------------------------
# 🔒 Option 3 – Finviz Top Gainers (HTML scraping, may be blocked)
# def get_stock_candidates():
#     url = "https://finviz.com/screener.ashx?v=111&s=ta_topgainers"
#     headers = {'User-Agent': 'Mozilla/5.0'}
#     try:
#         res = requests.get(url, headers=headers, timeout=10)
#         soup = BeautifulSoup(res.text, "html.parser")
#         links = soup.select("a.screener-link-primary")
#         symbols = [link.text.strip() for link in links if link.text.isupper()]
#         print(f"[INFO] Loaded top movers from Finviz: {symbols[:20]}")
#         return symbols[:20]
#     except Exception as e:
#         print(f"[ERROR] Finviz scrape failed: {e}")
#         return []

# --------------------------------------
# 🔒 Option 4 – TwelveData gainers (for Pro accounts)
# def get_stock_candidates():
#     try:
#         url = f"https://api.twelvedata.com/stocks?source=gainers&apikey=YOUR_API_KEY"
#         response = requests.get(url)
#         data = response.json()
#         symbols = [item["symbol"] for item in data.get("data", [])]
#         print(f"[INFO] Loaded top gainers from TwelveData")
#         return symbols
#     except Exception as e:
#         print(f"[ERROR] TwelveData gainers failed: {e}")
#         return []
