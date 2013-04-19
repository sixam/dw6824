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
        print '\033[33mDEPTH:', self.depth, '\033[0m'

        print '\n'
        print 'TRANS:',o,cd
        print '\n'

        while cd:
            print 'recurse'
            ox_id = cd.pop(0)
            print 'cd:', cd
            ox = contexts[ox_id]
            co = o.context
            print 'co',co
            cox = ox.context
            print 'cox',cox
            print 'c_ox in c_o:', self.issublist(cox,co)
            self.transform(ox, self.contextsdiff(co, cox),contexts)
            self.it.transform(o, ox)
            o.context.append(ox_id)
            print 'depth:',depth,'updated co:'

    def issublist(self, co, ds):
        for c in co:
            if c not in ds:
                return False
        return True

    def contextsdiff(self, ds, co):
        if not self.issublist(co,ds):
            print '\033[33mERROR IN CONTEXT DIFF\033[0m'
            print ds
            print co
        dds = copy.copy(ds)
        for c in co:
            dds.remove(c)
        return dds


