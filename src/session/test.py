import xmlrpclib
from dp.src.session.central import CentralServer
from dp.src.session.dummyclient import DummyClient
from dp.src.utils.log import Log

if __name__ == '__main__':
    sp              = 9005
    cp              = 8005
    ncp             = 7005

    lc              = Log(100)
    cs              = CentralServer('localhost', sp, lc)
    csrv            = xmlrpclib.Server('http://%s:%s' % ('localhost', sp))

    ld              = Log(50) 
    dc              = DummyClient('localhost', cp, ld, csrv)
    dsrv            = xmlrpclib.Server('http://%s:%s' % ('localhost',cp))

    cs.hosts        = [['localhost']]
    cs.ports        = [[cp]]
    cs.participants = [[dsrv]]

    lncd            = Log(42)
    csrvndc         = xmlrpclib.Server('http://%s:%s' % ('localhost', sp))
    ndc             = DummyClient('localhost', ncp, lncd, csrvndc)



    
    dc.cjoin(0,'localhost',cp)
    ndc.cjoin(0,'localhost', ncp)
