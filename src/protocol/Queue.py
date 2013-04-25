from .HistoryBuffer import HistoryBuffer
from .OperationEngineException import OperationEngineException
from .factory import factory
from .Operation import Operation

class Queue(HistoryBuffer):
    """docstring for Queue"""

    def __init__(self, log):
        HistoryBuffer.__init__(self)
        self.log = log
        
    def enqueue(self,op):
        key = factory.createHistoryKey(op.siteId, op.seqId)
        self.ops[key] = op
        op.immutable = True
        self.size += 1

    def getProcessable(self, cv):
        """ Pop and returns the operations whose context vectors now allows
        processing """
        ops = self.getMorrisSortedOperations()
        self.log.red('get processable count:',self.getCount())

        for op in ops:
            skip = False
            for other in ops:
                comp = other.compareByMorris(op)
                if comp == -1:
                    self.log.orange('Queue:not ready, past to process')
                    skip = True
                    break
            if skip:
                self.log.orange('Queue:skipping')
                continue
            else:
               comp = op.contextVector.morrisCompare(cv)
               if comp < 0:
                   self.log.orange('Queue:process',op,'remaining:',self.getCount())
                   return self.remove(op)
               if comp == 0 :
                   self.log.orange('Queue:process',op,'remaining:',self.getCount())
                   return self.remove(op)

        self.log.orange('Queue:none ready, remaining:',self.size)
        return None

