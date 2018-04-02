import asyncio
from dateutil import parser as dateparser
from haloobot.commands.base import Command
from haloobot.utils.time import temporary_setting_change, get_upcoming_events_string

def add_all(commands, tables, messages, settings):
    PartyModeCommand(commands, tables, messages, settings)
    SleepCommand(commands, tables, messages, settings)
    AddEventCommand(commands, tables, messages, settings)
    AddOneOffEventCommand(commands, tables, messages, settings)
    ListEventsCommand(commands, tables, messages, settings)
    RemoveEventCommand(commands, tables, messages, settings)
    GetUpcomingCommand(commands, tables, messages, settings)

class PartyModeCommand(Command):
    
    comtext = 'partymode'
    minargs = 0
    helptext = 'Party mode - 100% triggers for one hour! Syntax: /partymode "[optional: minutes to party]"'
    
    def run_command(self, args):
        time = 60
        if len(args) > 0:
            try:
                time = int(args[0])
            except:
                return '%s is not a valid amount of minutes' % args[0]
        loop = asyncio.get_event_loop()
        loop.create_task(
            temporary_setting_change(self.settings, 'trigger', 1.0, time * 60)
            )
        print('Party mode activated!')
        return 'Party mode activated for %s minutes!' % time


class SleepCommand(Command):
    
    comtext = 'sleepmode'
    minargs = 0
    helptext = 'Sleep mode - 0% triggers for one hour. Syntax: /sleepmode "[optional: minutes to sleep]"'
    
    def run_command(self, args):
        time = 60
        if len(args) > 0:
            try:
                time = int(args[0])
            except:
                return '%s is not a valid amount of minutes' % args[0]
        loop = asyncio.get_event_loop()
        loop.create_task(
            temporary_setting_change(self.settings, 'trigger', 1.0, time * 60)
            )
        print('Sleep mode activated!')
        return 'Sleep mode activated for %s minutes.' % time

class AddEventCommand(Command):

    comtext = 'addevent'
    minargs = 2
    helptext = 'Add an event. Syntax: /addevent "[event name]" "[next event date]" "[optional: event countdown in days]"'
    requires_message = True
    is_oneoff = False

    def run_command(self, args, msg):
        name = args[0]
        nextdate = args[1]
        countdown = args[2] if len(args) > 2 else 0
        try:
            nextdate = dateparser.parse(nextdate, dayfirst=True, yearfirst=False)
        except ValueError:
            print('Failed to parse {} when trying to add schedule'.format(nextdate))
            return 'Parser couldn\'t recognize the date format given >:'
        try:
            countdown = int(countdown)
        except ValueError:
            print('Failed to parse countdown {}'.format(countdown))
            return 'Invalid countdown!'
        nextdate = nextdate.date()
        try:
            self.tables['schedules'].insert({
                'chat_id': msg['chat']['id'],
                'name': name,
                'nextdate': nextdate,
                'countdown': countdown,
                'oneoff': self.is_oneoff
            })
        except Exception as e:
            print(e)
            return 'Something went wrong when trying to add the schedule >:'
        return 'Added event {}!'.format(name)

class AddOneOffEventCommand(AddEventCommand):

    comtext = 'addoneoff'
    minargs = 2
    helptext = 'Adds an one-off event. Syntax: /addevent "[event name]" "[event date]" "[optional: event countdown in days]"'
    requires_message = True
    is_oneoff = True

class RemoveEventCommand(Command):

    comtext = 'removeevent'
    minargs = 1
    helptext = 'Remove an event. Syntax: /removeevent "[event name]"'
    requires_message = True

    def run_command(self, args, msg):
        name = args[0]
        chatid = msg['chat']['id']
        try:
            self.tables['schedules'].delete(name=name, chat_id=chatid)
        except Exception as e:
            print('{} when trying to delete {}/{}'.format(e, name, chatid))
            return 'Couldn\'t delete {} >:'.format(name)
        return '{} deleted!'.format(name)

class ListEventsCommand(Command):

    comtext = 'listevents'
    minargs = 0
    helptext = 'List all events for this chat'
    requires_message = True

    def run_command(self, args, msg):
        res = []
        for event in self.tables['schedules'].find(chat_id=msg['chat']['id']):
            countdown_str = ', countdown {} days'.format(event['countdown']) if event['countdown'] else ''
            oneoff_str = ' (one-off)' if event['oneoff'] else ''
            res.append('{}: {}{}{}'.format(event['nextdate'], event['name'], countdown_str, oneoff_str))
        return '\n'.join(res) if res else 'No events scheduled!'

class GetUpcomingCommand(Command):

    comtext = 'getupcoming'
    minargs = 0
    helptext = 'Get upcoming events.'
    requires_message = True

    def run_command(self, args, msg):
        ret = get_upcoming_events_string(self.tables['schedules'], msg['chat']['id'])
        print('Gave upcoming events!')
        return ret if ret else 'No upcoming events today.'