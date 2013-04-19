from dp.src.rpc.it import IT
import copy
from dp.src.utils.log import Log


class COT:

    def __init__(self, log):
        self.log = log
        self.it = IT(log)

    def transform(self, o, cd, contexts):
        """ In place for o
            Everything else should be a copy!"""

        self.depth += 1
        depth = self.depth
        self.log.Print( '\033[33mDEPTH:', self.depth, '\033[0m')

        self.log.Print( '\n')
        self.log.Print( 'TRANS:',o,cd)
        self.log.Print( '\n')

        while cd:
            self.log.Print( 'recurse')
            ox_id = cd.pop(0)
            self.log.Print( 'cd:', cd)
            ox = contexts[ox_id]
            co = o.context
            self.log.Print( 'co',co)
            cox = ox.context
            self.log.Print( 'cox',cox)
            self.log.Print( 'c_ox in c_o:', self.issublist(cox,co))
            self.transform(ox, self.contextsdiff(co, cox),contexts)
            self.it.transform(o, ox)
            o.context.append(ox_id)
            self.log.Print( 'depth:',depth,'updated co:')

    def issublist(self, co, ds):
        for c in co:
            if c not in ds:
                return False
        return True

    def contextsdiff(self, ds, co):
        if not self.issublist(co,ds):
            self.log.Print( '\033[33mERROR IN CONTEXT DIFF\033[0m')
            self.log.Print( ds)
            self.log.Print( co)
        dds = copy.copy(ds)
        for c in co:
            dds.remove(c)
        return dds


