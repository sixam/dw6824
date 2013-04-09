import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)
import sys
import math
import functools
from PyQt4 import QtCore, QtGui

class Tool:
    """Set of authorized tools"""
    MOVE = 'Move'
    PEN = 'Pen'

class Stroke:
    """Basic Stroke"""
    def __init__(self, path, width, color):
        self.path  = path
        self.width = width
        self.color = color

    def __str__(self):
        return "Stroke: {0} - width: {1}, color: {2}".format(self.path, self.width, self.color)


class ScribbleArea(QtGui.QWidget):
    def __init__(self, parent=None):
        super(ScribbleArea, self).__init__(parent)

        self.setAttribute(QtCore.Qt.WA_StaticContents)

        # Current State 
        self.modified = False
        self.current_tool = Tool.PEN
        self.myPenWidth = 10
        self.myPenColor = QtCore.Qt.blue

        self.controlPoints = [];
        self.scribbling = False
        self.select_rect = QtCore.QRectF
        self.selected = -1
        self.moving = False

        self.image = QtGui.QImage()

        self.LinePath = QtGui.QPainterPath()

        # Drawing content
        self.strokes = [];

    def openImage(self, fileName):
        loadedImage = QtGui.QImage()
        if not loadedImage.load(fileName):
            return False

        newSize = loadedImage.size().expandedTo(self.size())
        self.resizeImage(loadedImage, newSize)
        self.image = loadedImage
        self.modified = False
        self.update()
        return True

    def saveImage(self, fileName, fileFormat):
        visibleImage = self.image
        self.resizeImage(visibleImage, self.size())

        if visibleImage.save(fileName, fileFormat):
            self.modified = False
            return True
        else:
            return False

    def setPenColor(self, newColor):
        self.myPenColor = newColor

    def setPenWidth(self, newWidth):
        self.myPenWidth = newWidth

    def clearImage(self):
        self.image.fill(QtGui.qRgb(255, 255, 255))
        self.modified = True
        self.update()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self.current_tool == Tool.MOVE:
                self.move_pos = event.posF()
                pass
            elif self.current_tool == Tool.PEN:
                self.controlPoints = []
                self.controlPoints.append(event.posF());
                self.path = QtGui.QPainterPath(event.posF());
                self.scribbling = True
            else:
                pass

    def mouseMoveEvent(self, event):
        if (event.buttons() & QtCore.Qt.LeftButton):
            if self.current_tool == Tool.MOVE:
                if self.selected != -1:
                    self.moving = True
                if self.moving and self.selected >= 0: 
                    offset = event.posF() - self.move_pos 
                    self.move_pos = event.posF()
                    stroke = self.strokes[self.selected]
                    stroke.path.translate(offset)
                    self.draw()
            elif self.current_tool == Tool.PEN and self.scribbling:
                self.controlPoints.append(event.posF());
                self.path.lineTo(event.posF());
                self.drawLineTo()
                self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self.current_tool == Tool.MOVE:
                if self.moving and self.selected >= 0: 
                    #offset = event.posF() - self.move_origin 
                    #stroke = self.strokes[self.selected]
                    #stroke.path.translate(offset)
                    self.moving = False
                else :
                    x = event.posF().x()
                    y = event.posF().y()
                    sel_rect = QtCore.QRectF(QtCore.QPointF(x-10,y-10),QtCore.QPointF(x+10,y+10))
                    self.selected = -1 #if the click is outside, we deselect
                    for s_id,stroke in enumerate(self.strokes): # check selection
                        if stroke.path.intersects(sel_rect):
                            self.selected = s_id
                            print 'selected :', s_id, stroke
                            break

            elif self.current_tool == Tool.PEN and self.scribbling:
                stroke = Stroke(self.path,self.myPenWidth,self.myPenColor)
                self.strokes.append(stroke)
                self.update()
                self.scribbling = False

            self.draw()

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.drawImage(event.rect(), self.image)

    def resizeEvent(self, event):
        if self.width() > self.image.width() or self.height() > self.image.height():
            newWidth = max(self.width(), self.image.width())
            newHeight = max(self.height(), self.image.height())
            self.resizeImage(self.image, QtCore.QSize(newWidth, newHeight))
            self.update()

        super(ScribbleArea, self).resizeEvent(event)

    def drawLineTo(self):
        painter = QtGui.QPainter(self.image)
        painter.setPen(QtGui.QPen(self.myPenColor, self.myPenWidth,
                QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
        painter.drawPath(self.path);
        self.modified = True

    def resizeImage(self, image, newSize):
        if image.size() == newSize:
            return

        newImage = QtGui.QImage(newSize, QtGui.QImage.Format_RGB32)
        newImage.fill(QtGui.qRgb(255, 255, 255))
        painter = QtGui.QPainter(newImage)
        painter.drawImage(QtCore.QPoint(0, 0), image)
        self.image = newImage

    def isModified(self):
        return self.modified

    def penColor(self):
        return self.myPenColor

    def penWidth(self):
        return self.myPenWidth

    def draw(self):
        #self.clearImage()
        self.image.fill(QtGui.qRgb(255, 255, 255))
        painter = QtGui.QPainter(self.image)
        for stroke in self.strokes:
            painter.setPen(QtGui.QPen(stroke.color, stroke.width,
                QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
            painter.drawPath(stroke.path);
        print 'redrawn'
        self.modified = True
        self.update()


class MainWindow(QtGui.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.saveAsActs = []
        self.toolActs   = []

        self.scribbleArea = ScribbleArea()
        self.setCentralWidget(self.scribbleArea)

        self.createActions()
        self.createMenus()

        self.setWindowTitle("Scribble")
        self.resize(1024, 768)

    def closeEvent(self, event):
        event.accept()
        #if self.maybeSave():
            #event.accept()
        #else:
            #event.ignore()

    def open(self):
        if self.maybeSave():
            fileName = QtGui.QFileDialog.getOpenFileName(self, "Open File",
                    QtCore.QDir.currentPath())
            if fileName:
                self.scribbleArea.openImage(fileName)

    def save(self):
        action = self.sender()
        fileFormat = action.data()
        self.saveFile(fileFormat)

    def penColor(self):
        newColor = QtGui.QColorDialog.getColor(self.scribbleArea.penColor())
        if newColor.isValid():
            self.scribbleArea.setPenColor(newColor)

    def penWidth(self):
        newWidth, ok = QtGui.QInputDialog.getInteger(self, "Scribble",
                "Select pen width:", self.scribbleArea.penWidth(), 1, 50, 1)
        if ok:
            self.scribbleArea.setPenWidth(newWidth)

    def setTool(self,tool):
        self.scribbleArea.current_tool = tool
        print '\033[32mTool :',tool,'\033[0m'

    def createActions(self):
        self.openAct = QtGui.QAction("&Open...", self, shortcut="Ctrl+O",
                triggered=self.open)

        for format in QtGui.QImageWriter.supportedImageFormats():
            format = str(format)

            text = format.upper() + "..."

            action = QtGui.QAction(text, self, triggered=self.save)
            action.setData(format)
            self.saveAsActs.append(action)

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
        self.saveAsMenu = QtGui.QMenu("&Save As", self)
        for action in self.saveAsActs:
            self.saveAsMenu.addAction(action)

        self.toolMenu = QtGui.QMenu("&Tool", self)
        for action in self.toolActs:
            self.toolMenu.addAction(action)

        fileMenu = QtGui.QMenu("&File", self)
        fileMenu.addAction(self.openAct)
        fileMenu.addMenu(self.saveAsMenu)
        fileMenu.addSeparator()
        fileMenu.addAction(self.exitAct)

        optionMenu = QtGui.QMenu("&Options", self)
        optionMenu.addAction(self.penColorAct)
        optionMenu.addAction(self.penWidthAct)
        optionMenu.addMenu(self.toolMenu)
        optionMenu.addSeparator()
        optionMenu.addAction(self.clearScreenAct)

        helpMenu = QtGui.QMenu("&Help", self)
        helpMenu.addAction(self.aboutAct)
        helpMenu.addAction(self.aboutQtAct)

        self.menuBar().addMenu(fileMenu)
        self.menuBar().addMenu(optionMenu)
        self.menuBar().addMenu(helpMenu)

    def maybeSave(self):
        if self.scribbleArea.isModified():
            ret = QtGui.QMessageBox.warning(self, "Scribble",
                        "The image has been modified.\n"
                        "Do you want to save your changes?",
                        QtGui.QMessageBox.Save | QtGui.QMessageBox.Discard |
                        QtGui.QMessageBox.Cancel)
            if ret == QtGui.QMessageBox.Save:
                return self.saveFile('png')
            elif ret == QtGui.QMessageBox.Cancel:
                return False

        return True

    def saveFile(self, fileFormat):
        initialPath = QtCore.QDir.currentPath() + '/untitled.' + fileFormat

        fileName = QtGui.QFileDialog.getSaveFileName(self, "Save As",
                initialPath,
                "%s Files (*.%s);;All Files (*)" % (fileFormat.upper(), fileFormat))
        if fileName:
            return self.scribbleArea.saveImage(fileName, fileFormat)

        return False
    
    def about(self):
        QtGui.QMessageBox.about(self, "About Scribble",
                "<p>The <b>Scribble</b> example shows how to use "
                "QMainWindow as the base widget for an application, and how "
                "to reimplement some of QWidget's event handlers to receive "
                "the events generated for the application's widgets:</p>"
                "<p> We reimplement the mouse event handlers to facilitate "
                "drawing, the paint event handler to update the application "
                "and the resize event handler to optimize the application's "
                "appearance. In addition we reimplement the close event "
                "handler to intercept the close events before terminating "
                "the application.</p>"
                "<p> The example also demonstrates how to use QPainter to "
                "draw an image in real time, as well as to repaint "
                "widgets.</p>")
