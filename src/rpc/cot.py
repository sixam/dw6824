from dp.src.rpc.it import IT
import copy


class COT:

    depth = 0
    @staticmethod
    def transform(o, cd, contexts):
        """ In place for o
            Everything else should be a copy!"""

        COT.depth += 1
        depth = COT.depth
        print '\033[33mDEPTH:', COT.depth, '\033[0m'

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
            print 'c_ox in c_o:', COT.issublist(cox,co)
            COT.transform(ox, COT.contextsdiff(co, cox),contexts)
            IT.transform(o, ox)
            o.context.append(ox_id)
            print 'depth:',depth,'updated co:'

    @staticmethod
    def issublist(co, ds):
        for c in co:
            if c not in ds:
                return False
        return True

    @staticmethod
    def contextsdiff(ds, co):
        if not COT.issublist(co,ds):
            print '\033[33mERROR IN CONTEXT DIFF\033[0m'
            print ds
            print co
        dds = copy.copy(ds)
        for c in co:
            dds.remove(c)
        return dds


    @staticmethod
    def contextdiffinplace(ds, co):
        pass
