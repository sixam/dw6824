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

        # log options
        self.show_lock    = True
        self.show_rpc     = True
        self.show_engine  = True
        self.show_release = True
        self.show_ui      = True

        # for recursion debug
        #self.accu = ""

    def exception(self, *args):
        self.log.exception('Something terrible happened')

    def accumulate(self,*args):
        s = ''
        for arg in args:
            s += str(arg)
            s += ' '
        s += '\n'
        self.accu += s

    def flush(self):
        self.accu = ''

    def release(self):
        if not self.show_release:
            return
        s = self.accu
        self.accu = ''
        self.red('Accumulated logs')
        self.orange(s)


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

    def lock(self,*args):
        if self.show_lock:
            args = list(args)
            args.insert(0,'\033[33mLK\033[0m:')
            args = tuple(args)
            self.Print(*args)

    def rpc(self,*args):
        if self.show_rpc:
            args = list(args)
            args.insert(0,'\033[35mRPC\033[0m:')
            args = tuple(args)
            self.Print(*args)

    def ui(self,*args):
        if self.show_ui:
            args = list(args)
            args.insert(0,'\033[32mUI\033[0m:')
            args = tuple(args)
            self.Print(*args)

    def engine(self,*args):
        if self.show_engine:
            args = list(args)
            args.insert(0,'\033[34mOE\033[0m:')
            args = tuple(args)
            self.Print(*args)


    def Print(self, *args):
        s = str()
        for arg in args:
            s += str(arg)
            s += ' '
        self.log.info(s)
