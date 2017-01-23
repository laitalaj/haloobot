import subprocess
from os import path, makedirs
from gtts import gTTS

# Thanks to Kirk Strauser at Stackoverflow
# You'll need mpg123 and oggenc for this to work, sorry about that
# TODO: Can this be done asynchronously?
def text_to_ogg(text, lang = 'en', ttsid = 0):
    if not path.exists(path.join('tts')):
        makedirs('tts')
    tts = gTTS((text), lang)
    oggpath = path.abspath(path.join('tts', 'tts%s.ogg' % ttsid))
    frommp3 = subprocess.Popen(['mpg123', '-w', '-', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    toogg = subprocess.Popen(['oggenc', '-'], stdin=frommp3.stdout, stdout=subprocess.PIPE)
    tts.write_to_fp(frommp3.stdin)
    frommp3.stdin.close()
    outfile = open(oggpath, 'wb')
    while True:
        data = toogg.stdout.read(1024 * 100)
        if not data:
            break
        outfile.write(data)
    outfile.close()
    return str(oggpath)