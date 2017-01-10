import asyncio
from haloobot.commands.base import Command

def add_all(commands, tables, messages, settings):
    PartyModeCommand(commands, tables, messages, settings)
    SleepCommand(commands, tables, messages, settings)

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