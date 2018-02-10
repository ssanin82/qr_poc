import unittest
import subprocess
import time
import os
import sys


class TestServer(unittest.TestCase):
    def setUp(self):
        #print(os.getcwd())
        self.server = subprocess.Popen(['python', 'server.py'], stdout=sys.stdout)

    def tearDown(self):
        self.server.kill()

    def test_simple1(self):
        self.assertTrue(True)
        time.sleep(3)

    def test_simple2(self):
        self.assertTrue(True)
        time.sleep(3)

    def test_simple3(self):
        self.assertTrue(True)
        time.sleep(3)


if '__main__' == __name__:
    unittest.main()
