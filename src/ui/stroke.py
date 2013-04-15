import copy
from PyQt4 import QtCore, QtGui
from utils.utils import Utils
class Stroke:
    """Basic Stroke"""
    def __init__(self, path=None, width=None, color=None, id='none'):
        self.path  = path
        self.width = width
        self.color = color
        if id == 'none':
            self.id = Utils.generateID()
        else:
            self.id    = id

    def __str__(self):
        return "Stroke: {3} - {0}pts - width: {1}, color: {2}".format(len(self.path), 
                self.width, self.color, self.id[0:5])
    def __deepcopy__(self):
        new = Stroke()
        new.path = copy.deepcopy(self.path);
        new.width = copy.deepcopy(self.width);
        new.color = copy.deepcopy(self.color);
        new.id = copy.deepcopy(self.id)
        return new


    def toPainterPath(self):
        points = self.path
        path   = QtGui.QPainterPath(QtCore.QPointF(*points[0]));
        for pt in points:
            path.lineTo(QtCore.QPointF(*pt));
        return path

    def offsetPosBy(self,offset):
        if isinstance(offset,QtCore.QPointF):
            x = offset.x()
            y = offset.y()
        else:
            x = offset[0]
            y = offset[1]

        for i,pt in enumerate(self.path):
            pt[0] = pt[0] + x
            pt[1] = pt[1] + y
