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
            print 'CD:',cd
            co = o.context

            for ox_id in cd:
                print 'ox:',ox_id
                ox = copy.copy(contexts[ox_id])
                cx = ox.context
                print 'C(o):', co
                print 'C(ox):', cx
                print 'Cx in Co?',COT.issublist(cx,co)
                if COT.issublist(cx,co):
                    break
                elif ox_id==len(cd) :
                    return False


            cd.remove(ox_id)

            cd =COT.contextsdiff(co, cx)
            print 'CD:',cd
            COT.transform(o, cd, contexts)
            IT.transform(o, ox)
            o.context.append(ox.request_id)
            return True

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
