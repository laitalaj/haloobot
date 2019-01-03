from haloobot.commands.base import Command
from urllib import request

def add_all(commands, tables, messages, settings):
    BreakSilenceCommand(commands, tables, messages, settings)
    SilenceCommand(commands, tables, messages, settings)
    IPCommand(commands, tables, messages, settings)
    CommandListingCommand(commands, tables, messages, settings)

class BreakSilenceCommand(Command):
    
    comtext = 'breaksilence'
    minargs = 0
    helptext = 'Breaks silence'
    requires_message = True
    
    def run_command(self, args, msg):
        self.settings['silence'] = False
        self.settings['chat_id'] = msg['chat']['id'] # "Haloobot is designed to work only in one chat" -laitalaj
        print('Broke silence!')
        return 'Silence broken!'


class SilenceCommand(Command):
    
    comtext = 'silence'
    minargs = 0
    helptext = 'Silences the bot'
    
    def run_command(self, args):
        self.settings['silence'] = True
        print('Silenced the bot')
        return '~hush~'


class IPCommand(Command):
    
    comtext = 'whereareyou'
    minargs = 1
    helptext = ''
    
    def run_command(self, args):
        if args[0] == self.settings['password']:
            try:
                print('Gave IP to someone')
                return 'My ip is %s!' % request.urlopen('http://api.ipify.org').read().decode('utf-8')
            except Exception as e:
                print('Couldn\'t get IP address: %s' % e)
                return 'I don\'t know where I am >:'
        else:
            print('Someone tried to get IP with wrong password!')

class CommandListingCommand(Command):
    
    comtext = 'listcommands'
    minargs = 0
    helptext = 'Lists commands in botfather-friendly format'
    
    def __init__(self, commands, tables, messages, settings):
        super().__init__(commands, tables, messages, settings)
        self.commands = commands
        
    def run_command(self, args):
        message = []
        for command in self.commands:
            if self.commands[command].helptext:
                message.append(command + ' - ' + self.commands[command].helptext)
        message.sort()
        print('Giving commands...')
        return '\n'.join(message)