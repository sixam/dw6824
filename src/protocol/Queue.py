from .HistoryBuffer import HistoryBuffer
#from .HistoryBuffer import HistoryBuffer

class Queue(HistoryBuffer)
    """docstring for Queue"""
    def __init__(self):

   def enqueue(self,op):
       pass

   def getProcessable(self, cv):
       """ Pop and returns the operations whose context vectors now allows
       processing """
       ops = self.getMorrisSortedOperations()
       for op in ops:
           if op.contextVector.morrisCompare(cv) < 0:
               return self.remove(op)
       return None

    def getMorrisSortedOperations(self):
        ops = []
        for v in self.ops:
            ops.append(self.ops[v])
         return sorted(ops, key=cmp_to_key(lambda x, y: x.compareByMorris(y)))




#        def peek(self):
#            ops = self.getContextSortedOperations()
#            return ops.pop().copy()
#
#        def pop(self):
#            ops = self.getContextSortedOperations()
#            op = ops.pop()
#            self.remove(op)
#            return op





        
