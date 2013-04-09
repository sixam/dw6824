from PyQt4 import QtCore, QtGui
from rpc.client import Client
from stroke import Stroke
from tool import Tool

class ScribbleArea(QtGui.QWidget):
    def __init__(self, client,parent=None):
        super(ScribbleArea, self).__init__(parent)

        self.setAttribute(QtCore.Qt.WA_StaticContents)

        # Current State 
        self.current_tool = Tool.PEN

        # Drawing state
        self.controlPoints = [];
        self.scribbling = False
        self.myPenWidth = 10.0
        self.myPenColor = QtGui.QColor(0,0,255)

        # Select and move state
        self.select_rect = QtCore.QRectF
        self.selected = -1
        self.moving = False

        self.image = QtGui.QImage()

        self.client = client

        # Drawing content
        self.strokes = [];

    def setPenColor(self, newColor):
        self.myPenColor = newColor

    def setPenWidth(self, newWidth):
        self.myPenWidth = newWidth

    def clearImage(self):
        self.image.fill(QtGui.QColor(255, 255, 255))
        self.update()

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self.current_tool == Tool.MOVE:
                self.move_pos = event.posF()
                x = event.posF().x()
                y = event.posF().y()
                sel_rect = QtCore.QRectF(QtCore.QPointF(x-10,y-10),QtCore.QPointF(x+10,y+10))
                self.selected = -1 #if the click is outside, we deselect
                for s_id,stroke in enumerate(self.strokes): # check selection
                    if stroke.toPainterPath().intersects(sel_rect):
                        self.selected = s_id
                        break
                pass
            elif self.current_tool == Tool.PEN:
                self.controlPoints = []
                self.controlPoints.append([event.posF().x(),event.posF().y()]);
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
                    for i,pt in enumerate(stroke.path):
                        pt[0] = pt[0] + offset.x()
                        pt[1] = pt[1] + offset.y()
                    self.draw()
            elif self.current_tool == Tool.PEN and self.scribbling:
                self.path.lineTo(event.posF());
                self.controlPoints.append([event.posF().x(),event.posF().y()]);
                self.drawLineTo()
                self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self.current_tool == Tool.MOVE:
                if self.moving and self.selected >= 0: 
                    self.moving = False
                else :
                    pass

            elif self.current_tool == Tool.PEN and self.scribbling:
                stroke = Stroke(self.controlPoints,self.myPenWidth,list(self.myPenColor.getRgb()))
                self.client.addStroke(stroke)
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

    def resizeImage(self, image, newSize):
        if image.size() == newSize:
            return

        newImage = QtGui.QImage(newSize, QtGui.QImage.Format_RGB32)
        newImage.fill(QtGui.qRgb(255, 255, 255))
        painter = QtGui.QPainter(newImage)
        painter.drawImage(QtCore.QPoint(0, 0), image)
        self.image = newImage

    def penColor(self):
        return self.myPenColor

    def penWidth(self):
        return self.myPenWidth

    def draw(self):
        self.image.fill(QtGui.QColor(255, 255, 255))
        painter = QtGui.QPainter(self.image)
        for stroke in self.strokes:
            painter.setPen(QtGui.QPen(QtGui.QColor(*stroke.color), stroke.width,
                QtCore.Qt.SolidLine, QtCore.Qt.RoundCap, QtCore.Qt.RoundJoin))
            path = stroke.toPainterPath()
            painter.drawPath(path);
        self.update()

    def delete(self):
        if self.selected >= 0:
            print 'deleted'
            del(self.strokes[self.selected])
            self.draw()


