import subprocess
from os import path, remove
from gtts import gTTS

# Thanks to Kirk Strauser at Stackoverflow
# You'll need mpg123 and oggenc for this to work, sorry about that
# TODO: Can this be done asynchronously?
def text_to_ogg(text, ttsid = 0):
    tts = gTTS((text))
    mp3path = path.abspath(path.join('tts', 'tts%s.mp3' % ttsid))
    oggpath = path.abspath(path.join('tts', 'tts%s.ogg' % ttsid))
    tts.save(str(mp3path)) #Converting to str just to be certain
    frommp3 = subprocess.Popen(['mpg123', '-w', '-', str(mp3path)], stdout=subprocess.PIPE)
    toogg = subprocess.Popen(['oggenc', '-'], stdin=frommp3.stdout, stdout=subprocess.PIPE)
    outfile = open(oggpath, 'wb')
    while True:
        data = toogg.stdout.read(1024 * 100)
        if not data:
            break
        outfile.write(data)
    remove(mp3path)
    return outfile