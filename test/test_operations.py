import sys
import time
import random

from .test_common import GenericTestCase

class TestOperations(GenericTestCase):
    """ Test basic operations, multiple instances, multiples peers with and
    without failures """

    def test_basic(self):
        """ Basic - add strokes """
        for ck in self.clerks:
            for sid in self.ids:
                ck.thaw(sid)

        p0 = self.peers[0]
        p1 = self.peers[1]
        ck0 = self.clerks[0]
        ck1 = self.clerks[1]

        s = self.genRandomStrokes(2)

        ck0.addStroke(s[0])
        time.sleep(1)
        ck1.addStroke(s[1])
        time.sleep(1)

        self.assertStrokesEqual()

    def test_basic_delete(self):
        """ Basic - delete strokes """
        p0 = self.peers[0]
        p1 = self.peers[1]
        ck0 = self.clerks[0]
        ck1 = self.clerks[1]

        s = self.genRandomStrokes(2)

        ck0.addStroke(s[0])
        time.sleep(1)
        ck1.addStroke(s[1])
        time.sleep(1)
        ck0.deleteStroke(s[0],0)
        time.sleep(1)

        self.assertStrokesEqual()

    def test_basic_move(self):
        """ Basic - move strokes """
        p0 = self.peers[0]
        p1 = self.peers[1]
        ck0 = self.clerks[0]
        ck1 = self.clerks[1]

        s = self.genRandomStrokes(4)

        ck0.addStroke(s[0])
        ck0.addStroke(s[1])
        time.sleep(1)
        ck1.addStroke(s[2])
        ck1.addStroke(s[3])
        time.sleep(1)

        strokes = ck0.getStrokes()
        index = 0
        offset = [10,10]
        ck0.moveStroke(strokes[index],index,offset)
        time.sleep(1)

        self.assertStrokesEqual()

    def test_delay_01(self):
        """ Delay - simple """
        p0 = self.peers[0]
        p1 = self.peers[1]
        ck0 = self.clerks[0]
        ck1 = self.clerks[1]
        
        s = self.genRandomStrokes(12)

        ck0.addStroke(s[0]);
        ck1.addStroke(s[1])
        time.sleep(1)
        
        p0.kill()
        p1.kill()
        
        ck0.addStroke(s[2]);
        ck1.addStroke(s[4])
        time.sleep(1)
        
        p0.revive()
        p1.revive()
        time.sleep(1)

        ck0.addStroke(s[6]);
        ck1.addStroke(s[7])
        time.sleep(1)

        self.assertStrokesEqual()

    def test_delay_02(self):
        """ Delay - dOPT puzzle """
        p0 = self.peers[0]
        p1 = self.peers[1]
        ck0 = self.clerks[0]
        ck1 = self.clerks[1]

        s = self.genRandomStrokes(12)

        ck0.addStroke(s[0]);
        ck1.addStroke(s[1])
        time.sleep(1)
        
        p0.kill()
        p1.kill()
        
        ck0.addStroke(s[2]);
        ck0.addStroke(s[3]);
        ck1.addStroke(s[4])
        time.sleep(1)
        
        p0.revive()
        p1.revive()
        time.sleep(1)

        ck0.addStroke(s[5])
        ck1.addStroke(s[6])

        time.sleep(2)
        self.assertStrokesEqual()

    def test_manystrokes(self):
        """ Many - strokes """
        s = self.genRandomStrokes(100)
        for stroke in s:
            i = random.randint(0,1024) % len(self.peers)
            self.clerks[i].addStroke(stroke)
        time.sleep(30)
        self.assertStrokesEqual()

    def test_manypeers(self):
        """ Many - peers """
        self.addMultipleServers(2)
        for ck in self.clerks:
            for sid in self.ids:
                ck.thaw(sid)

        s = self.genRandomStrokes(20)
        for stroke in s:
            i = random.randint(0,len(self.peers)-1)
            self.clerks[i].addStroke(stroke)
        time.sleep(10)

        for ck in self.clerks:
            ck.state.getStrokes()

        self.assertStrokesEqual()

    def test_manypeers02(self):
        """ Many - peers, strokes, operations """
        self.addMultipleServers(2)
        for ck in self.clerks:
            for sid in self.ids:
                ck.thaw(sid)

        n_strokes = 12
        s = self.genRandomStrokes(n_strokes)
        for stroke in s:
            i = random.randint(0,len(self.peers)-1)
            self.clerks[i].addStroke(stroke)

        for s in range(n_strokes/2):
            i = random.randint(0,len(self.peers)-1)
            strokes = self.clerks[i].getStrokes()
            if not strokes:
                continue
            m = random.randint(0, len(strokes) - 1)
            if not strokes[m]:
                continue
            if random.randint(0,1) :
                offset = [random.randint(1,200),random.randint(1,200)]
                self.clerks[i].moveStroke(strokes[m],m,offset)
            else:
                self.clerks[i].deleteStroke(strokes[m],m)
        time.sleep(25)

        self.assertStrokesEqual()

    def test_manydead(self):
        """ Many - peers dying"""
        self.addMultipleServers(3)
        for ck in self.clerks:
            for sid in self.ids:
                ck.thaw(sid)

        s = self.genRandomStrokes(9)
        for stroke in s:
            i = random.randint(0,1024) % len(self.peers)
            self.clerks[i].addStroke(stroke)
        time.sleep(5)
        
        dead = []
        s = self.genRandomStrokes(15)
        for stroke in s:
            i = random.randint(0,1024) % len(self.peers)
            self.clerks[i].addStroke(stroke)
            if random.randint(0,1) > 0 and i not in dead:
                self.peers[i].kill()
                dead.append(i)
        time.sleep(15)
        for p in dead:
            self.peers[p].revive()
        s = self.genRandomStrokes(len(self.peers))
        for stroke in s:
            i = s.index(stroke)
            self.clerks[i].addStroke(stroke)

        time.sleep(25)

        self.assertStrokesEqual()

    def test_manydeadmanyops(self):
        """Many peer - Many ops - Many die"""
        self.addMultipleServers(3)
        for ck in self.clerks:
            for sid in self.ids:
                ck.thaw(sid)

        s = self.genRandomStrokes(9)
        for stroke in s:
            i = random.randint(0,1024) % len(self.peers)
            self.clerks[i].addStroke(stroke)
        
        dead = []
        s = self.genRandomStrokes(9)
        for stroke in s:
            i = random.randint(0,1024) % len(self.peers)
            if i in dead:
                continue
            coin = random.randint(0,2)
            if coin == 0:
                self.clerks[i].addStroke(stroke)
            if coin == 1:
                strokes = self.clerks[i].getStrokes()
                if not strokes:
                    continue
                m = random.randint(0, len(strokes) - 1)
                offset = [random.randint(1,200),random.randint(1,200)]
                self.clerks[i].moveStroke(strokes[m],m,offset)
            else:
                strokes = self.clerks[i].getStrokes()
                if not strokes:
                    continue
                m = random.randint(0, len(strokes) - 1)
                self.clerks[i].deleteStroke(strokes[m], m)
            if random.randint(0,1) > 0 and i not in dead:
                self.peers[i].kill()
                dead.append(i)
        time.sleep(5)

        for p in dead:
            self.peers[p].revive()
        time.sleep(35)

        self.assertStrokesEqual()
