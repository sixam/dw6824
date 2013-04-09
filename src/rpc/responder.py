from PyQt4 import QtCore, QtGui
from ui import ui

class RPCresponder:
    def __init__(self,window):
        # make all of the string functions available through
        # string.func_name
        import string
        self.string = string

    def _listMethods(self):
        # implement this method so that system.listMethods
        # knows to advertise the strings methods
        return list_public_methods(self) + \
                ['string.' + method for method in list_public_methods(self.string)]

    # RPC methods
    def get_strokes(self):
        return self.window.scribbleArea.strokes

    def add_stroke(self,strokeData):
        stroke = ui.Stroke(**strokeData)
        self.window.scribbleArea.strokes.append(stroke)
        self.window.scribbleArea.draw()
        return True

