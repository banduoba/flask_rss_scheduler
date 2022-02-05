import logging
import logging.handlers
import os
import sys


class logFactory(object):
    def __init__(self, name):
        self.log = logging.getLogger(name)
        self.logpath = os.path.abspath(os.path.join(os.getcwd(), "logs"))
        if not os.path.exists(self.logpath):
            os.makedirs(self.logpath)
        self.logname = os.path.join(self.logpath, f'{name}.log')
        self.logsize = 1024 * 1024 * int(8)
        self.lognum = int(3)

        self.fmt = logging.Formatter(
            '[%(levelname).1s] %(asctime)s - [pid:%(process)d] - %(filename)s - [%(lineno)d]: %(message)s',
            '%Y/%m/%d %H:%M:%S')

        self.handle1 = logging.handlers.RotatingFileHandler(self.logname, maxBytes=self.logsize,
                                                            backupCount=self.lognum, encoding='utf-8')
        self.handle1.setFormatter(self.fmt)
        self.log.addHandler(self.handle1)

        self.handle2 = logging.StreamHandler(stream=sys.stdout)
        self.handle2.setFormatter(self.fmt)
        self.log.addHandler(self.handle2)

        self.log.setLevel(logging.INFO)
