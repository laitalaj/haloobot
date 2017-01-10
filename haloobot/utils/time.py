import time

def get_day_number():
    t = time.localtime()
    return t.tm_year * 365 + t.tm_yday