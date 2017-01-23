import random
from haloobot.commands.base import Command

def add_all(commands, tables, messages, settings):
    SendVoiceCommand(commands, tables, messages, settings)

class SendVoiceCommand(Command):
    
    comtext = 'voiceme'
    minargs = 1
    helptext = 'Sends given text as an audio message to the chat. Syntax: /voiceme "[message]" "[optional: language code]"'
    
    def run_command(self, args):
        if len(args) > 1:
            lang = args[1]
        else:
            lang = random.choice(self.settings['tts_lang'])
        if not self.settings['tts_cooldown']:
            return (args[0], 'voice', lang)
        else:
            return 'Sorry, cooling down (-: (text to speak cooldown is %s seconds)' % self.settings['tts_cooldown_time']