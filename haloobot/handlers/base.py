import os, random, re
from haloobot.utils.dicts import dict_contains_key
from haloobot.utils.audio import text_to_ogg
from haloobot.utils.blame import blame_message

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
            try:
                if k == '*':
                    return await self.do_handle(msg)
                if dict_contains_key(msg, k):
                    return await self.do_handle(msg)
            except Exception as e:
                await self.send_message(msg['chat']['id'], blame_message(e), 'Markdown')
    
    async def send_message(self, chat_id, message, parse_mode = None):
        if self.settings['silence']:
            return True
        try:
            if len(message) > 4000:
                message = message[:4000]
            await self.bot.sendMessage(chat_id, message, parse_mode=parse_mode)
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
        
    async def send_sticker(self, chat_id, file_id, reply_to = None): #TODO: Get rid of that send_reply and use instead something like this in send_message
        if self.settings['silence']:
            return True
        try:
            await self.bot.sendSticker(chat_id, file_id,
                                       reply_to_message_id = reply_to)
            return True
        except Exception as e:
            print('Couldn\'t send a sticker: %s' % e)
            return False
    
    async def send_image(self, chat_id, file_id, caption = None):
        if self.settings['silence']:
            return True
        try:
            await self.bot.sendPhoto(chat_id, file_id, caption)
            return True
        except Exception as e:
            print('Couldn\'t send a image: %s' % e)
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
    
    async def send_audio(self, chat_id, filename):
        if self.settings['silence']:
            return True
        trimmer = re.compile('[^\w]+') #Make sure that no-one accesses something they shouldn't
        filename = trimmer.sub('', filename)
        if 'name' in self.tables['songs'].columns:
            song = self.tables['songs'].find_one(name = filename)
        else:
            song = None
        if song:
            try:
                print('Sending audio clip %s with file id' % filename)
                file_format = song['format'] # Very quick and dirty hack, hopefully it doesn't come back to haunt me
                method = self.bot.sendVoice if file_format == 'ogg' else self.bot.sendAudio
                await method(chat_id, song['file_id'])
                return True
            except Exception as e:
                print('Couldn\'t send audio: %s' % e)
                return False
        else:
            audiopath = os.path.join('audio', filename + '.mp3')
            if not os.path.isfile(audiopath):
                print('Tried to send a non-existing clip %s' % filename)
                self.send_message(chat_id, "I don\'t have a clip called %s!" % filename)
                return False
            try:
                with open(audiopath, 'rb') as audio:
                    print('Sending audio file %s' % filename)
                    response = await self.bot.sendAudio(chat_id, audio, title = filename)
                    self.tables['songs'].insert({'name': filename,
                                                 'file_id': response['audio']['file_id']})
                return True
            except Exception as e:
                print('Couldnt send audio: %s' % e)
                return False
    
    async def download_file(self, file_id, file_type, filename):
        if file_type.startswith('audio'):
            file_format = file_type.split('/')[1]
            if not os.path.exists(os.path.join('audio')):
                os.makedirs('audio')
            dest = os.path.join('audio', "{}.{}".format(filename, file_format))
            if os.path.exists(dest): #TODO: Refactor
                print('Tried to overwrite a file!')
                return False
            self.tables['songs'].insert({'name': filename,
                                         'file_id': file_id,
                                         'format': file_format})
        else:
            if not os.path.exists(os.path.join('etc')):
                os.makedirs('etc')
            dest = os.path.join('etc', filename)
            if os.path.exists(dest):
                print('Tried to overwrite a file!')
                return False
        try:
            await self.bot.download_file(file_id, dest)
            print('Downloaded ...%s to %s!' % (file_id[-8:], dest))
        except Exception as e:
            print('Couldn\'t download file ...%s to %s - %s' % (file_id[-8:], dest, e))
            return False
        return True
    
    async def do_handle(self, msg):
        return False
