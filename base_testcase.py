import unittest
import os
import sys
mycwd = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro")
sys.path.append(os.path.join(mycwd,'myLib'))
import mirolib

class Miro_unittest_testcase(unittest.TestCase):

    def setUp(self):
        self.verificationErrors = []
        

    def tearDown(self):
        mirolib.handle_crash_dialog(self)
        self.assertEqual([], self.verificationErrors)
