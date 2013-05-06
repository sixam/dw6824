import resources
from PyQt4 import QtCore, QtGui
from rpc.clerk import Clerk
from stroke import Stroke
from tool import Tool
from utils.utils import Utils

from threading import Lock


class ScribbleArea(QtGui.QLabel):
    """ Main Area for drawing
        =====================

        Capture mouse events and update the state accordingly.
        All the broadcasting is done by the clerk object

    """
    def __init__(self, state, parent=None):
        super(ScribbleArea, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_StaticContents)

        # Current tool mode 
        self.current_tool = Tool.PEN

        # Drawing state
        self.controlPoints = [];
        self.scribbling    = False
        self.myPenWidth    = 3.0
        self.myPenColor    = QtGui.QColor(0,0,0)

        # Select and move state variables
        self.select_rect = QtCore.QRectF
        self.selected    = -1
        self.moving      = False

        # Drawing canvas
        self.image = QtGui.QImage(':/images/Canvas.png', format=None)

        # RPC clerk
        self.clerk = Clerk(state)

        # Drawing content
        self.state = state    # This should never be to the left of an assignment
                              # fields should never be accessed, only methods!

        # access to the logger
        self.log = state.log

        # init the stroke list
        self.strokes = []
        self.lock = Lock()

    def clearImage(self):
        """ 
            Resets drawing context
        """
        self.image.fill(QtGui.QColor(255, 255, 255))
        self.update()

    def strokesSignalHandler(self):
        """ 
            Updates drawing context upon reception of a 'modified stroke list'
            signal
        """
        self.log.lock( 'signal (lock)')
        self.lock.acquire()
        self.log.lock( 'signal (locked)')
        self.log.ui('update state, reset selection')
        if self.selected >= 0:
            id = self.strokes[self.selected].id

        self.strokes = self.state.getStrokes()
        if self.selected >= 0:
            self.selected = -1
            for s in self.strokes:
                if s.id == id:
                    self.selected = self.strokes.index(s)
                    break
        self.draw()
        self.lock.release()
        self.log.lock( 'signal (unlock)')

    def mousePressEvent(self, event):
        self.log.ui("mouse pressed")
        if event.button() == QtCore.Qt.LeftButton:
            pos = event.posF()
            if self.current_tool == Tool.MOVE:
                self._moveStart(pos)
            elif self.current_tool == Tool.PEN:
                self._penStart(pos)
            else:
                pass

    def mouseMoveEvent(self, event):
        self.log.ui("mouse moved")
        if (event.buttons() & QtCore.Qt.LeftButton):
            pos = event.posF()
            if self.current_tool == Tool.MOVE:
                self._moveUpdate(pos)
            elif self.current_tool == Tool.PEN:
                self._penUpdate(pos)

    def mouseReleaseEvent(self, event):
        self.log.ui("mouse released")
        if event.button() == QtCore.Qt.LeftButton:
            if self.current_tool == Tool.MOVE:
                pos = event.posF()
                self._moveEnd(pos)
            elif self.current_tool == Tool.PEN:
                self._penEnd()

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

    def resizeImage(self, image, newSize):
        if image.size() == newSize:
            return
        newImage = QtGui.QImage(newSize, QtGui.QImage.Format_RGB32)
        newImage.fill(QtGui.qRgb(255, 255, 255))
        painter = QtGui.QPainter(newImage)
        painter.drawImage(QtCore.QPoint(0, 0), image)
        self.image = newImage

    def draw(self):
        """ Updates the drawing context """
        self.image = QtGui.QImage(':/images/Canvas.png', format=None)
        painter = QtGui.QPainter(self.image)
        for stroke in self.strokes:
            if not stroke:
                continue
            painter.setPen(QtGui.QPen(QtGui.QColor(*stroke.color), stroke.width,
                QtCore.Qt.SolidLine, QtCore.Qt.FlatCap, QtCore.Qt.MiterJoin))
            path = stroke.toPainterPath()
            painter.drawPath(path);
        self.update()

    def drawLineTo(self):
        """ Draw a temporary line for live preview  """
        painter = QtGui.QPainter(self.image)
        painter.setPen(QtGui.QPen(self.myPenColor, self.myPenWidth,
                QtCore.Qt.SolidLine, QtCore.Qt.FlatCap, QtCore.Qt.MiterJoin))
        painter.drawPath(self.path);

    def delete(self):
        """ Deletes the currently selected stroke """
        self.log.lock( 'delete (lock)')
        self.lock.acquire()
        self.log.lock( 'delete (locked)')
        self.log.ui('delete',self.selected)
        if self.selected >= 0:
            index = self.selected
            s = self.strokes[index]
            self.selected = -1
            self.lock.release()
            self.log.lock( 'delete (unlock)')
            self.clerk.deleteStroke(s,index)
        else:
            self.lock.release()
            self.log.lock( 'delete (unlock)')

    def penColor(self):
        return self.myPenColor
        
    def setPenColor(self,color):
        self.myPenColor = color
        self.log.ui( 'new color', color)

    def penWidth(self):
        return self.myPenWidth
        
    def setPenWidth(self,width):
        self.myPenWidth = width

    def setTool(self,tool):
        self.current_tool = tool
        self.log.ui('changed tool:',tool)

################################ MOVE TOOL
    def _moveStart(self, pos):
        """ 
            Move operation starts
        """
        self.move_pos = pos
        x = pos.x()
        y = pos.y()
        sel_rect = QtCore.QRectF(QtCore.QPointF(x-10,y-10),QtCore.QPointF(x+10,y+10))
        self.log.lock( 'move start (lock)')
        self.lock.acquire()
        self.log.lock( 'move start (locked)')
        self.selected = -1 #if the click is outside, we deselect
        for i,stroke in reversed(list(enumerate(self.strokes))): # check selection
            if stroke.toPainterPath().intersects(sel_rect):
                self.selected = i
                self.log.ui( '\033[34mselected:',self.strokes[self.selected],'\033[0m')
                break
        self.original_move_pos = self.move_pos
        self.lock.release()
        self.log.lock( 'move start (unlock)')

    def _moveUpdate(self,pos):
        """ 
            Move operation in progress
        """
        self.log.lock( 'move update (lock)')
        self.lock.acquire()
        self.log.lock( 'move update (locked)')
        if self.selected >=0 :
            self.moving = True
        if self.moving and self.selected >= 0:
            offset = pos - self.move_pos 
            self.move_pos = pos
            self.strokes[self.selected].offsetPosBy(offset)
            self.draw()
        self.lock.release()
        self.log.lock( 'move update (unlock)')

    def _moveEnd(self,pos):
        """ 
            Move operation ends
        """
        self.log.lock( 'move end (lock)')
        self.lock.acquire()
        self.log.lock( 'move end (locked)')
        if self.moving and self.selected >= 0: 
            offset = pos - self.move_pos 
            self.moving = False
            self.lock.release()
            self.log.lock( 'move end (unlock)')
            self.clerk.moveStroke(self.strokes[self.selected],self.selected,[offset.x(),offset.y()])
        else:
            self.lock.release()
            self.log.lock( 'move end (unlock)')
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
            self.update()
            self.scribbling = False
################################ END 

