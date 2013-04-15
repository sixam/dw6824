import ConfigParser
import random
import os
import rpc.common

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
        config = utils.getConfig()
        return "%s/%s" % (os.environ.get('DW_BASE'), config.get('log', logtype) % (local_id) )
    @staticmethod
    def generateID():
        return "{0}".format(random.getrandbits(128))
