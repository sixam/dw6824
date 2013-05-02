from dp.src.utils.log import Log
l = Log(100)
from dp.src.session.central import CentralServer
cs = CentralServer('bratwurst.mit.edu',8000,l)
