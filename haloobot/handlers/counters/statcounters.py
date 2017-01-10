def update_count(stat, tables):
    entry = tables['stats'].find_one(type=stat)
    if entry==None:
        print('Couldn\'t find entry for stat %s!' % stat)
        return
    entry['count'] += 1
    tables['stats'].update(entry, ['type'])
    print('Count for %s is now %s' % (stat, entry['count']))

def update_skipped(stat, tables):
    entry = tables['stats'].find_one(type=stat)
    if entry==None:
        print('Couldn\'t find entry for stat %s!' % stat)
        return
    entry['skipped'] += 1
    tables['stats'].update(entry, ['type'])
    print('Skipped for %s is now %s' % (stat, entry['skipped']))