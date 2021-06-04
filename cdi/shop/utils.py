import datetime


def store_open():
    date = datetime.datetime.now()
    is_open = False
    if date.isoweekday() in [x for x in range(1, 7) if x != 5] and date.hour in range(8, 16):
        is_open = not is_open
    return is_open
