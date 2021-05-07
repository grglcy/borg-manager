from . import LEVEL_DEBUG, LEVEL_INFO, LEVEL_WARNING, LEVEL_ERROR, LEVEL_CRITICAL


class Log(object):
    def __init__(self, level=LEVEL_WARNING):
        self.level = LEVEL_WARNING

    def output(self, level, message):
        if self.level <= level:
            print(message)

    def debug(self, message):
        return self.output(LEVEL_DEBUG, message)

    def info(self, message):
        return self.output(LEVEL_INFO, message)

    def warn(self, message):
        return self.output(LEVEL_WARNING, message)

    def error(self, message):
        return self.output(LEVEL_ERROR, message)

    def critical(self, message):
        return self.output(LEVEL_CRITICAL, message)
