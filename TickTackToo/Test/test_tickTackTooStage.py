from unittest import TestCase

from TickTackToo.TickTackTooStage import TickTackTooStage

class TestTickTackTooStage(TestCase):
  def test_clear(self):
    tttS = TickTackTooStage()
    tttS.setStage("001021020")
    tttS.setX("C3")
    self.assertEqual(tttS.stage[11][23],'X')
    tttS.clear()
    self.assertEqual(tttS.stage[11][23],' ')

  def test_setWinLine(self):
    tttS = TickTackTooStage()
    tttS.setStage("222020202")
    self.assertEqual(tttS.stage[3][3],"|")
    tttS.setWinLine(1)
    self.assertEqual(tttS.stage[3][3],"#")

    tttS.setStage("001021021")
    self.assertEqual(tttS.stage[5][23],"-")
    tttS.setWinLine(6)
    self.assertEqual(tttS.stage[5][23],"#")

    tttS.setStage("201120122")
    self.assertEqual(tttS.stage[2][4]," ")
    tttS.setWinLine(7)
    self.assertEqual(tttS.stage[2][4],"#")

  def test_setX(self):
    tttS = TickTackTooStage()
    self.assertEqual(tttS.stage[6][14],' ')
    tttS.setX("B2")
    self.assertEqual(tttS.stage[6][14],'\\')
    self.assertEqual(tttS.stage[2][6],' ')
    tttS.setX("1A")
    self.assertEqual(tttS.stage[2][6],'\\')
    self.assertRaises(KeyError,tttS.setO,"aaaa")

  def test_setO(self):
    tttS = TickTackTooStage()
    self.assertEqual(tttS.stage[6][13],' ')
    tttS.setO("B2")
    self.assertEqual(tttS.stage[6][13],',')
    self.assertEqual(tttS.stage[2][5],' ')
    tttS.setO("1A")
    self.assertEqual(tttS.stage[2][5],',')
    self.assertRaises(KeyError,tttS.setO,"aaaa")

  def test_setStage(self):
    tttS = TickTackTooStage()

    codeStage = "201120122"
    for i in range(9):
      if codeStage[i] == '1':
        self.assertEqual(tttS.stage[2 + (i//3) * 4][6 + (i%3) * 8]," ")
      elif codeStage[i] == '2':
        self.assertEqual(tttS.stage[2 + (i//3) * 4][5 + (i%3) * 8]," ")

    tttS.setStage(codeStage)
    for i in range(9):
      if codeStage[i] == '1':
        self.assertEqual(tttS.stage[2 + (i//3) * 4][6 + (i%3) * 8],"\\")
      elif codeStage[i] == '2':
        self.assertEqual(tttS.stage[2 + (i//3) * 4][5 + (i%3) * 8],",")
