class Command:
    
    comtext = ''
    minargs = 0
    helptext = ''
    
    def __init__(self, commands, tables, messages, settings):
        if self.comtext in commands.keys():
            print('WARNING: There\'s already a command for %s, overwriting!' % self.comtext)
        if self.comtext:
            commands[self.comtext] = self
        self.tables = tables
        self.messages = messages
        self.settings = settings
    
    def run(self, args):
        if len(args) < self.minargs:
            return self.helptext
        return self.run_command(args)
    
    def run_command(self, args):
        return ''