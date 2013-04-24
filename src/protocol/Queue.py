from .HistoryBuffer import HistoryBuffer
from .OperationEngineException import OperationEngineException
from .factory import factory
from .Operation import Operation

# cmp_to_key borrowed from
# http://code.activestate.com/recipes/576653-convert-a-
# cmp-function-to-a-key-function/
def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

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
       for op in ops:
           comp = op.contextVector.morrisCompare(cv)
           if comp < 0:
               return self.remove(op)
           if comp == 0 :
               return self.remove(op)

       return None





#        def peek(self):
#            ops = self.getContextSortedOperations()
#            return ops.pop().copy()
#
#        def pop(self):
#            ops = self.getContextSortedOperations()
#            op = ops.pop()
#            self.remove(op)
#            return op





        
