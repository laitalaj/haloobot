from inspect import iscoroutinefunction

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
    
    async def run(self, args, msg = None):
        if len(args) < self.minargs:
            return self.helptext
        methodArgs = None
        if self.requires_message:
            methodArgs = (args, msg)
        else:
            methodArgs = (args,)
        if iscoroutinefunction(self.run_command):
            return await self.run_command(*methodArgs)
        return self.run_command(*methodArgs)

    def run_command(self, args, msg = None):
        return ''