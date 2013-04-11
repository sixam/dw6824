from PyQt4 import QtCore, QtGui
from dp.src.ui.stroke import Stroke

class RPCresponder:
    def __init__(self, state, window):
        # make all of the string functions available through
        # string.func_name
        import string
        self.string = string
        self.window = window
        self.strokes = state.strokes

    def _listMethods(self):
        # implement this method so that system.listMethods
        # knows to advertise the strings methods
        return list_public_methods(self) + \
                ['string.' + method for method in list_public_methods(self.string)]

    # RPC methods
    def get_strokes(self):
        return self.strokes

    def addStroke(self,strokeData):
        stroke = Stroke(**strokeData)
        self.strokes.append(stroke)
        self.window.scribbleArea.draw()
        return True

    def moveStroke(self,moveOp):
        print moveOp
        id = moveOp['id']
        offset = moveOp['offset']
        stroke = self.strokes[id]
        stroke.offsetPosBy(offset)
        self.window.scribbleArea.draw()
        return True

