from dp.src.rpc.it import IT
import copy


class COT:
    @staticmethod
    def transform(o, cd, contexts):
        """ In place for o
            Everything else should be a copy!"""

        print 'bbys with',o,cd,contexts
        while cd:
            ox = cd.pop(0)
            print "CD:",cd
            cx = contexts[ox.request_id]
            cd2 =COT.contextsdiff(co, cx)
            print 'recurse on', cd2
            COT.transform(ox, cd2)
            print 'pretransform'
            IT.transform(o, ox)
            print 'posttrans'
            o.context.append(ox.request_id)
        print 'bbys done'



    @staticmethod
    def issublist(co, ds):
        for c in co:
            if c not in ds:
                return False
        return True

    @staticmethod
    def contextsdiff(ds, co):
        print 'cdiff'
        dds = copy.copy(ds)
        for c in co:
            print 'try remove'
            dds.remove(c)
            print 'removed'
        return dds
