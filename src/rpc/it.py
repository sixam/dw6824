class IT:
    @staticmethod
    def transform(o, ox):
        IT._transform(o, ox)


    @staticmethod
    def _transform(ri,rj):

        print 'starting transform'

        if oi.type == OpType.ADD:
            transADD(ri,rj)
        if oi.type == OpType.DEL:
            transDEL(ri,rj)
        if oi.type == OpType.MOVE:
            transMOVE(ri,rj)

        print '\033[32m--transformed\033[0m',ri,rj,'\n'

    def transADD(ri,rj):

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

        
    def transDEL( ri, rj):
        print 'in trans DEL'
        oi = ri.op
        oj = rj.op

        PosI = oi.pos
        PosJ = oj.pos

        pi = ri.priority
        pj = rj.priority

        if oj.type == OpType.ADD:
            if PosI < PosJ:
                pass
            else:
                oi.pos += 1

        if oj.type == OpType.DEL:
            if PosI < PosJ:
                pass
            elif PosI > PosJ:
                oi.pos -= 1
            else:
                oi.type = OpType.NoOp

        if oj.type == OpType.MOVE:
            if PosI < PosJ:
                pass
            elif PosI > PosJ:
                pass
            else: # PosI == PosJ
                if pi < pj:
                    oi.type = OpType.NoOp
                else:
                    pass

    def transMOVE(ri,rj):
        print 'in trans MOVE'
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
                if pi > pj:
                    oi.pos += 1 # This is strange
                else:
                    pass

        if oj.type == OpType.DEL:
            if PosI < PosJ:
                pass
            elif PosI > PosJ:
                oi.pos -= 1
            else: # PosI == PosJ
                if pi < pj:
                    oi.type = OpType.NoOp
                else:
                    pass

        if oj.type == OpType.MOVE:
            if PosI < PosJ:
                pass
            elif PosI > PosJ:
                pass
            else: # PosI == PosJ
                if pi < pj:
                    oi.type = OpType.NoOp
                else:
                    pass

