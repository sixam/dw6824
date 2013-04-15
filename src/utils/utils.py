import ConfigParser
import random
import os
import rpc.common

class Utils:
    def __init__(self):
        pass
    @staticmethod
    def getConfig():
        config = ConfigParser.RawConfigParser()
        for loc in os.listdir("%s/conf" % os.environ.get('DW_BASE')):
            config.read("%s/%s/%s" % (os.environ.get('DW_BASE'),'conf',loc))
        return config
    @staticmethod
    def getLogPath(logtype,local_id):
        config = utils.getConfig()
        return "%s/%s" % (os.environ.get('DW_BASE'), config.get('log', logtype) % (local_id) )
    @staticmethod
    def generateID():
        return "{0}".format(random.getrandbits(128))

    @staticmethod
    def movToDelAdd(rq):
        print 'Move to del add'
        rqs = []
        opd = rpc.common.Operation(type=rpc.common.OpType.DEL, stroke_id = rq.op.stroke_id, pos = rq.op.pos,
                stroke = rq.op.stroke)
        rqd = rpc.common.Request(sender = rq.sender, 
                vt = rq.vt[:], op=opd, priority = rq.priority, request_id = rq.request_id);
        rqs.append(rqd)

        nvt = rq.vt[:];
        nvt[rq.sender] += 1 # make the add happen strictly after the del
        #nstroke = copy.copy(rq.op.stroke);
        #nstroke.offsetPosBy(offset)

        opa = rpc.common.Operation(type=rpc.common.OpType.ADD, stroke_id = rq.op.stroke_id, pos = rq.op.pos,
                stroke = rq.op.stroke)

        rqa = rpc.common.Request(sender = rq.sender, 
                vt = nvt, op = opa, priority = rq.priority, request_id = rq.request_id);
        rqs.append(rqa)
        return rqs

