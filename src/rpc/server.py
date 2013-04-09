from SimpleXMLRPCServer import SimpleXMLRPCServer
from ui import ui
from PyQt4 import QtCore, QtGui
import sys
from threading import Thread

class Node:
    def __init__(self):
        # make all of the string functions available through
        # string.func_name
        import string
        self.string = string

        self.window = ui.MainWindow()
        self.window.show()

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
        return 0

class Server:
    def __init__(self,identifier,port):
        self.server = SimpleXMLRPCServer((identifier,port))
        self.server.register_introspection_functions()
        self.server.register_instance(Node())

        t = Thread(target = self.run)
        t.daemon = True
        t.start()

    def run(self):
        self.server.serve_forever()

# client code : import xmlrpclib
# srv = xmlrpclib.Server('http://localhost:8000')
# srv.function
