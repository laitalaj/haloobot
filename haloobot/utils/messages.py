import emoji, time

#TODO: Make flexible
def do_replaces(msg, message, match):
    for i in range(len(match.groups()) + 1):
        group = match.group(i)
        if group != None:
            message = message.replace('$%s' % i, group)
    if 'from' in msg.keys():
        message = message.replace('$name', msg['from']['first_name'])
    message = message.replace('$time', time.strftime('%H:%M'))
    message = emoji.emojize(message, True)
    return message