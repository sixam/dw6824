class VT:
    def __init__(self):
        pass

    @staticmethod
    def cmp(a,b):
        # 0 if a == b
        # 1 if a > b (b is a NON-STRICT prefix of a)
        # -1 if a < b 
        # None if concurrent
        r = 0
        if a[0] > b[0]:
            r = 1
        elif a[0] < b[0]:
            r = -1
        
        for i in range(len(a)):
            if r == 0 and (a[i] > b[i]):
                r = 1
            if r == 0 and (a[i] < b[i]):
                r = -1
            if r == 1 and (a[i] < b[i]):
                return None
            if r == -1 and (a[i] > b[i]):
                return None
        return r
