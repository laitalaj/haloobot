import os
from haloobot.utils.dicts import dict_contains_key
from haloobot.utils.audio import text_to_ogg

class Handler:
    
    handle_keys = []
    ignore_keys = []
    
    def __init__(self, handlers, bot, tables, messages, settings):
        handlers.append(self)
        self.bot = bot
        self.tables = tables
        self.messages = messages
        self.settings = settings
    
    async def handle(self, msg):
        for k in self.ignore_keys:
            if dict_contains_key(msg, k):
                return False
        for k in self.handle_keys:
            if k == '*':
                return await self.do_handle(msg)
            if dict_contains_key(msg, k):
                return await self.do_handle(msg)
    
    async def send_message(self, chat_id, message):
        if self.settings['silence']:
            return True
        try:
            await self.bot.sendMessage(chat_id, message)
            return True
        except Exception as e:
            print('Couldn\'t send a message: %s' % e)
            return False
        
    async def send_sticker(self, chat_id, file_id):
        if self.settings['silence']:
            return True
        try:
            await self.bot.sendSticker(chat_id, file_id)
            return True
        except Exception as e:
            print('Couldn\'t send a sticker: %s' % e)
            return False
    
    async def send_voice(self, chat_id, message):
        if self.settings['silence']:
            return True
        success = True
        oggpath = None
        try:
            oggpath = text_to_ogg(message, self.settings['tts_id'])
            self.settings['tts_id'] += 1
            try:
                with open(oggpath) as oggfile:
                    await self.bot.sendVoice(chat_id, oggfile)
            except Exception as e:
                print('Couldn\'t send voice: %s' % e)
                success = False
        except Exception as e:
            print('Text to speech failed: %s' % e)
            success = False
        finally:
            if oggpath != None:
                os.remove(oggpath)
        return success
        
    async def do_handle(self, msg):
        return False