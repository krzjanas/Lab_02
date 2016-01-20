from TickTackToo.TickTackToo import getCoordinate

class TickTackTooStage:

    def __init__(self):
        self.clear()

    def clear(self):
        self.stage = []
        self.stage.append("R,\\,C,|, , , ,A, , , ,|, , , ,B, , , ,|, , , ,C, , , ,|, ".split(','))
        self.stage.append("-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-, ".split(','))
        self.stage.append(" , , ,|, , , , , , , ,|, , , , , , , ,|, , , , , , , ,|, ".split(','))
        self.stage.append(" ,1, ,|, , , , , , , ,|, , , , , , , ,|, , , , , , , ,|, ".split(','))
        self.stage.append(" , , ,|, , , , , , , ,|, , , , , , , ,|, , , , , , , ,|, ".split(','))
        self.stage.append("-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-, ".split(','))
        self.stage.append(" , , ,|, , , , , , , ,|, , , , , , , ,|, , , , , , , ,|, ".split(','))
        self.stage.append(" ,2, ,|, , , , , , , ,|, , , , , , , ,|, , , , , , , ,|, ".split(','))
        self.stage.append(" , , ,|, , , , , , , ,|, , , , , , , ,|, , , , , , , ,|, ".split(','))
        self.stage.append("-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-, ".split(','))
        self.stage.append(" , , ,|, , , , , , , ,|, , , , , , , ,|, , , , , , , ,|, ".split(','))
        self.stage.append(" ,3, ,|, , , , , , , ,|, , , , , , , ,|, , , , , , , ,|, ".split(','))
        self.stage.append(" , , ,|, , , , , , , ,|, , , , , , , ,|, , , , , , , ,|, ".split(','))
        self.stage.append("-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-,-, ".split(','))

    def printStage(self,lineBefore=5,lineAfter=5,spacesLeft=20):
        for i in range(lineBefore):
            print()

        for raw in self.stage:
            for i in range(spacesLeft):
                print(end=' ')

            for col in raw:
                print(col,end='')
            print()

        for i in range(lineAfter):
            print()

    def setWinLine(self,nr):
        if not isinstance(nr,int):
            raise TypeError
        if 0 < nr < 4:
            for i in range(27):
                self.stage[3+(nr-1)*4][i+2] = '#'
        if 3 < nr < 7:
            for i in range(13):
                self.stage[1+i][7+(nr-4)*8] = '#'
        if nr == 7:
            for i in range(12):
                self.stage[2+i][4+2*i] = '#'
            for i in range(13):
                self.stage[1+i][3+2*i] = '#'
        if nr == 8:
            for i in range(12):
                self.stage[2+i][26-2*i] = '#'
            for i in range(13):
                self.stage[1+i][27-2*i] = '#'

    def setX(self,code):
        cor = getCoordinate(code)
        self._setV(cor[0],cor[1],'X')


    def setO(self,code):
        cor = getCoordinate(code)
        self._setV(cor[0],cor[1],'O')


    def setStage(self,codeStage):
        print("<%s>"%codeStage)
        if not isinstance(codeStage,str):
            raise TypeError
        if len(codeStage) != 9:
            raise TypeError

        self.clear()
        for i in range(9):
            if codeStage[i] == '1':
                self._setV(i//3,i%3,'X')
            elif codeStage[i] == '2':
                self._setV(i//3,i%3,'O')

    def _setV(self,raw,col,charakter):
        if(not isinstance(raw,int) or not isinstance(col,int)):
            raise TypeError

        if(raw > 2 or raw < 0 or col > 2 or col < 0 ):
            raise IndexError

        plRaw = 3 + raw * 4
        plCol = 7 + col * 8

        if charakter == 'X':
            self.stage[plRaw][plCol] = 'X'
            self.stage[plRaw-1][plCol-1] = '\\'
            self.stage[plRaw-1][plCol+1] = '/'
            self.stage[plRaw+1][plCol-1] = '/'
            self.stage[plRaw+1][plCol+1] = '\\'
        elif charakter == 'O':
            self.stage[plRaw-1][plCol-2] = ','
            self.stage[plRaw-1][plCol-1] = '-'
            self.stage[plRaw-1][plCol-0] = '-'
            self.stage[plRaw-1][plCol+1] = '-'
            self.stage[plRaw-1][plCol+2] = ','
            self.stage[plRaw+1][plCol-2] = '\''
            self.stage[plRaw+1][plCol+2] = '\''
            self.stage[plRaw][plCol-2] = '|'
            self.stage[plRaw][plCol+2] = '|'
            self.stage[plRaw+1][plCol-1] = '-'
            self.stage[plRaw+1][plCol-0] = '-'
            self.stage[plRaw+1][plCol+1] = '-'