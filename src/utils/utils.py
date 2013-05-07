import ConfigParser
import random
import os
#import rpc.common
import logging

class Utils:
    def __init__(self):
        pass

    @staticmethod
    def generateID():
        s="{0}".format(random.getrandbits(128))
        s = s[1:5]
        return s
