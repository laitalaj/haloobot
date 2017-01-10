from haloobot.commands.base import Command

def add_all(commands, tables, messages, settings):
    SetTriggerCommand(commands, tables, messages, settings)

class SetTriggerCommand(Command):
    
    comtext = 'settrigger'
    minargs = 1
    helptext = 'Changes trigger to given percentage. Syntax: /settrigger "[trigger percentage]"'
    
    def run_command(self, args):
        try:
            newtrigger = int(args[0])
        except:
            return 'Couldn\'t parse percentage %s' % args[0]
        self.settings['trigger'] = newtrigger/100
        settingsentry = self.tables['settings'].find_one(type = 'trigger')
        settingsentry['value'] = args[0]
        self.tables['settings'].update(settingsentry, ['type'])
        print("Trigger now at %s" % self.settings['trigger'])
        return 'Successfully changed trigger percentage to %s!' % newtrigger