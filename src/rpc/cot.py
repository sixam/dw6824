from dp.src.rpc.it import IT
import copy


class COT:
    @staticmethod
    def transform(o, cd, contexts):
        """ In place for o
            Everything else should be a copy!"""

        print 'TRANS:',o,cd

        if cd:
            print 'CD:',cd
            ox_id = cd.pop(0)
            co = o.context
            ox = contexts[ox_id]
            cx = ox.context
            print 'Co in Cx?',COT.issublist(co,cx)
            print 'C(ox):',cx
            cd =COT.contextsdiff(co, cx)
            COT.transform(ox, cd, contexts)
            IT.transform(o, ox)
            o.context.append(ox.request_id)

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
        dds = copy.copy(ds)
        for c in co:
            dds.remove(c)
        return dds
