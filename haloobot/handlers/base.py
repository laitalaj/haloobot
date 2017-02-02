import os, random
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
            if len(message) > 4000:
                message = message[:4000]
            await self.bot.sendMessage(chat_id, message)
            return True
        except Exception as e:
            print('Couldn\'t send a message: %s' % e)
            return False
        
    async def send_reply(self, chat_id, reply_to, message):
        if self.settings['silence']:
            return True
        try:
            if len(message) > 4000:
                message = message[:4000]
            await self.bot.sendMessage(chat_id, message, 
                                       reply_to_message_id = reply_to)
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
    
    async def send_voice(self, chat_id, message, lang=None):
        if self.settings['silence']:
            return True
        success = True
        oggpath = None
        if lang == None:
            lang = random.choice(self.settings['tts_lang'])
        if 'message' in self.tables['speeches'].columns:
            speech = self.tables['speeches'].find_one(message=message, language=lang)
        else:
            speech = None
        if speech:
            try:
                print('Sending voice with file ID ...%s' % speech['file_id'][-8:])
                await self.bot.sendVoice(chat_id, speech['file_id'])
                return True
            except Exception as e:
                print('Couldn\'t send voice: %s' % e)
                return False
        else:
            try:
                oggpath = text_to_ogg(message, lang, self.settings['tts_id'])
                self.settings['tts_id'] += 1
                try:
                    with open(oggpath, 'rb') as oggfile:
                        print('Sending voice from file %s' % oggpath)
                        response = await self.bot.sendVoice(chat_id, oggfile)
                        self.tables['speeches'].insert({
                            'message': message,
                            'file_id': response['voice']['file_id'],
                            'language': lang
                            })
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