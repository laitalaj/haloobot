import subprocess
from os import path, makedirs, remove
from io import BytesIO
from gtts import gTTS

# Thanks to Kirk Strauser at Stackoverflow
# You'll need mpg123 and oggenc for this to work, sorry about that
# TODO: Can this be done asynchronously?
def text_to_ogg(text, lang = 'en', ttsid = 0):
    if not path.exists(path.join('tts')):
        makedirs('tts')
    tts = gTTS((text), lang)
    #mp3path = path.abspath(path.join('tts', 'tts%s.mp3' % ttsid))
    oggpath = path.abspath(path.join('tts', 'tts%s.ogg' % ttsid))
    #frommp3 = subprocess.Popen(['mpg123', '-w', '-', str(mp3path)], stdout=subprocess.PIPE)
    toogg = subprocess.Popen(['oggenc', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    tts.write_to_fp(toogg.stdin)
    outfile = open(oggpath, 'wb')
    while True:
        data = toogg.stdout.read(1024 * 100)
        if not data:
            break
        outfile.write(data)
    outfile.close()
    #remove(mp3path)
    return str(oggpath)