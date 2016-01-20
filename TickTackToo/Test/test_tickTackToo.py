from unittest import TestCase

from TickTackToo.TickTackToo import TickTackToo
import logging

class TestTickTackToo(TestCase):
  def test_clear(self):
    ttt = TickTackToo()
    ttt._setPol("001021020")
    ttt.setX("C3")
    self.assertEqual(ttt.cells,[[0,0,1],[0,2,1],[0,2,1]])
    self.assertEqual(ttt.last,'X')
    ttt.clear()
    self.assertEqual(ttt.cells,[[0,0,0],[0,0,0],[0,0,0]])
    self.assertEqual(ttt.last,'O')

  def test_setX(self):
    ttt = TickTackToo()
    ttt.setX("B2")
    self.assertEqual(ttt.cells[1][1],1)
    self.assertEqual(ttt.last,'X')

    self.assertRaises(MemoryError,ttt.setX,"C1")
    ttt.setO("1C")
    self.assertRaises(ZeroDivisionError,ttt.setX,"C1")
    self.assertRaises(KeyError,ttt.setX,"aaaa")

  def test_setO(self):
    ttt = TickTackToo()
    ttt.setX("B3")
    ttt.setO("B2")
    self.assertEqual(ttt.cells[1][1],2)
    self.assertEqual(ttt.last,'O')
    self.assertRaises(MemoryError,ttt.setO,"C1")
    ttt.setX("1C")
    self.assertRaises(ZeroDivisionError,ttt.setO,"C1")
    self.assertRaises(KeyError,ttt.setO,"aaaa")

  def test_checkWin(self):
    ttt = TickTackToo()
    self.assertEqual(ttt.checkWin(),(0,0))
    ttt.setX("1C")
    self.assertEqual(ttt.checkWin(),(0,0))

    ttt._setPol("222020202")
    self.assertEqual(ttt.checkWin(),(2,1))
    ttt._setPol("001021021")
    self.assertEqual(ttt.checkWin(),(1,6))
    ttt._setPol("001012121")
    self.assertEqual(ttt.checkWin(),(1,8))
    ttt._setPol("201120122")
    self.assertEqual(ttt.checkWin(),(2,7))

  def test_checkDraw(self):
    ttt = TickTackToo()
    self.assertFalse(ttt.checkDraw())
    ttt.setX("1C")
    self.assertFalse(ttt.checkDraw())

    ttt._setPol("222020202")
    self.assertFalse(ttt.checkDraw())
    ttt._setPol("001021021")
    self.assertFalse(ttt.checkDraw())
    ttt._setPol("001012121")
    self.assertFalse(ttt.checkDraw())
    ttt._setPol("221122122")
    self.assertFalse(ttt.checkDraw())
    ttt._setPol("222121212")
    self.assertFalse(ttt.checkDraw())

    ttt._setPol("121121212")
    self.assertTrue(ttt.checkDraw())

  def test_getStage(self):
    ttt = TickTackToo()
    self.assertEqual(ttt.getStage(),"000000000")
    ttt.setX("1C")
    self.assertEqual(ttt.getStage(),"001000000")
    ttt._setPol("222020202")
    self.assertEqual(ttt.getStage(),"222020202")
    ttt._setPol("001021021")
    self.assertEqual(ttt.getStage(),"001021021")
