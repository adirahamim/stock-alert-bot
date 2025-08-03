
import streamlit as st
import pandas as pd
import os
import json
from settings import stocks

st.set_page_config(layout="wide")
st.title("📈 לוח בקרה בוט השקעות חכם")

# פרופיל סוחר
st.sidebar.header("🎛️ הגדרות משתמש")
profile = st.sidebar.radio("בחר פרופיל משקיע:", ["aggressive", "conservative", "neutral"])
st.sidebar.success(f"הפרופיל הנבחר: {profile}")

# טופס לעדכון ערכי מניה
st.sidebar.header("✏️ עדכון פרמטרי מניה")
symbol_to_update = st.sidebar.selectbox("בחר מניה לעדכון", list(stocks.keys()))
if symbol_to_update:
    low = st.sidebar.number_input("אזור קנייה (low)", value=float(stocks[symbol_to_update]["low"]))
    high = st.sidebar.number_input("התנגדות (high)", value=float(stocks[symbol_to_update]["high"]))
    buy_price = st.sidebar.number_input("שער קנייה", value=float(stocks[symbol_to_update]["buy_price"]))

    if st.sidebar.button("עדכן ערכים ושמור לקובץ"):
        stocks[symbol_to_update]["low"] = low
        stocks[symbol_to_update]["high"] = high
        stocks[symbol_to_update]["buy_price"] = buy_price
        st.sidebar.success(f"המניה {symbol_to_update} עודכנה בהצלחה ✅")

        # כתיבה לקובץ settings.py
        with open("settings.py", "r") as f:
            lines = f.readlines()

        with open("settings.py", "w") as f:
            inside_dict = False
            for line in lines:
                if line.strip().startswith("stocks = {"):
                    f.write("stocks = {\n")
                    for key, val in stocks.items():
                        f.write(f'    "{key}": {val},')
                    f.write("}")
                    inside_dict = True
                elif inside_dict and line.strip() == "}":
                    inside_dict = False
                    continue
                elif not inside_dict:
                    f.write(line)

# טבלת איתותים מהCSV
st.subheader("📬 איתותים חיים מהבוט")
if os.path.exists("signals_log.csv"):
    df = pd.read_csv("signals_log.csv", header=None, names=["זמן", "מניה", "מחיר", "איתות"])
    df["זמן"] = pd.to_datetime(df["זמן"], errors="coerce")
    df = df.dropna(subset=["זמן"])

    df = df.sort_values(by="זמן", ascending=False)
    st.dataframe(df, use_container_width=True)
else:
    st.warning("עדיין אין איתותים מתועדים")

# טבלת מצב נוכחי
st.subheader("📊 מצב המניות הנוכחי")
stock_data = []
for symbol, data in stocks.items():
    stock_data.append({
        "סימול": symbol,
        "אזור קנייה (low)": data["low"],
        "התנגדות (high)": data["high"],
        "שער קנייה": data["buy_price"],
        "מחיר אחרון": data.get("last", "N/A")
    })
st.dataframe(pd.DataFrame(stock_data), use_container_width=True)
