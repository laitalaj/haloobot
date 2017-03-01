class Command:
    
    comtext = ''
    minargs = 0
    helptext = ''
    
    requires_message = False
    
    def __init__(self, commands, tables, messages, settings):
        if self.comtext in commands.keys():
            print('WARNING: There\'s already a command for %s, overwriting!' % self.comtext)
        if self.comtext:
            commands[self.comtext] = self
        self.tables = tables
        self.messages = messages
        self.settings = settings
    
    def run(self, args, msg = None):
        if len(args) < self.minargs:
            return self.helptext
        if self.requires_message:
            return self.run_command(args, msg)
        else:
            return self.run_command(args)
    
    def run_command(self, args, msg = None):
        return ''