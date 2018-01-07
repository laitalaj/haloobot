if __name__ == '__main__':
    print('Importing...')
    
    import telepot.aio
    import emoji
    import re
    import dataset
    import asyncio
    import sys
    import time
    import haloobot.handlers
    from os import path
    
    print("Loading database...")
    db = dataset.connect('sqlite:///database.db')
    
    print("Initializing data...")
    
    tables = {
        'db': db,
        'stats': db['stats'],
        'sends': db['sends'],
        'settings': db['settings'],
        'stickers': db['stickers'],
        'speakers': db['speakers'],
        'speeches': db['speeches'],
        'songs': db['songs'],
        'sources': db['sources']
        }
    
    #TODO: Initialization for new instances?
    if 'type' not in tables['settings'].columns:
        print("Performing first-time setup of settings...")
        tables['settings'].insert({'type': 'trigger', 'value': '33'})
    
    settings = {
        'name': None,
        'key': None,
        'password': 'please',
        'trigger': int(tables['settings'].find_one(type = "trigger")['value']) / 100,
        'silence': True,
        'tts_cooldown': False,
        'tts_id': 0,
        'tts_lang': ['en'],
        'tts_max_length': 100,
        'tts_cooldown_time': 600
        }
    
    setting_handlers = {
        'tts_lang': lambda x: x.replace(' ', '').split(','),
        'tts_cooldown_time': lambda x: int(x),
        'tts_max_length': lambda x: int(x)
        }
    
    if path.isfile('haloosettings'):
        with open('haloosettings') as haloosettings:
            haloostrings = haloosettings.read().replace(' ', '').split('\n')
            for s in haloostrings:
                try:
                    s_key, s_value = s.split('=')
                    if s_key in setting_handlers.keys():
                        s_value = setting_handlers[s_key](s_value)
                    settings[s_key] = s_value
                except:
                    print('Badly formatted setting: "%s"' % s)
    
    if settings['key'] == None:
        print('No telegram bot api key given in haloosettings - can\'t run haloobot!')
        sys.exit()
    
    regex_to_message = {}
    for s in tables['sends'].all():
        regex_to_message[s['type']] = (re.compile(emoji.emojize(s['regex'], True), 0 if s['case_sensitive'] else re.IGNORECASE), s['message'])
    
    print("Initializing bot with key %s..." % settings['key'])
    bot = telepot.aio.Bot(settings['key'])
    
    print('Preparing message handling...')
    handlers = []
    haloobot.handlers.add_all(handlers, bot, tables, regex_to_message, settings)
    command_handler = haloobot.handlers.get_command_handler(bot, tables, regex_to_message, settings)
    
    async def handle(msg):
        if time.time() - msg['date'] > 60*60: # Skip messages that are older than one hour
            return
        if not await command_handler.handle(msg):
            for h in handlers:
                await h.handle(msg)
    
    print('Launching bot...')
    loop = asyncio.get_event_loop()
    loop.create_task(bot.message_loop(handle))
    
    print('--- READY TO MEME ---')
    loop.run_forever()
