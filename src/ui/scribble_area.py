from PyQt4 import QtCore, QtGui
from rpc.clerk import Clerk
from stroke import Stroke
from tool import Tool

class ScribbleArea(QtGui.QWidget):
    """ Main Area for drawing
        =====================

        Capture mouse events and update the state accordingly.
        All the broadcasting is done by the clerk object

    """
    def __init__(self, state, parent=None):
        super(ScribbleArea, self).__init__(parent)

        self.setAttribute(QtCore.Qt.WA_StaticContents)

        # Current mode 
        self.current_tool = Tool.PEN

        # Drawing state
        self.controlPoints = [];
        self.scribbling = False
        self.myPenWidth = 10.0
        self.myPenColor = QtGui.QColor(0,0,255)

        # Select and move state variables
        self.select_rect = QtCore.QRectF
        self.selected = -1
        self.moving = False

        # Drawing canvas
        self.image = QtGui.QImage()

        # RPC clerk
        self.clerk = Clerk(state)

        # Drawing content
        self.strokes = state.strokes #local pointer to the node's structure

    def clearImage(self):
        self.image.fill(QtGui.QColor(255, 255, 255))
        self.update()

################################ MOVE TOOL
    def _moveStart(self, pos):
        self.move_pos = pos
        x = pos.x()
        y = pos.y()
        sel_rect = QtCore.QRectF(QtCore.QPointF(x-10,y-10),QtCore.QPointF(x+10,y+10))
        self.selected = -1 #if the click is outside, we deselect
        for s_id,stroke in enumerate(self.strokes): # check selection
            if stroke.toPainterPath().intersects(sel_rect):
                self.selected = s_id
                break
        self.original_move_pos = self.move_pos

    def _moveUpdate(self,pos):
        if self.selected != -1:
            self.moving = True
        if self.moving and self.selected >= 0: 
            offset = pos - self.move_pos 
            self.move_pos = pos
            stroke = self.strokes[self.selected]
            stroke.offsetPosBy(offset)
            self.draw()

    def _moveEnd(self,pos):
        if self.moving and self.selected >= 0: 
            offset = pos - self.original_move_pos 
            self.clerk.moveStroke(self.selected,offset)
            self.moving = False
        else:
            pass
################################ END 

################################ PEN TOOL
    def _penStart(self,pos):
        self.controlPoints = []
        self.controlPoints.append([pos.x(),pos.y()]);
        self.path = QtGui.QPainterPath(pos);
        self.scribbling = True

    def _penUpdate(self,pos):
        if self.scribbling:
            self.path.lineTo(pos);
            self.controlPoints.append([pos.x(),pos.y()]);
            self.drawLineTo()
            self.update()

    def _penEnd(self):
        if self.scribbling:
            stroke = Stroke(self.controlPoints,self.myPenWidth,list(self.myPenColor.getRgb()))
            self.clerk.addStroke(stroke)
            self.strokes.append(stroke)
            self.update()
            self.scribbling = False
################################ END 

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            pos = event.posF()
            if self.current_tool == Tool.MOVE:
                self._moveStart(pos)
            elif self.current_tool == Tool.PEN:
                self._penStart(pos)
            else:
                pass

    def mouseMoveEvent(self, event):
        if (event.buttons() & QtCore.Qt.LeftButton):
            pos = event.posF()
            if self.current_tool == Tool.MOVE:
                self._moveUpdate(pos)
            elif self.current_tool == Tool.PEN:
                self._penUpdate(pos)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if self.current_tool == Tool.MOVE:
                pos = event.posF()
                self._moveEnd(pos)
            elif self.current_tool == Tool.PEN:
                self._penEnd()
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
        """ Draw a temporary line  """
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
        """ Deletes the currently selected stroke """
        if self.selected >= 0:
            print 'deleted', self.strokes[self.selected]
            del(self.strokes[self.selected])
            self.draw()


