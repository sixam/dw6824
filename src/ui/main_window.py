import functools
from PyQt4 import QtCore, QtGui
from tool import Tool
from scribble_area import ScribbleArea

class MainWindow(QtGui.QMainWindow):
    def __init__(self,state):
        super(MainWindow, self).__init__()

        self.toolActs   = []

        self.scribbleArea = ScribbleArea(state)
        self.setCentralWidget(self.scribbleArea)

        self.createActions()
        self.createMenus()

        self.setWindowTitle("Scribble")
        self.resize(1024, 768)

    def closeEvent(self, event):
        event.accept()

    def penColor(self):
        newColor = QtGui.QColorDialog.getColor(self.scribbleArea.penColor())
        if newColor.isValid():
            self.scribbleArea.setPenColor(newColor)

    def penWidth(self):
        newWidth, ok = QtGui.QInputDialog.getDouble(self, "Scribble",
                "Select pen width:", self.scribbleArea.penWidth(), 1, 50, 1)
        if ok:
            self.scribbleArea.setPenWidth(newWidth)

    def setTool(self,tool):
        self.scribbleArea.setTool(tool)

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

        helpMenu = QtGui.QMenu("&Help", self)
        helpMenu.addAction(self.aboutAct)
        helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(fileMenu)
        self.menuBar().addMenu(optionMenu)
        self.menuBar().addMenu(helpMenu)
    
    def about(self):
        QtGui.QMessageBox.about(self, "About Scribble",
                "WIP app")
