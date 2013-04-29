import functools
from PyQt4 import QtCore, QtGui
from PyQt4.Qt import *
from tool import Tool
from scribble_area import ScribbleArea
import xmlrpclib
sizeX = 1024
sizeY = 768

class MainWindow(QtGui.QMainWindow):
    def __init__(self,state):
        super(MainWindow, self).__init__()
        self.toolActs   = []
        self.scribbleArea = ScribbleArea(state)
        self.setCentralWidget(self.scribbleArea)
        self.createActions()
        self.createMenus()
        self.setWindowTitle("Scribble")
        self.resize(sizeX, sizeY)

    def closeEvent(self, event):
        event.accept()

    def penColor(self):
        newColor = QtGui.QColorDialog.getColor()
        if newColor.isValid():
            self.scribbleArea.setPenColor(newColor)

    def penWidth(self):
        newWidth, ok = QtGui.QInputDialog.getDouble(self, "Scribble",
                "Select pen width:", self.scribbleArea.penWidth(), 1, 50, 1)
        if ok:
            self.scribbleArea.setPenWidth(newWidth)

    def setTool(self,tool):
        self.scribbleArea.setTool(tool)

    def startSession(self):
         CS, ok = QtGui.QInputDialog.getText(self, 
                "Scribble",
                "Server Address",
                QLineEdit.Normal,
                "http://bratwurst.mit.edu:8000")
         sNumber = 0
         if ok:
             self.scribbleArea.state.cs = xmlrpclib.Server(str(CS))
             sNumber = self.scribbleArea.clerk.start()
             QMessageBox.about(self, "Scribble Area", "Your session number is: %s" % str(sNumber))


    def joinSession(self):
         CS, ok = QtGui.QInputDialog.getText(self, 
                "Scribble",
                "Server Address",
                QLineEdit.Normal,
                "http://bratwurst.mit.edu:8000")
         if not ok:
             return

         sNumber, ok = QtGui.QInputDialog.getInt(self, "Scribble",
                "Session Number:", 0, 0, 50, 1)
         if ok:
             self.scribbleArea.state.cs = xmlrpclib.Server(str(CS))
             self.scribbleArea.clerk.join(sNumber)
             QMessageBox.about(self, "Scribble Area", "Unable to join session: %s" % str(sNumber))

    def lockSession(self):
        CS, ok = QtGui.QInputDialog.getText(self, 
                "Scribble",
                "Server Address",
                QLineEdit.Normal,
                "http://bratwurst.mit.edu:8000")
        sNumber = self.scribbleArea.state.session

        if ok:
            self.scribbleArea.clerk.lock()
        

    def createActions(self):
        self.deleteAct = QtGui.QAction("Delete", self, shortcut="D",
                triggered=self.scribbleArea.delete)

        # list available tools
        for tool in ['Move','Pen']:
            action = QtGui.QAction(tool, self)
            action.triggered.connect(functools.partial(self.setTool,tool))
            self.toolActs.append(action)
            if tool == 'Move':
                action.setShortcut("M")
            if tool == 'Pen':
                action.setShortcut("P")


        self.exitAct = QtGui.QAction("E&xit", self, shortcut="Ctrl+Q",
                triggered=self.close)

        self.penColorAct = QtGui.QAction("&Pen Color...", self,
                triggered=self.penColor, shortcut="C")

        self.penWidthAct = QtGui.QAction("Pen &Width...", self,
                triggered=self.penWidth, shortcut="W")

        self.clearScreenAct = QtGui.QAction("&Clear Screen", self,
                shortcut="Ctrl+L", triggered=self.scribbleArea.clearImage)

        self.aboutAct = QtGui.QAction("&About", self, triggered=self.about)

        self.aboutQtAct = QtGui.QAction("About &Qt", self,
                triggered=QtGui.qApp.aboutQt)


        self.startSessionAct = QtGui.QAction("&Start Session...", self,
            triggered=self.startSession)

        self.joinSessionAct = QtGui.QAction("&Join Session...", self,
            triggered=self.joinSession)

        self.lockSessionAct = QtGui.QAction("&Lock Session...", self,
            triggered=self.lockSession)

    def createMenus(self):
        self.toolMenu = QtGui.QMenu("&Tool", self)
        for action in self.toolActs:
            self.toolMenu.addAction(action)

        fileMenu = QtGui.QMenu("&File", self)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAct)

        optionMenu = QtGui.QMenu("&Options", self)
        optionMenu.addAction(self.penColorAct)
        optionMenu.addAction(self.penWidthAct)
        optionMenu.addMenu(self.toolMenu)
        optionMenu.addSeparator()
        optionMenu.addAction(self.clearScreenAct)
        optionMenu.addAction(self.deleteAct)

        sessionMenu = QtGui.QMenu("&Session", self)
        sessionMenu.addAction(self.startSessionAct)
        sessionMenu.addAction(self.joinSessionAct)
        sessionMenu.addAction(self.lockSessionAct)

        helpMenu = QtGui.QMenu("&Help", self)
        helpMenu.addAction(self.aboutAct)
        helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(fileMenu)
        self.menuBar().addMenu(optionMenu)
        self.menuBar().addMenu(sessionMenu)
        self.menuBar().addMenu(helpMenu)
    
    def about(self):
        QtGui.QMessageBox.about(self, "About Scribble",
                "M.Gharbi & A.Tacchetti wrote this cool piece of soft ! Some of the backend comes from Coweb")
