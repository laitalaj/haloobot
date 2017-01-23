import random, asyncio
from haloobot.commands.base import Command
from haloobot.utils.time import temporary_setting_change

def add_all(commands, tables, messages, settings):
    SendVoiceCommand(commands, tables, messages, settings)

class SendVoiceCommand(Command):
    
    comtext = 'voiceme'
    minargs = 1
    helptext = 'Sends given text as an audio message to the chat. Syntax: /voiceme "[message]" "[optional: language code]"'
    
    def run_command(self, args):
        if len(args[0]) > self.settings['tts_max_length']:
            return 'Sorry, too long message! (max length %s characters)' % self.settings['tts_max_length']
        if len(args) > 1:
            lang = args[1]
        else:
            lang = random.choice(self.settings['tts_lang'])
        if not self.settings['tts_cooldown']:
            loop = asyncio.get_event_loop()
            loop.create_task(
                temporary_setting_change(self.settings, 'tts_cooldown', True, self.settings['tts_cooldown_time'])
                )
            return (args[0], 'voice', lang)
        else:
            return 'Sorry, cooling down (-: (text to speak cooldown is %s seconds)' % self.settings['tts_cooldown_time']