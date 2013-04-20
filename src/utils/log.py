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


    def red(self,*args):
        args = list(args)
        args.insert(0,'\033[31m')
        args.append('\033[0m')
        args = tuple(args)
        self.Print(*args)

    def orange(self,*args):
        args = list(args)
        args.insert(0,'\033[33m')
        args.append('\033[0m')
        args = tuple(args)
        self.Print(*args)

    def blue(self,*args):
        args = list(args)
        args.insert(0,'\033[34m')
        args.append('\033[0m')
        args = tuple(args)
        self.Print(*args)

    def green(self,*args):
        args = list(args)
        args.insert(0,'\033[32m')
        args.append('\033[0m')
        args = tuple(args)
        self.Print(*args)

    def purple(self,*args):
        args = list(args)
        args.insert(0,'\033[35m')
        args.append('\033[0m')
        args = tuple(args)
        self.Print(*args)

    def Print(self, *args):
        s = str()
        for arg in args:
            s += str(arg)
            s += ' '
        self.log.info(s)
