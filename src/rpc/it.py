from dp.src.rpc.commontypes import Request, Operation, OpType
class IT:
    def __init__(self, log):
        self.log = log

    def transform(self, o, ox):
        self._transform(o, ox)


    def _transform(self, ri,rj):

        oi = ri.op
        oj = rj.op

        print 'starting transform'

        if oi.type == OpType.ADD:
            self.transADD(ri,rj)
        #if oi.type == OpType.DEL:
            #self.transDEL(ri,rj)
        #if oi.type == OpType.MOVE:
            #self.transMOVE(ri,rj)

        print '\033[32m--transformed\033[0m',ri,rj,'\n'

    def transADD(self, ri,rj):

        print 'in trans ADD'
        oi = ri.op
        oj = rj.op

        PosI = oi.pos
        PosJ = oj.pos

        pi = ri.priority
        pj = rj.priority


        if oj.type == OpType.ADD:
            if PosI < PosJ:
                pass
            elif PosI > PosJ:
                oi.pos += 1
            else:
                if oi.stroke.id== oj.stroke.id:
                    oi.type = OpType.NoOp
                else:
                    if pi > pj:
                        oi.pos += 1
                    else:
                        pass

        if oj.type == OpType.DEL:
            if PosI < PosJ:
                pass
            else:
                oi.pos -= 1
        if oj.type == OpType.MOVE:
            if PosI < PosJ:
                pass
            elif PosI > PosJ:
                pass
            else: # PosI == PosJ
                if pi > pj:
                    oi.pos += 1 # This is a bit weird, just like the one in add/add
                else:
                    pass

        
