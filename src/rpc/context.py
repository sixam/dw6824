from dp.src.rpc.cot import COT
class Context:
    def __init__(self, c = []):
        self.c
    def __cmp__(self, other):
        if len(self) > len(other) and COT.issublist(other.c, self.c):
            return 1
        elif len(self) < len(other) and COT.issublist(self.c, other.c):
            return -1
        else:
            return 0
