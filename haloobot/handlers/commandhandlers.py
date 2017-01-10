import re
import haloobot.commands
from haloobot.handlers.base import Handler

class CommandHandler(Handler):
    
    handle_keys = ['text']
    ignore_keys = []
    
    def __init__(self, handlers, bot, tables, messages, settings):
        super().__init__(handlers, bot, tables, messages, settings)
        self.commands = {}
        haloobot.commands.add_all(self.commands, tables, messages, settings)
        self.commandre = re.compile('/(\w+)(@\w+)?')
        self.parser = re.compile('"([^"]*)"')
    
    async def do_handle(self, msg):
        chat_id = msg['chat']['id']
        com = self.commandre.match(msg['text'])
        if com != None:
            if com.group(2) != '@ha_loo_bot' and com.group(2) != None:
                print('Skipping command to %s' % com.group(2))
                return True
            comstring = com.group(1)
            comargs = self.parser.findall(msg['text'])
            if comstring in self.commands.keys():
                response = self.commands[comstring].run(comargs)
                if response:
                    await self.send_message(chat_id, response)         
            else:
                print('Skipping unknown command %s' % comstring)
            return True
        else:
            return False