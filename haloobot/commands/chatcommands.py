import random, asyncio, os
from haloobot.commands.base import Command
from haloobot.utils.time import temporary_setting_change
from haloobot.utils.food import getmenu
from haloobot.utils.reddit import get_random_meme

def add_all(commands, tables, messages, settings):
    SendVoiceCommand(commands, tables, messages, settings)
    SendAudioCommand(commands, tables, messages, settings)
    ListAudioCommand(commands, tables, messages, settings)
    GetMenuCommand(commands, tables, messages, settings)
    AddAudioCommand(commands, tables, messages, settings)
    GetMemeCommand(commands, tables, messages, settings)
    AddMemeSourceCommand(commands, tables, messages, settings)

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


class SendAudioCommand(Command):
    
    comtext = 'playme'
    minargs = 1
    helptext = 'Sends audio clip to chat. Syntax: /playme "[audio clip name]"'
    
    def run_command(self, args):
        return (args[0], 'audio')

class ListAudioCommand(Command):
    
    comtext = 'listclips'
    minargs = 0
    helptext = 'Lists available audio clips'
    
    def run_command(self, args):
        audiopath = os.path.join('audio')
        if not os.path.isdir(audiopath): # TODO: Move this to some place where it makes more sense?
            os.makedirs(audiopath)
        clips = os.listdir(audiopath)
        if clips:
            return 'Available clips: ' + ', '.join(sorted(map(lambda x: x.split('.')[0], clips)))
        else:
            return 'No audio clips available ):'

class AddAudioCommand(Command):
    
    comtext = 'addclip'
    minargs = 1
    helptext = 'Adds audio clip. Use by replying to an audio message with /addclip "[clip name]"'
    requires_message = True
    
    def run_command(self, args, msg):
        if 'reply_to_message' not in msg:
            return 'To use addclip, please reply to the audio message containing the clip!'
        original_msg = msg['reply_to_message']
        if 'audio' not in original_msg:
            return 'That message doesn\'t contain an audio clip!'
        audio = original_msg['audio']
        return (audio['file_id'], 'download', 'audio', args[0], 'Audio clip %s downloaded!' % args[0], 'Couldn\'t download the clip >:')

class GetMenuCommand(Command):
    
    comtext = 'getmenu'
    minargs = 0
    helptext = 'Get today\'s Unicafe menu. 100% accurate'
    
    def run_command(self, args):
        return 'Tänään tarjolla: ' + getmenu()

class GetMemeCommand(Command):

    comtext = 'getmeme'
    minargs = 0
    helptext = 'Get a random fresh new meme from Reddit. You can optionally specify the subreddit with /getmeme "[subreddit]".'

    async def run_command(self, args):
        meme_file_name, meme_file = await get_random_meme(subreddit = args[0] if len(args) > 0 else None, db = self.tables['db'])
        return (meme_file, meme_file_name, None)

class AddMemeSourceCommand(Command):
    
    comtext = 'addsource'
    minargs = 1
    helptext = 'Add a source for random fresh may mays. Usage: /addsource "[subreddit]"'
    
    async def run_command(self, args):
        if self.tables['sources'].find_one(name = args[0]) != None:
            return '%s is already a source for dank may mays.' % args[0]
        meme_file_name, meme_file = await get_random_meme(subreddit = args[0])
        if meme_file_name == None:
            return 'No memes found in %s - try again if you are sure that there are some!' % args[0]
        self.tables['sources'].insert({'name': args[0]})
        return ('Added %s - an example meme below!\n' % args[0]) + meme_file
