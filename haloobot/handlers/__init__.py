from . import basichandlers, commandhandlers

def add_all(handlers, bot, tables, messages, settings):
    basichandlers.add_all(handlers, bot, tables, messages, settings)

def get_command_handler(bot, tables, messages, settings):
    return commandhandlers.CommandHandler([], bot, tables, messages, settings)