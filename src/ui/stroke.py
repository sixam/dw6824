from PyQt4 import QtCore, QtGui
class Stroke:
    """Basic Stroke"""
    def __init__(self, path=None, width=None, color=None):
        self.path  = path
        self.width = width
        self.color = color

        # id

    def __str__(self):
        return "Stroke: {0}pts - width: {1}, color: {2}".format(len(self.path), self.width, self.color)

    def toPainterPath(self):
        points = self.path
        path   = QtGui.QPainterPath(QtCore.QPointF(*points[0]));
        for pt in points:
            path.lineTo(QtCore.QPointF(*pt));
        return path

