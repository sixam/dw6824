from dp.src.rpc.it import IT
import copy


class COT:
    @staticmethod
    def transform(o, cd, contexts):
        """ In place for o
            Everything else should be a copy!"""

        while cd:
            print cd
            ox_id = cd.pop(0)
            ox = contexts[ox.request_id]
            cx = ox.context
            cd2 =COT.contextsdiff(co, cx)
            COT.transform(ox, cd2, contexts)
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
        dds = copy.copy(ds)
        for c in co:
            dds.remove(c)
        return dds
