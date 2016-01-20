from unittest import TestCase

import TickTackToo
import logging

class TestTickTackToo(TestCase):
  def test_clear(self):
    ttt = TickTackToo.TickTackToo()
    ttt._setPol("001021020")
    ttt.setX("C3")
    self.assertEqual(ttt.cells,[[0,0,1],[0,2,1],[0,2,1]])
    self.assertEqual(ttt.last,'X')
    ttt.clear()
    self.assertEqual(ttt.cells,[[0,0,0],[0,0,0],[0,0,0]])
    self.assertEqual(ttt.last,None)

  def test_setX(self):
    ttt = TickTackToo.TickTackToo()
    ttt.setX("B2")
    self.assertEqual(ttt.cells[1][1],1)
    self.assertEqual(ttt.last,'X')

    self.assertRaises(MemoryError,ttt.setX,"C1")
    ttt.setO("1C")
    self.assertRaises(ZeroDivisionError,ttt.setX,"C1")
    self.assertRaises(KeyError,ttt.setX,"aaaa")

  def test_setO(self):
    ttt = TickTackToo.TickTackToo()
    ttt.setO("B2")
    self.assertEqual(ttt.cells[1][1],2)
    self.assertEqual(ttt.last,'O')

    self.assertRaises(MemoryError,ttt.setO,"C1")
    ttt.setX("1C")
    self.assertRaises(ZeroDivisionError,ttt.setO,"C1")
    self.assertRaises(KeyError,ttt.setO,"aaaa")

  def test_checkWin(self):
    ttt = TickTackToo.TickTackToo()
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
