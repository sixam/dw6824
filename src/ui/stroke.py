from PyQt4 import QtCore, QtGui
class Stroke:
    """Basic Stroke"""
    def __init__(self, path=None, width=None, color=None, id=0):
        self.path  = path
        self.width = width
        self.color = color
        self.id    = id

    def __str__(self):
        return "Stroke: {0}pts - width: {1}, color: {2}".format(len(self.path), self.width, self.color)

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
