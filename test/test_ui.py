import sys
import time
import random

from .test_common import GenericTestCase

from dp.src.ui.main_window import MainWindow

from PyQt4 import QtCore, QtGui
from PyQt4.QtTest import QTest 

# scribble area size
sizeX = 1024
sizeY = 768

class TestUI(GenericTestCase):
    """ Test operations using UI interactions """

    def setUp(self):
        super(TestUI, self).setUp()
        self.app = QtGui.QApplication(sys.argv)
        self._addUIto(0)

    def _addUIto(self,peer_index):
        p = self.peers[peer_index]
        p.window = MainWindow(p.state)
        self.window = p.window
        self.area = p.window.scribbleArea
        p.window.show()
        p.window.raise_()
        p.state.window = p.window
        p.state.newStrokesSignal.connect(p.window.scribbleArea.strokesSignalHandler)

    def _drawRandomStroke(self):
        numpoints = random.randint(1,20) 
        QTest.mousePress(self.area,QtCore.Qt.LeftButton,pos=self._getPoint(),delay=0)
        for i in range(numpoints):
            QTest.mouseMove(self.area,self._getPoint(),delay=10)
        QTest.mouseRelease(self.area,QtCore.Qt.LeftButton,pos=self._getPoint(),delay=10)

    def _getPoint(self):
        return QtCore.QPoint(random.randint(1,sizeX-1),random.randint(1,sizeY-1))
        

    #def test_basic_ui_interactions(self):
        #""" UI - basic """
        #ck0 = self.clerks[0]
        #QTest.qWaitForWindowShown(self.area)

        #self._drawRandomStroke()

        #strokes = ck0.getStrokes()



