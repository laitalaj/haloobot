import random, time, asyncio
from haloobot.utils.messages import do_replaces
from haloobot.utils.time import get_day_number, temporary_setting_change
from haloobot.utils.food import getmenu
from haloobot.handlers.base import Handler
from haloobot.handlers.counters import speakercounters, statcounters

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
        message = self.process_msg(msg)
        if message:
            random.shuffle(message)
            messagestr = ' '.join(message)
            voice_possible = len(messagestr) < self.settings['tts_max_length'] and not self.settings['tts_cooldown']
            if voice_possible and random.random() < self.settings['trigger']:
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
    
    async def do_handle(self, msg):
        chat_id = msg['chat']['id']
        speakercounters.update_speaker_stickers(msg, self.tables)
        sticker = msg['sticker']
        if self.tables['stickers'].insert_ignore({'file_id': sticker['file_id']}, ['file_id']):
            print('Added new sticker ...%s!' % sticker['file_id'][-8:])
        if 'emoji' in sticker: # Keep that old db working and the emoji up to date
            self.tables['stickers'].update({'file_id': sticker['file_id'], 'emoji': sticker['emoji']}, ['file_id'])
        if random.random() < self.settings['trigger']:
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
            await self.send_sticker(chat_id, to_send['file_id'])
            print('Sent sticker ...%s as a reply to ...%s' % (to_send['file_id'][-8:], sticker['file_id'][-8:]))
            speakercounters.update_speaker_triggers(msg, self.tables)
        else:
            print('Didn\'t reply to sticker ...%s' % sticker['file_id'][-8:])
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
        if t.tm_wday in (0, 1, 2, 3, 4) and t.tm_hour in (8, 9, 10, 11):
            if self.settings['food_time_sent'] < get_day_number():
                await self.send_message(chat_id, 'HALOOBOT-HUOMAUTUS: Haluaisin huomauttaa että exactumissa on tänään tarjolla:' + getmenu() + 'Muistathan syödä kasvaaksesi isoksi!')
                self.settings['food_time_sent'] = get_day_number()
                print('Haloobot-huomautus suoritettu!')




class ReplyHandler(TextHandler):
    
    handle_keys = ['reply_to_message.from.username']
    ignore_keys = []
    reply_starts = ['I would like to put emphasis on ',
                    'I\'d like to add ',
                    'What about ',
                    'How about ',
                    'Have you ever thought about this: ',
                    'My opinion of your message is ']
    
    async def do_handle(self, msg):
        chat_id = msg['chat']['id']
        msg_id = msg['message_id']
        if msg['reply_to_message']['from']['username'] != self.settings['name']:
            return False
        oldtrigger = self.settings['trigger']
        self.settings['trigger'] = 1.0
        message = self.process_msg(msg, False)
        self.settings['trigger'] = oldtrigger
        reply = 'Thank you for replying! '
        reply += random.choice(self.reply_starts)
        if message:
            random.shuffle(message)
            reply += ' '.join(message)
        else:
            reply += 'nothing.'
        await self.send_reply(chat_id, msg_id, reply)
        print('Replied to %s' % msg_id)
        return True


