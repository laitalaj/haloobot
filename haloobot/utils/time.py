import time, asyncio

def get_day_number():
    t = time.localtime()
    return t.tm_year * 365 + t.tm_yday

async def temporary_setting_change(settings, setting, to, time):
    oldval = settings[setting]
    print('Setting %s changed to %s temporarily' % (setting, to))
    settings[setting] = to
    await asyncio.sleep(time)
    if settings[setting] == to:
        settings[setting] = oldval
        print('Setting %s changed back to %s' % (setting, oldval))
    else:
        print('Won\'t change setting %s back to %s because it has already been changed...' % (setting, oldval))