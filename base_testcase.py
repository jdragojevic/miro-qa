import unittest
import os
import sys
from sikuli.Sikuli import *

mycwd = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro")
sys.path.append(os.path.join(mycwd,'myLib'))
import mirolib
import config

class Miro_unittest_testcase(unittest.TestCase):

    def setUp(self):
        self.verificationErrors = []
        print "starting test: ",self.shortDescription()


    def tearDown(self):
        mirolib.handle_crash_dialog(self)
        type(Key.ESC)  #get rid of any leftover dialogs on teardown
        print "finished test: ",self.id()
        self.assertEqual([], self.verificationErrors)
