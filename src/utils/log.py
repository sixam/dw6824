from dp.src.utils.utils import Utils
import logging

class Log:
    def __init__(self, id):
        self.id = id
        self.log = logging.getLogger('log-%s' % self.id)
        fname = Utils.getLogPath('mainlog', self.id)
        fhandle = logging.FileHandler(fname)

        formatter = logging.Formatter('%(message)')
        #%(levelname)s
        fhandle.setFormatter(formatter)
        self.log.addHandler(fhandle)


    def log(*args):
        s = str()
        for arg in args:
            s += arg
        s += '\n'
        self.log.info(s)
