import datetime
from datetime import timedelta

# def store_open():
#     date = datetime.datetime.now()
#     is_open = False
#     if date.isoweekday() in range(0, 6) and date.hour in range(8, 16):
#         is_open = not is_open
#     return is_open

def store_open():
    date = datetime.datetime.now()
    is_open = False
    start = (date - timedelta(days=(date.weekday() + 2) % 7)) - timedelta(days=7)
    end = (start + timedelta(days=7)) # 6
    if start <= date <= end and date.hour in range(8, 16): # <
        is_open = not is_open
    return is_open

dt = datetime.datetime.now()
start = (dt - timedelta(days=(dt.weekday() + 2) % 7)) - timedelta(days=7)
end = (start + timedelta(days=6))
print(start.strftime("%Y-%m-%d"))
print(end.strftime("%Y-%m-%d"))
