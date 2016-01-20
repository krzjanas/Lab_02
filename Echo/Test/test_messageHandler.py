from unittest import TestCase
from Echo.MessageHandler import MessageHandler



class TestMessageHandler(TestCase):
    def test_encodeMessage(self):
        m = MessageHandler()
        type = "_text"
        msg = "Taki text  "
        self.assertEqual(m.encodeMessage(type, msg), "{TXT}Taki text{}".encode())
        type = "_nothing"
        self.assertEqual(m.encodeMessage(type, msg), "{NTH}Taki text{}".encode())
        type = "_SSSPPASDASDASDASD ASD_ASAS"
        self.assertEqual(m.encodeMessage(type, msg), "{NTH}Taki text{}".encode())
        type=""
        self.assertEqual(m.encodeMessage(type, msg), "{NTH}Taki text{}".encode())

    def test_decodeMessage(self):
        m = MessageHandler()
        data="{TXT}Taki text{}".encode()
        msg = "Taki text"
        self.assertEqual(m.decodeMessage(data), ("_text",msg) )
        data="{NTH}Taki text{} ".encode()
        self.assertEqual(m.decodeMessage(data), ("_nothing",msg) )
        data="{OOOasda}Taki text{}".encode()
        self.assertEqual(m.decodeMessage(data), ("_nothing","sda}Taki text") )
        data="{NTst".encode()
        self.assertEqual(m.decodeMessage(data), ("","") )


    def test_decodeType(self):
        m = MessageHandler()
        type="{NTH}"
        self.assertEqual(m.decodeType(type), "_nothing" )
        type="{TXT}"
        self.assertEqual(m.decodeType(type), "_text" )
        type="{SFAFDAFASFAFASF}"
        self.assertEqual(m.decodeType(type), "" )
        type=""
        self.assertEqual(m.decodeType(type), "" )

    def test_addPosition(self):
        m = MessageHandler()
        m.addPosition("[KEY]","value")
        self.assertEqual(m.decodeType("[KEY]"), "value" )