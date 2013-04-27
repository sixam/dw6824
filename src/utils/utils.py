import ConfigParser
import random
import os
#import rpc.common
import logging

class Utils:
    def __init__(self):
        pass
    @staticmethod
    def getConfig():
        config = ConfigParser.RawConfigParser()
        for loc in os.listdir("%s/conf" % os.environ.get('DW_BASE')):
            config.read("%s/%s/%s" % (os.environ.get('DW_BASE'),'conf',loc))
        return config

    @staticmethod
    def getLogPath(logtype,local_id):
        config = Utils.getConfig()
        return "%s/%s" % (os.environ.get('DW_BASE'), config.get('log', logtype) % (local_id) )
    @staticmethod
    def generateID():
        s="{0}".format(random.getrandbits(128))
        s = s[1:5]
        return s
    @staticmethod
    def getImagePath():
        return "%s/icons/Canvas.jpg" % os.environ.get('DW_BASE')
