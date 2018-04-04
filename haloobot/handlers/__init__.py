from . import basichandlers, commandhandlers, schedulehandlers

def add_all(handlers, bot, tables, messages, settings):
    basichandlers.add_all(handlers, bot, tables, messages, settings)

def get_command_handler(bot, tables, messages, settings):
    return commandhandlers.CommandHandler([], bot, tables, messages, settings)

def get_schedule_handler(bot, tables, messages, settings):
    return schedulehandlers.ScheduleHandler([], bot, tables, messages, settings)