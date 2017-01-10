from haloobot.commands.base import Command
from emoji import emojize

def add_all(commands, tables, messages, settings):
    StatsCommand(commands, tables, messages, settings)
    PeopleStatsCommand(commands, tables, messages, settings)

class StatsCommand(Command):
    
    comtext = 'stats'
    minargs = 0
    helptext = 'Sends haloobot\'s stats'
    
    def run_command(self, args):
        to_send = self.tables['stats'].find(order_by='-count', _limit=5)
        trigger = self.settings['trigger']
        message = 'I\'m triggered %s percent of the time.\n' % int(trigger * 100)
        message += 'I remember %s ebin stickers!\n' % self.tables['stickers'].count()
        message += 'Top memes:\n'
        for m in to_send:
            message += '* I\'ve sent "%s" %s times! I\'ve skipped %s chances to maymay. \n' % (m['message'], m['count'], m['skipped'])
        print('Sending stats!')
        return emojize(message, True)


class PeopleStatsCommand(Command):
    
    comtext = 'pstats'
    minargs = 0
    helptext = 'Sends stats of the people using haloobot'
    
    def run_command(self, args):
        message = 'People stats!\n'
        speakers = self.tables['speakers']
        most_messages = speakers.find_one(order_by='-total_messages')
        message += 'Most messages: %s with %s messages!\n' % (most_messages['first_name'], most_messages['total_messages'])
        longest_message = speakers.find_one(order_by='-longest_message')
        message += 'Longest message: %s with %s characters!\n' % (longest_message['first_name'], longest_message['longest_message'])
        laverage_message = speakers.find_one(order_by='-average_message')
        message += 'Longest average message: %s with %s characters!\n' % (laverage_message['first_name'], int(laverage_message['average_message']))
        saverage_message = speakers.find_one(order_by='average_message')
        message += 'Shortest average message: %s with %s characters!\n' % (saverage_message['first_name'], int(saverage_message['average_message']))
        most_stickers = speakers.find_one(order_by='-total_stickers')
        message += 'Most stickers: %s with %s stickers sent!\n' % (most_stickers['first_name'], most_stickers['total_stickers'])
        most_triggers = speakers.find_one(order_by='-total_triggers')
        message += 'Most triggering: %s , who has triggered me %s times!' % (most_triggers['first_name'], most_triggers['total_triggers'])
        return message