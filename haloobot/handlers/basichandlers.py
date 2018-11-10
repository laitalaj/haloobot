import random, telepot, time, asyncio
from haloobot.utils.messages import do_replaces
from haloobot.utils.time import get_day_number, temporary_setting_change
from haloobot.handlers.base import Handler
from haloobot.handlers.counters import speakercounters, statcounters
from haloobot.utils.dicts import dict_contains_key

def add_all(handlers, bot, tables, messages, settings):
    SpeakerUpdateHandler(handlers, bot, tables, messages, settings)
    TextHandler(handlers, bot, tables, messages, settings)
    StickerHandler(handlers, bot, tables, messages, settings)
    ReplyHandler(handlers, bot, tables, messages, settings)
    HuomautusHandler(handlers, bot, tables, messages, settings)

class SpeakerUpdateHandler(Handler):
    
    handle_keys = ['*']
    ignore_keys = []
    
    async def do_handle(self, msg):
        speakercounters.update_speaker(msg, self.tables)
    

class TextHandler(Handler):
    
    handle_keys = ['text', 'caption']
    ignore_keys = []
    
    def process_msg(self, msg, update_stats = True):
        text = msg['text'] if 'text' in msg.keys() else ''
        text += msg['caption'] if 'caption' in msg.keys() else ''
        if update_stats:
            speakercounters.update_speaker_text(msg, self.tables)
        if len(text) > 4000:
                print('Skipping too long message...')
                return False
        message = []
        for t in self.messages.keys():
            match = self.messages[t][0].search(text)
            if match != None:
                if random.random() > self.settings['trigger']:
                    if update_stats:
                        statcounters.update_skipped(t, self.tables)
                else:
                    message.append(do_replaces(msg, self.messages[t][1], match))
                    if update_stats:
                        statcounters.update_count(t, self.tables)
                        speakercounters.update_speaker_triggers(msg, self.tables)
        return message

    async def do_handle(self, msg):
        chat_id = msg['chat']['id']
        reply_to_me = dict_contains_key(msg, 'reply_to_message.from.username') and msg['reply_to_message']['from']['username'] == self.settings['name']
        message = self.process_msg(msg)
        if message and not reply_to_me:
            random.shuffle(message)
            messagestr = ' '.join(message)
            voice_possible = len(messagestr) < self.settings['tts_max_length'] and not self.settings['tts_cooldown']
            if voice_possible and random.random() < max(self.settings['trigger'], 0.5):
                loop = asyncio.get_event_loop()
                loop.create_task(
                    temporary_setting_change(self.settings, 'tts_cooldown', True, self.settings['tts_cooldown_time'])
                    )
                await self.send_voice(chat_id, messagestr)
            else:
                await self.send_message(chat_id, messagestr)
        return True


class StickerHandler(Handler):
    
    handle_keys = ['sticker']
    ignore_keys = []
    
    def process_sticker(self, msg, update_stats = True):
        if update_stats:
            speakercounters.update_speaker_stickers(msg, self.tables)
        sticker = msg['sticker']
        if self.tables['stickers'].insert_ignore({'file_id': sticker['file_id']}, ['file_id']):
            print('Added new sticker ...%s!' % sticker['file_id'][-8:])
        if 'emoji' in sticker: # Keep that old db working and the emoji up to date
            self.tables['stickers'].update({'file_id': sticker['file_id'], 'emoji': sticker['emoji']}, ['file_id'])
        if random.random() < self.settings['trigger']:
            if update_stats:
                speakercounters.update_speaker_triggers(msg, self.tables)
            to_send = None
            for emoji in sticker['emoji']:
                if emoji in '();/*-': # Should hinder any SQL injetions in case someone manages to feed non-emojis through the api
                    continue
                try:
                    results = self.tables['db'].query('SELECT * FROM stickers WHERE emoji LIKE \'%{}%\' ORDER BY RANDOM()'.format(emoji))
                    to_send = results.next()
                    while to_send['file_id'] == sticker['file_id']:
                        to_send = results.next()
                except StopIteration:
                    to_send = None
            if to_send == None:
                to_send = self.tables['db'].query('SELECT * FROM stickers ORDER BY RANDOM() LIMIT 1').next()
                print('Didn\'t find any differing stickers with matching emoji >:')
            return to_send
        else:
            return None
    
    async def do_handle(self, msg):
        chat_id = msg['chat']['id']
        reply_to_me = dict_contains_key(msg, 'reply_to_message.from.username') and msg['reply_to_message']['from']['username'] == self.settings['name']
        reply = self.process_sticker(msg)
        if reply != None and not reply_to_me:
            await self.send_sticker(chat_id, reply['file_id'])
            print('Sent sticker ...%s as a reply to ...%s' % (reply['file_id'][-8:], msg['sticker']['file_id'][-8:]))
        else:
            print('Didn\'t reply to sticker ...%s' % msg['sticker']['file_id'][-8:])
        return True


class HuomautusHandler(Handler):
    
    handle_keys = ['*']
    ignore_keys = []
    
    def __init__(self, handlers, bot, tables, messages, settings):
        super().__init__(handlers, bot, tables, messages, settings)
        self.settings['time_sent'] = get_day_number() - 1
        self.settings['food_time_sent'] = get_day_number() - 1
    
    async def do_handle(self, msg):
        chat_id = msg['chat']['id']
        t = time.localtime()
        if t.tm_wday in (0, 1, 2, 3, 4) and t.tm_hour in (2, 3, 4):
            if self.settings['time_sent'] < get_day_number():
                await self.send_message(chat_id, 'HALOOBOT-HUOMAUTUS: Haluaisin huomauttaa että kello on %s arkipäivä-aamuyöllä. Ehkä kannattaisi mennä nukkumaan?' % time.strftime('%H:%M'))
                self.settings['time_sent'] = get_day_number()
                print('Haloobot-huomautus suoritettu!')


class ReplyHandler(TextHandler, StickerHandler):
    
    handle_keys = ['reply_to_message.from.username']
    ignore_keys = []
    reply_starts = ['I would like to put emphasis on ',
                    'I\'d like to add ',
                    'What about ',
                    'How about ',
                    'Have you ever thought about this: ',
                    'My opinion of your message is ']
    
    async def do_handle(self, msg):
        content_type, _, chat_id = telepot.glance(msg)
        msg_id = msg['message_id']
        if msg['reply_to_message']['from']['username'] != self.settings['name']:
            return False
        oldtrigger = self.settings['trigger']
        self.settings['trigger'] = 1.0
        if content_type == 'sticker':
            reply = self.process_sticker(msg, False)
        else:
            message = self.process_msg(msg, False)
            reply = 'Thank you for replying! '
            reply += random.choice(self.reply_starts)
            if message:
                random.shuffle(message)
                reply += ' '.join(message)
            else:
                reply += 'nothing.'
        self.settings['trigger'] = oldtrigger
        if content_type == 'sticker':
            await self.send_sticker(chat_id, reply['file_id'], msg_id)
        else:
            await self.send_reply(chat_id, msg_id, reply)
        print('Replied to %s' % msg_id)
        return True


