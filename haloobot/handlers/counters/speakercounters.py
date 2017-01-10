def add_speaker(msg, tables):
    if 'from' not in msg.keys():
        return False
    frm = msg['from']
    entry = tables['speakers'].find_one(id = frm['id'])
    if entry != None:
        return False
    tables['speakers'].insert({'id': frm['id'], 'first_name': frm['first_name'], 'total_messages': 0,
                     'total_text': 0, 'longest_message': 0, 'average_message': 0.0,
                     'total_stickers': 0, 'total_triggers': 0})
    return True
    
def update_speaker(msg, tables):
    if 'from' not in msg.keys() or 'text' not in msg.keys():
        return
    entry = tables['speakers'].find_one(id = msg['from']['id'])
    if entry == None:
        if add_speaker(msg, tables):
            entry = tables['speakers'].find_one(id = msg['from']['id'])
        else:
            return
    entry['total_messages'] += 1
    tables['speakers'].update(entry, ['id'])
    
def update_speaker_text(msg, tables):
    if 'from' not in msg.keys() or 'text' not in msg.keys():
        return
    entry = tables['speakers'].find_one(id = msg['from']['id'])
    if entry == None:
        if add_speaker(msg):
            entry = tables['speakers'].find_one(id = msg['from']['id'])
        else:
            return
    entry['total_text'] += 1
    msglen = len(msg['text'])
    entry['average_message'] = (entry['average_message'] * (entry['total_text'] - 1) + msglen) / entry['total_text']
    if msglen > entry['longest_message']:
        entry['longest_message'] = msglen
        print('New longest message for %s: %s chars!' % (entry['first_name'], msglen))
    tables['speakers'].update(entry, ['id'])

def update_speaker_stickers(msg, tables):
    if 'from' not in msg.keys() or 'sticker' not in msg.keys():
        return
    entry = tables['speakers'].find_one(id = msg['from']['id'])
    if entry == None:
        if add_speaker(msg):
            entry = tables['speakers'].find_one(id = msg['from']['id'])
        else:
            return
    entry['total_stickers'] += 1
    tables['speakers'].update(entry, ['id'])

def update_speaker_triggers(msg, tables):
    if 'from' not in msg.keys():
        return
    entry = tables['speakers'].find_one(id = msg['from']['id'])
    if entry == None:
        if add_speaker(msg):
            entry = tables['speakers'].find_one(id = msg['from']['id'])
        else:
            return
    entry['total_triggers'] += 1
    print('More triggers for %s!' % entry['first_name'])
    tables['speakers'].update(entry, ['id']) 