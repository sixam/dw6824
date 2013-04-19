from dp.src.rpc.it import IT
import copy


class COT:
    @staticmethod
    def transform(o, cd, contexts):
        """ In place for o
            Everything else should be a copy!"""

        print '\n'
        print 'TRANS:',o,cd
        print '\n'

        while cd:
            print 'recurse'
            ox_id = cd.pop(0)
            ox = contexts[ox_id]
            co = o.context
            cox = ox.context
            COT.transform(ox, COT.contextsdiff(co, cox))
            IT.transform(o, ox)
            o.context.append(ox.request_id)

    @staticmethod
    def issublist(co, ds):
        for c in co:
            print 'hello'
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
