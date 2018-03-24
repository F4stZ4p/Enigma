from logging import getLoggerClass, NOTSET, addLevelName, setLoggerClass

LEVEL_STYLES = {
    'debug': {'color': 'green'},
    'info': {},
    'plugin': {'color': 'blue'},
    'warning': {'color': 'yellow'},
    'error': {'color': 'red'},
    'critical': {'color': 'red', 'bold': True}
}

PLUGIN = 25


class EnigmaLogger(getLoggerClass()):
    def __init__(self, name, level=NOTSET):
        super().__init__(name, level)

        addLevelName(PLUGIN, "PLUGIN")

    def plugin(self, msg, *args, **kwargs):
        if self.isEnabledFor(PLUGIN):
            self._log(PLUGIN, msg, args, **kwargs)


setLoggerClass(EnigmaLogger)
