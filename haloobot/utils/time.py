import time, asyncio
from datetime import date
from random import choice
from emoji import emojize
from dateutil.relativedelta import *

EVENT_EMOJIS = (':tada:', ':confetti_ball:', ':beers:', ':bottle_with_popping_cork:', ':clinking_glasses:')

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

def get_upcoming_events(schedules_table, chat_id):
    today = date.today()
    events_today = []
    events_upcoming = []
    for event in schedules_table.find(chat_id=chat_id):
        # Doing this with a for-loop because dates in sqlite are a bit of a pain
        eventdate = event['nextdate']
        if eventdate < today:
            event['nextdate'] += relativedelta(years=+1)
            schedules_table.update(event, ['id'])
        elif eventdate == today:
            events_today.append(event['name'])
        elif eventdate - relativedelta(days=-event['countdown']) < today:
            events_upcoming.append(event['countdown'], event['name'])
    return (events_today, sorted(events_upcoming))

def get_upcoming_events_string(schedules_table, chat_id):
    today, upcoming = get_upcoming_events(schedules_table, chat_id)
    ret = []
    for event in today:
        ret.append('Today is {}! {}'.format(event, emojize(choice(EVENT_EMOJIS), use_aliases=True)))
    if ret:
        ret.append('')
    if upcoming:
        ret.append('Upcoming events:')
        for event in upcoming:
            ret.append(' -{} is in {} days'.format(event[1], event[0]))
    return '\n'.join(ret)