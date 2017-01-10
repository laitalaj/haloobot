from . import messagecommands, settingscommands, statcommands, utilitycommands, timecommands

def add_all(commands, tables, messages, settings):
    messagecommands.add_all(commands, tables, messages, settings)
    settingscommands.add_all(commands, tables, messages, settings)
    statcommands.add_all(commands, tables, messages, settings)
    utilitycommands.add_all(commands, tables, messages, settings)
    timecommands.add_all(commands, tables, messages, settings)