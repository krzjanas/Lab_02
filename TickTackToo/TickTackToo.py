def getCoordinate(code):
    corR=('1','2','3')
    corC=('A','B','C')
    if not isinstance(code,str):
        raise KeyError
    if len(code) != 2:
        raise KeyError
    if corR.count(code[0]) and corC.count(code[1]):
        return (corR.index(code[0]),corC.index(code[1]))
    elif  corR.count(code[1]) and corC.count(code[0]):
        return (corR.index(code[1]),corC.index(code[0]))
    else:
        raise KeyError

class TickTackToo:

    def __init__(self):
        self.clear()

    def clear(self):
        self.cells = [[0,0,0],[0,0,0],[0,0,0]]
        self.last = 'O'

#throws:
    # MemoryError -> You use two indentical options in raw
    # KeyError -> Code have bad format (not like "A3") in every possible way
    # ZeroDivisionError -> You try put char in used place

    def setX(self,code):
        return self._setVal(code,'X')

    def setO(self,code):
        return self._setVal(code,'O')

    def checkWin(self):
        for ind in range(3):
            ch = self.cells[ind][0]
            if ch != 0 and self.cells[ind][1] == ch and self.cells[ind][2] == ch:
                return (ch,ind+1)

            ch = self.cells[0][ind]
            if ch != 0 and self.cells[1][ind] == ch and self.cells[2][ind] == ch:
                return (ch,ind+4)

        ch = self.cells[1][1]
        if ch != 0 :
            if self.cells[0][0] == ch and self.cells[2][2] == ch:
                return (ch,7)
            elif self.cells[0][2] == ch and self.cells[2][0] == ch:
                return (ch,8)

        return (0,0)

    def checkDraw(self):
        for i in range(3):
            for j in range(3):
                if not self.cells[i][j]:
                    return False
        if self.checkWin()[0]:
            return False
        else:
            return True

    def _setVal(self,code,charakter):
        if self.last == charakter:
            raise MemoryError
        cor = getCoordinate(code)
        self._set(cor[0],cor[1],charakter)
        self.last = charakter
        return self.checkWin()

    #For testing
    def _setPol(self,strPol):
        if not isinstance(strPol,str):
            raise TypeError
        if len(strPol) != 9:
            raise TypeError

        self.clear()
        for i in range(9):
            if strPol[i] == '1':
                self._set(i//3,i%3,'X')
            elif strPol[i] == '2':
                self._set(i//3,i%3,'O')

    def _set(self,raw,column,character):
        if(not isinstance(raw,int) or not isinstance(column,int)):
            raise TypeError

        if(raw > 2 or raw < 0 or column > 2 or column < 0 ):
            raise IndexError

        if(self.cells[raw][column] != 0):
            raise ZeroDivisionError

        if(character == 'X'):
            self.cells[raw][column] = 1
        elif(character == 'O'):
            self.cells[raw][column] = 2

    def getStage(self):
        codeStage = ''
        for i in range(3):
            for j in range(3):
                if self.cells[i][j] == 1:
                    codeStage = codeStage+'1'
                elif self.cells[i][j] == 2:
                    codeStage = codeStage+'2'
                else:
                    codeStage = codeStage+'0'
        return codeStage