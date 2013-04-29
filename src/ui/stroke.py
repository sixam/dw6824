import copy
from PyQt4 import QtCore, QtGui
from utils.utils import Utils

sizeX = 1024
sizeY = 768

class Stroke:
    """Basic Stroke"""
    def __init__(self, path=[], width=0, color=[0,0,0,255], id='none'):
        self.path  = path
        self.width = width
        self.color = color
        if id == 'none':
            self.id = Utils.generateID()
        else:
            self.id    = id

    def __str__(self):
        c = self.getBarycenter()
        return "Stroke : %s - [%01.02f,%01.02f] - c: {0} - pts:{1}".format(self.color,len(self.path)) % (self.id[0:5],c[0]/sizeX,c[1]/sizeY)

    def __copy__(self):
        new       = Stroke()
        new.path  = copy.copy(self.path);
        new.width = copy.copy(self.width);
        new.color = copy.copy(self.color);
        new.id    = copy.copy(self.id)
        return new

    def __cmp__(self, other):
        eq = True
        if self.path != other.path:
            eq = False
        if self.width != other.width:
            eq = False
        if self.color != other.color:
            eq = False
        if self.id != other.id:
            eq = False
        b1 = self.getBarycenter()
        b2 = other.getBarycenter()
        if b1[0]!=b2[0] or b1[1]!=b2[1]:
            eq = False
        if eq:
            return 0
        return -1

    def marshall(self):
        """ Wraps the stroke data into a RPC-friendly format """
        packet          = {}
        packet['path']  = self.path
        packet['width'] = self.width
        packet['color'] = self.color
        packet['id']    = self.id
        return packet

    def toPainterPath(self):
        """ Transform the strokes to a QT line """
        points = self.path
        path   = QtGui.QPainterPath(QtCore.QPointF(*points[0]));
        for pt in points:
            path.lineTo(QtCore.QPointF(*pt));
        return path

    def getBarycenter(self):
        x = 0
        y = 0
        n = len(self.path)
        if n > 0:
            for pt in self.path:
                x += pt[0]
                y += pt[1]
            x /= float(n)
            y /= float(n)
        return [x,y]

    def moveTo(self,newpos):
        """ Change the stroke position to the supplied location """
        c = self.getBarycenter()
        offset = [newpos[0]-c[0],newpos[1]-c[1]]
        self.offsetPosBy(offset)

    def offsetPosBy(self,offset):
        """ Change the stroke position by an offset """
        if isinstance(offset,QtCore.QPointF):
            x = offset.x()
            y = offset.y()
        else:
            x = offset[0]
            y = offset[1]

        for i,pt in enumerate(self.path):
            pt[0] = pt[0] + x
            pt[1] = pt[1] + y
