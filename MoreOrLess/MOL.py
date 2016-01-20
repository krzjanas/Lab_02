import random

class MOL:
    def __init__(self, minV, maxV):
        self.minV = minV
        self.maxV = maxV
        self.curr = random.randint(minV,maxV)

    def guess(self,val):
        if val == self.curr:
            return 0
        elif val > self.curr:
            return 1
        else:
            return -1