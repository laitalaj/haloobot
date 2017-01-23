import asyncio
from haloobot.commands.base import Command
from haloobot.utils.time import temporary_setting_change

def add_all(commands, tables, messages, settings):
    PartyModeCommand(commands, tables, messages, settings)
    SleepCommand(commands, tables, messages, settings)

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