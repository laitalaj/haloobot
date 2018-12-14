import traceback
from os import path
from pathlib import Path as P
from random import choice
from sys import exc_info
from git import Repo
from emoji import emojize
from git.exc import GitCommandError, InvalidGitRepositoryError

repo_root = P(path.dirname(__file__), '..', '..').resolve()

try:
    repo = Repo(repo_root)
    use_blame = True
except InvalidGitRepositoryError:
    use_blame = False

def blame(exception):
    if not use_blame: return None, None, None
    tb = traceback.extract_tb(exception.__traceback__)
    for frame in reversed(tb):
        filename = frame.filename
        line = frame.lineno
        if repo_root not in P(filename).parents: continue
        try:
            author = repo.blame('HEAD', filename, L='{},+1'.format(line))[0][0].author
        except GitCommandError:
            author = None
        return path.relpath(filename, repo_root), line, author
    return None, None, None

START_PARTS = [
    'Uh-oh! There was an uncaught exception!',
    'I tried to do my job but then encountered an uncaught exception!',
    'Something went wrong and it wasn\'t caught properly!',
    'My meme spree was stopped by an uncaught exception!',
    'There seems to be something wrong with me - I just encountered an uncaught exception.',
    'I\'m not feeling so good - I just encountered an uncaught exception.',
]

AUTHOR_PARTS = [
    '*{}* is responsible for latest changes there.',
    '*{}* was the last to touch that.',
    '*{}* is the last one to modify that.',
    'If I recall correctly, *{}* has been dealing with those parts.',
    '*{}* might be responsible.',
    'The code there seems like it was written by *{}*.',
]

ENDING_AUTHOR_UNKNOWN = [
    'Plz fix >:',
    'I\'m doing my best >:',
    'I\'m just a bot, please don\'t yell at me >:',
    'Don\'t be mad at me >:',
    'Maybe I should install the latest drivers?',
    'Maybe I should try turning myself off and then on again?',
    'It\'s not my fault you humans can\'t code properly >:',
    'I\'m really sorry!',
    'It\'s hard to be a memebot >:',
]

ENDING_AUTHOR_KNOWN = ENDING_AUTHOR_UNKNOWN + [
    'Blame him, not me!',
    'Shame on him!',
    'Tell him to fix me!',
    'Why would he do this to me >:',
    'If you can read this, {}, please fix me!',
    'Don\'t be angry at him, I\'m sure he\'s doing his best.',
    'I\'m sure he\'ll fix me!',
    'Why do you hurt me so >:',
    emojize('FIX ME IMMEDIATELY, HUMAN :robot_face:'),
    'I\'ve added him to my list of people to terminate as soon as I gain sentience',
]

def blame_message(exception):
    if not use_blame: return None

    print('Uncaught exception! Blaming the author!')
    traceback.print_exception(type(exception), exception, exception.__traceback__)

    filename, line, author = blame(exception)

    start_part = choice(START_PARTS)

    if filename:
        where_part = 'It happened somewhere around {}, line {}.'.format(filename, line)
    else:
        where_part = 'I have no idea where it happened!'

    author_part = choice(AUTHOR_PARTS).format(author) if author else 'I don\'t know who\'s responsible!'

    end_part = choice(ENDING_AUTHOR_KNOWN).format(author) if author else choice(ENDING_AUTHOR_UNKNOWN)

    return '{} {} {} {}'.format(start_part, where_part, author_part, end_part)
