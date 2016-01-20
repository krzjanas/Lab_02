class MessageHandler():
    def __init__(self):
        self._createDictionary()

    def _createDictionary(self):
        self._BaseDictionary = {}
        self._BaseDictionary["{NTH}"]="_nothing"
        self._BaseDictionary["{NAM}"]="_name"
        self._BaseDictionary["{NRQ}"]="_name_request"
        self._BaseDictionary["{NAC}"]="_name_accepted"
        self._BaseDictionary["{TXT}"]="_text"
        self._BaseDictionary["{CHT}"]="_chat"
        self._BaseDictionary["{INF}"]="_info"
        self._BaseDictionary["{RQS}"]="_request"
        self._BaseDictionary["{ERR}"]="_error"
        self._BaseDictionary["{CRT}"]="_correct"
        self._BaseDictionary["{PRV}"]="_private"
        self._BaseDictionary["{NUM}"]="_number"
        self._BaseDictionary["{STP}"]="_stop"
        self._BaseDictionary["{STR}"]="_start"

        self._SecondDictionary = {}

    def addPosition(self, key, value):
        if len(key) != 5:
            return 0
        self._SecondDictionary[key]=value
        return 1

    def encodeMessage(self, type, text):
        text=text.rstrip()
        for key,val in self._BaseDictionary.items():
            if type == val:
                return (key+text+"{}").encode()
        for key,val in self._SecondDictionary.items():
            if type == val:
                return (key+text+"[]").encode()
        return ("{NTH}"+text+"{}").encode()

    def decodeMessage(self, msg):
        msg = msg.decode().rstrip()
        if len(msg) < 7:
            return "",""
        mType = msg[0:5]
        mText = msg[5:-2]

        for key,val in self._BaseDictionary.items():
            if mType == key:
                return val,mText
        for key,val in self._SecondDictionary.items():
            if mType == key:
                return val,mText
        return "_nothing",mText

    def decodeType(self,type):
        try:
            return self._BaseDictionary[type]
        except KeyError:
            try:
                return self._SecondDictionary[type]
            except KeyError:
                return ""

    def printAll(self):
        for it in self._BaseDictionary.items():
            print("Base - %s - %s"%it)
        for it in self._SecondDictionary.items():
            print("Secd - %s - %s"%it)