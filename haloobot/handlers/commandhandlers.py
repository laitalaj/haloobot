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
            if com.group(2) != '@' + self.settings['name'] and com.group(2) != None:
                print('Skipping command to %s' % com.group(2))
                return True
            comstring = com.group(1)
            comargs = self.parser.findall(msg['text'])
            if comstring in self.commands.keys():
                response = await self.commands[comstring].run(comargs, msg)
                if response and type(response) == tuple:
                    if response[1] == 'voice': # (message, 'voice', <language>)
                        if len(response) > 2:
                            await self.send_voice(chat_id, response[0], response[2])
                        else:
                            await self.send_voice(chat_id, response[0])
                    elif response[1] == 'sticker': # (file_id, 'sticker')
                        await self.send_sticker(chat_id, response[0])
                    elif response[1] == 'audio': # (filename, 'audio')
                        await self.send_audio(chat_id, response[0])
                    elif response[1] == 'image': # (file_id, 'image', <caption>)
                        if len(response) > 2:
                            await self.send_image(chat_id, response[0], response[2])
                        else:
                            await self.send_image(chat_id, response[0])
                    elif response[1] == 'download': # (file_id, 'download', file_type, filename, success_message, fail_message) 
                        success = await self.download_file(response[0], response[2], response[3])
                        if success:
                            await self.send_message(chat_id, response[4])
                        else:
                            await self.send_message(chat_id, response[5])
                    else:
                        await self.send_message(chat_id, response[0])  
                elif response:
                    await self.send_message(chat_id, response)      
            else:
                print('Skipping unknown command %s' % comstring)
            return True
        else:
            return False