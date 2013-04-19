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
        print 'TRANS:',o
        print '\n'

        # Sort cd by context dependencies 'hb.getOpsDifference'
        # Go through all ops in cd

        # do not transform original op
        #o = copy.copy(o)

        # transformed operation

        while cd:
            print 'cd:', cd
            print 'all contexts:'
            for c in cd:
                print contexts[c]

            # previously transformed op
            ox_id = cd.pop(0)
            ox = contexts[ox_id]
            print 'ox_id:', ox_id

            # At this point we should have some caching to avoid going through
            # the recursion every time

            # If not in cache, transform ox recursively

            co = o.context
            cox = ox.context
            print 'co',co
            print 'cox',cox

            # new context difference
            xcd = COT.contextsdiff(co, cox)

            print 'c_ox in c_o:', COT.issublist(cox,co)

            print 'recurse'
            COT.transform(ox, xcd ,contexts)

            print 'transformed op:',ox

            IT.transform(o, ox)
            o.context.append(ox_id)
            print 'depth:',depth,'updated co:', o

    @staticmethod
    def sortContextDifference(cd,contexts):
        pass


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

