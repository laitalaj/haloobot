def dict_contains_key(d, key):
    if type(key) == str:
        keyparts = key.split('.')
    else:
        keyparts = key
    if len(keyparts) > 1:
        if keyparts[0] in d.keys():
            if type(d[keyparts[0]]) == dict:
                return dict_contains_key(d[keyparts[0]], keyparts[1:])
    else:
        return keyparts[0] in d.keys()
    return False
