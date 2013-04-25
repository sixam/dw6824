import sys
import time
import random

from .test_common import GenericTestCase

from dp.src.ui.main_window import MainWindow

from PyQt4 import QtCore, QtGui
from PyQt4.QtTest import QTest 

class TestUI(GenericTestCase):
    """ Test operations using UI interactions """

    def setUp(self):
        super(TestUI, self).setUp()
        self.app = QtGui.QApplication(sys.argv)
        self.addUIto(0)

    def addUIto(self,peer_index):
        p = self.peers[peer_index]
        p.window = MainWindow(p.state)
        self.area = p.window.scribbleArea
        p.window.show()
        p.window.raise_()
        p.state.window = p.window
        p.state.newStrokesSignal.connect(p.window.scribbleArea.strokesSignalHandler)

    def drawRandomStroke()

    def test_basic_ui_interactions(self):
        """ UI - basic """
        ck0 = self.clerks[0]

        QTest.qWaitForWindowShown(self.area)
        #QTest.mouseClick(self.area,QtCore.Qt.LeftButton,pos=QtCore.QPoint(10,20))
        QTest.mousePress(self.area,QtCore.Qt.LeftButton,pos=QtCore.QPoint(10,20))
        QTest.mouseMove(self.area,pos=QtCore.QPoint(30,45))
        QTest.mouseRelease(self.area,QtCore.Qt.LeftButton,pos=QtCore.QPoint(30,45))

        strokes = ck0.getStrokes()
        print self.peers[0].window.scribbleArea.state
        time.sleep(1)


