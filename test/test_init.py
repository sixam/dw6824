import unittest
import sys
import datetime
import time

from dp.src.utils.utils import Utils
from dp.src.rpc.peer import Peer


class TestSimple(unittest.TestCase):
    """simple test"""

    def setUp(self):
        # NOTE : problem with ports
        config = Utils.getConfig()
        servers = ['local1']
        self.peers = []

        for server in servers:
            local_id = server
            ip = config.get(local_id,'ip')
            port = int(config.get(local_id,'port'))
            id = int(config.get(local_id,'id'));
            noUI = True
            build_ui = False
            peer = Peer(ip,port, id,build_ui)
            print 'added',peer
            for server2 in servers:
                if server2 != server:
                    remote_id = server2
                    ip_r   = config.get(remote_id,'ip')
                    port_r = int(config.get(remote_id,'port'))
                    peer.addPeer(ip_r,port_r)
            self.peers.append(peer)

    def tearDown(self):
        del self.peers
        pass


# Test basic add/move/delete strokes
    def test_basic(self):
        print 'incorrect ordering, got: wanted:'
        pass

# Test concurrent add/move/delete strokes
    def test_concurrent_add_delete(self):
        pass

# Test unreliable add/move/delete strokes

# Test basic join/leave peers

# Test unreliable join/leave



