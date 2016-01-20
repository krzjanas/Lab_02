from Echo.MessageHandler import MessageHandler

class TTT_MessageHandler(MessageHandler):
    def __init__(self):
        super().__init__()
        self._SecondDictionary["[WIN]"] = "win"
        self._SecondDictionary["[DRW]"] = "draw"
        self._SecondDictionary["[M_X]"] = "move_X"
        self._SecondDictionary["[M_O]"] = "move_O"
        self._SecondDictionary["[MOV]"] = "move"
        self._SecondDictionary["[WRG]"] = "wrong"
        self._SecondDictionary["[CHR]"] = "character"
        self._SecondDictionary["[STG]"] = "stage"



