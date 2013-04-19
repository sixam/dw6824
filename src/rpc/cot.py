from dp.src.rpc.it import IT


class COT:
    @staticmethod
    def transform(o, cd, contexts):
        """ In place for o
            Everything else should be a copy!"""
        while cd:
            ox = cd.pop(0)
            cx = contexts[ox.request_id]
            COT.transform(ox, COT.contextsdiff(co, cx))
            IT.transform(o, ox)
            o.context.append(ox.request_id)



    def issublist(co, ds):
        for c in co:
            if c not in ds:
                return False
        return True

    def contextsdiff(ds, co):
        dds = copy.copy(ds)
        for c in co:
            dds.remove(c)
        return dds
