import random, asyncio, os
from subprocess import check_output
from emoji import emojize
from haloobot.commands.base import Command
from haloobot.utils.blame import praise
from haloobot.utils.time import temporary_setting_change
from haloobot.utils.reddit import get_random_meme
from haloobot.utils.excuse import getexcuse
from haloobot.utils.fingerpori import get_newest_fingerpori, get_newest_fingerpori_b, get_random_fingerpori
from haloobot.utils.fokit import get_newest_fokit, get_random_fokit
from haloobot.utils.smbc import get_newest_smbc, get_random_smbc
from haloobot.utils.aijamatto import getmatto

def add_all(commands, tables, messages, settings):
    SendVoiceCommand(commands, tables, messages, settings)
    SendAudioCommand(commands, tables, messages, settings)
    ListAudioCommand(commands, tables, messages, settings)
    GetExcuseCommand(commands, tables, messages, settings)
    AddAudioCommand(commands, tables, messages, settings)
    RemoveAudioCommand(commands, tables, messages, settings)
    GetMemeCommand(commands, tables, messages, settings)
    AddMemeSourceCommand(commands, tables, messages, settings)
    ListMemeSourcesCommand(commands, tables, messages, settings)
    PraiseCommand(commands, tables, messages, settings)
    FortuneCowCommand(commands, tables, messages, settings)
    FingerporiCommand(commands, tables, messages, settings)
    FingerporiBCommand(commands, tables, messages, settings)
    RandomPoriCommand(commands, tables, messages, settings)
    MattoCommand(commands, tables, messages, settings)
    FokitCommand(commands, tables, messages, settings)
    RandomFokitCommand(commands, tables, messages, settings)
    SmbcCommand(commands, tables, messages, settings)
    RandomSmbcCommand(commands, tables, messages, settings)

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
        if 'audio' in original_msg:
            audio = original_msg['audio']
            atype = 'mp3'
        elif 'voice' in original_msg:
            audio = original_msg['voice']
            atype = 'ogg'
        else:
            return 'That message doesn\'t contain an audio clip!'
        return (audio['file_id'], 'download', 'audio/{}'.format(atype), args[0], 'Audio clip %s downloaded!' % args[0], 'Couldn\'t download the clip >:')

class RemoveAudioCommand(Command):

    comtext = 'rmclip'
    minargs = 1
    helptext = 'Removes audio clip. Usage: /rmclip "[clip name]"'

    def run_command(self, args):
        return (args[0], 'rm', 'audio', 'Audio clip %s removed! (or it didn\'t exist at all)' % args[0], 'Couldn\'t remove %s >:' % args[0])

class GetExcuseCommand(Command):

    comtext = 'getexcuse'
    minargs = 0
    helptext = '''Get an excuse as to why you're code a shit'''

    def run_command(self, args):
        return getexcuse()

class GetMemeCommand(Command):

    comtext = 'getmeme'
    minargs = 0
    helptext = 'Get a random fresh new meme from Reddit. You can optionally specify the subreddit with /getmeme "[subreddit]".'

    async def run_command(self, args):
        _, meme_msg = await get_random_meme(subreddit = args[0] if len(args) > 0 else None, db = self.tables['db'])
        return meme_msg

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
        print('Adding %s as meme source...' % args[0])
        return ('Added %s as a meme source - an example meme below!\n' % args[0]) + meme_file


class ListMemeSourcesCommand(Command):
    
    comtext = 'listsources'
    minargs = 0
    helptext = 'List meme sources'
    
    def run_command(self, args):
        return 'Meme sources:\n' + '\n'.join(map(lambda s: s['name'], self.tables['sources'].all()))


class PraiseCommand(Command):

    comtext = 'praise'
    minargs = 0
    helptext = 'Praise the contributors!'

    PRAISE_EMOJI = [
        ':smiling_face_with_heart-eyes:', ':star-struck:', ':red_heart:',
        ':OK_hand:', ':thumbs_up:', ':clapping_hands:', ':raising_hands:',
        ':folded_hands:', ':flexed_biceps:', ':person_bowing:',
        ':man_mage:', ':prince:', ':man_student:', ':man_scientist:',
        ':genie:', ':lion_face:', ':glowing_star:'
        ':military_medal:', ':sports_medal:', ':trophy:', ':crown:',
        ':gem_stone:', ':place_of_worship:'
    ]

    def run_command(self, args):
        print('Praising the contributors!')
        to_praise = [emojize('*{}*{}'.format(c, random.choice(self.PRAISE_EMOJI))) for c in praise(self.settings['praise_length'])]
        return 'PRAISE THE {}: {}'.format('CONTRIBUTORS' if len(to_praise) > 1 else 'CREATOR', ', '.join(sorted(to_praise))), 'Markdown'


class FortuneCowCommand(Command):

    comtext = 'fortune'
    minargs = 0
    helptext = 'Returns your fortune in cow format. Usage: /fortune "[optional cowsay]"'
    
    COWEYES = [
        'b', 'd', 'g', 'p', 's', 't', 'w', 'y', #Standard
        'e^^', 'eಠಠ' #Custom
    ]

    def run_command(self, args):
        fortune = args[0] if len(args) >= 1 else check_output(['fortune', '-a'])
        cow = check_output(['cowsay', '-{}'.format(random.choice(self.COWEYES)), fortune])
        return ('```' + cow.decode() + '```', 'Markdown')

class FingerporiCommand(Command):

    comtext = 'fingerpori'
    minargs = 0
    helptext = 'Gives you today\'s Fingerpori'

    async def run_command(self, args):
        image_url = await get_newest_fingerpori()
        self.settings['last_fingerpori_url'] = image_url
        return (image_url, 'image')

class FingerporiBCommand(Command):

    comtext = 'fingerpori_b'
    minargs = 0
    helptext = 'Gives you today\'s alternative Fingerpori'

    async def run_command(self, args):
        image_url = await get_newest_fingerpori_b()
        self.settings['last_fingerpori_b_url'] = image_url
        return (image_url, 'image')

class RandomPoriCommand(Command):

    comtext = 'randompori'
    minargs = 0
    helptext = 'Gives you a random Fingerpori'

    async def run_command(self, args):
        return (await get_random_fingerpori(), 'image')

class MattoCommand(Command):

    comtext = 'dudecarpet'
    minargs = 0
    helptext = 'Moro dude :D mitä dude.'

    async def run_command(self, args):
        return await getmatto()

class FokitCommand(Command):
    comtext = 'fokit'
    minargs = 0
    helptext = 'Gives you today\'s Fok_It'

    async def run_command(self, args):
        image_url = await get_newest_fokit()
        self.settings['last_fokit_url'] = image_url
        return (image_url, 'image')

class RandomFokitCommand(Command):
    comtext = 'randomfokit'
    minargs = 0
    helptext = 'Gives you a random Fok_It'

    async def run_command(self, args):
        return (await get_random_fokit(), 'image')

class SmbcCommand(Command):

    comtext = 'smbc'
    minargs = 0
    helptext = 'Gives you today\'s SMBC'

    async def run_command(self, args):
        image_url, caption = await get_newest_smbc()
        self.settings['last_smbc_url'] = image_url
        return (image_url, 'image', caption)

class RandomSmbcCommand(Command):
    comtext = 'randomsmbc'
    minargs = 0
    helptext = 'Gives you a random SMBC'

    async def run_command(self, args):
        image_url, caption = await get_random_smbc()
        return (image_url, 'image', caption)
