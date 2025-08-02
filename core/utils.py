
import datetime
import pytz

def is_us_market_open():
    now = datetime.datetime.now(pytz.timezone('America/New_York'))
    return now.weekday() < 5 and datetime.time(9, 30) <= now.time() <= datetime.time(16, 0)

def is_il_market_open():
    now = datetime.datetime.now(pytz.timezone('Asia/Jerusalem'))
    # ת״א פתוחה ראשון עד חמישי 9:00-17:25
    return now.weekday() in [0,1,2,3,6] and datetime.time(9, 0) <= now.time() <= datetime.time(17, 25)

def get_active_market():
    if is_il_market_open():
        return "IL"
    elif is_us_market_open():
        return "US"
    else:
        return "CLOSED"
# def get_active_market():
#     return "US"  # או "IL" או "CLOSED" בהתאם למצב השוק
#     


# Added by upgrade for buy recommendation
from settings import TOTAL_BUDGET
def calculate_buy_amount(price):
    allocation = 0.05  # 5% allocation per signal
    amount = TOTAL_BUDGET * allocation
    return round(amount, 2)
