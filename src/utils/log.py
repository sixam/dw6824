from dp.src.utils.utils import Utils
import logging

class Log:
    def __init__(self, id):
        self.id = id
        self.log = logging.getLogger('log-%s' % self.id)
        self.log.setLevel(logging.DEBUG)
        fname = Utils.getLogPath('mainlog', self.id)
        fhandle = logging.FileHandler(fname)
        fhandle.setLevel(logging.DEBUG)

        formatter = logging.Formatter('%(message)s')
        #%(levelname)s
        fhandle.setFormatter(formatter)
        if not self.log.handlers:
            self.log.addHandler(fhandle)


    def Print(self, *args):
        s = str()
        for arg in args:
            s += str(arg)
            s += ' '
        self.log.info(s)
