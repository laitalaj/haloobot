from haloobot.commands.base import Command
from haloobot.utils.regex import validate_regex
from emoji import emojize

def add_all(commands, tables, messages, settings):
    AddMessageCommand(commands, tables, messages, settings)
    ChangeRegexCommand(commands, tables, messages, settings)
    ChangeMessageCommand(commands, tables, messages, settings)
    GetNameCommand(commands, tables, messages, settings)
    GetRegexCommand(commands, tables, messages, settings)
    GetMessageCommand(commands, tables, messages, settings)
    ListNamesCommand(commands, tables, messages, settings)

class AddMessageCommand(Command):
    
    comtext = 'addmessage'
    minargs = 3
    helptext = 'Adds a message. Syntax: /addmessage "[name]" "[regex]" "[message]" "[optional: "True" if case-sensitive]"'
    
    def run_command(self, args):
        name = args[0]
        regex = args[1]
        message = args[2]
        if len(args) > 3:
            case_sensitive = args[3] == 'True'
        else:
            case_sensitive = False
        if self.tables['sends'].find_one(type = name) != None:
            return 'There\'s already a message with name %s!' % name
        compiledre = validate_regex(regex, case_sensitive)
        if type(compiledre) == str:
            return compiledre
        self.messages[name] = (compiledre, message)
        self.tables['sends'].insert({'type': name, 'regex': regex, 'message': message, 'case_sensitive': bool(case_sensitive)})
        self.tables['stats'].insert({'type': name, 'message': message, 'count': 0, 'skipped': 0})
        print('Added message %s' % name)
        return 'Successfully added message %s!' % message


class ChangeRegexCommand(Command):
    
    comtext = 'changeregex'
    minargs = 2
    helptext = 'Changes a message\'s regex. Syntax: /changeregex "[name]" "[new regex]" "[optional: "True" if case-sensitive]"'
    
    def run_command(self, args):
        name = args[0]
        regex = args[1]
        if len(args) > 2:
            case_sensitive = args[2] == 'True'
        else:
            case_sensitive = False
        compiledre = validate_regex(regex, case_sensitive)
        if type(compiledre) == str:
            return compiledre
        entry = self.tables['sends'].find_one(type = name)
        if entry == None:
            return 'Couldn\'t find message with name %s' % name
        entry['regex'] = regex
        self.tables['sends'].update(entry, ['type'])
        self.messages[name] = (compiledre, emojize(entry['message'], True))
        print('Changed regex for %s' % name)
        return 'Regex changed successfully for %s' % name
        

class ChangeMessageCommand(Command):
    
    comtext = 'changemessage'
    minargs = 2
    helptext = 'Changes message that will be sent when triggered. Syntax: /changemessage "[name]" "[new message]"'
    
    def run_command(self, args):
        name = args[0]
        message = args[1]
        entry = self.tables['sends'].find_one(type = name)
        statentry = self.tables['stats'].find_one(type = name)
        if entry == None:
            return 'Couldn\'t find message with name %s' % name
        if statentry == None:
            print('No stat entry for %s!!!' % name)
        else:
            statentry['message'] = message
            self.tables['stats'].update(statentry, ['type'])
        entry['message'] = message
        self.tables['sends'].update(entry, ['type'])
        self.messages[name] = (self.messages[name][0], emojize(message, True))
        print('Changed message for %s' % name)
        return 'Message changed successfully for %s' % name


class GetNameCommand(Command):
    
    comtext = 'getname'
    minargs = 1
    helptext = 'Finds names for messages containing given string. Syntax: /getname "[part of message]"'
    
    def run_command(self, args):
        table = self.tables['sends'].table
        possibles = self.tables['db'].query(table.select(table.c.message.like('%'+args[0]+'%')))
        message = []
        for p in possibles:
            message.append('- name: %s, message: %s' % (p['type'], p['message']))
            if len(message)>6:
                message.append('(omitted further results)')
                break
        try:
            print('Tried to get names with query %s' % args[0])
        except:
            print('Tried to get names with an unprintable query')
        if message:
            return 'Results:\n' + '\n'.join(message)
        else:
            return 'No results for message %s' % args[0]
        
        
class GetRegexCommand(Command):
    
    comtext = 'getregex'
    minargs = 1
    helptext = 'Gets regex for given name. Syntax: /getregex "[name]"'
    
    def run_command(self, args):
        result = self.tables['sends'].find_one(type = args[0])
        try:
            print('Tried to get regex for %s' % args[0])
        except:
            print('Tried to get regex for an unprintable name')
        if result:
            return 'Regex for %s: %s' % (args[0], result['regex'])
        else:
            return 'No message with name %s found!' % args[0]


class GetMessageCommand(Command):
    
    comtext = 'getmessage'
    minargs = 1
    helptext = 'Gets message for given name. Syntax: /getmessage "[name]"'
    
    def run_command(self, args):
        result = self.tables['sends'].find_one(type = args[0])
        try:
            print('Tried to get message for %s' % args[0])
        except:
            print('Tried to get message for an unprintable name')
        if result:
            return 'Message for %s: %s' % (args[0], result['message'])
        else:
            return 'No message with name %s found!' % args[0]


class ListNamesCommand(Command):
    
    comtext = 'listnames'
    minargs = 0
    helptext = 'Lists names of all messages'
    
    def run_command(self, args):
        results = self.tables['sends'].all()
        message = []
        for r in results:
            message.append(r['type'])
        message.sort()
        print('Sending all names!')
        if message:
            return 'All names: ' + ', '.join(message)
        else:
            return 'No messages found!'
    
    
    
    
