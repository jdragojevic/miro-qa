import unittest
from sikuli.Sikuli import *
from myLib.miro_app import MiroApp


class Miro_unittest_testcase(unittest.TestCase):

    def setUp(self):
        self.verificationErrors = []
        print "starting test: ",self.shortDescription()


    def tearDown(self):
        miro = MiroApp()
        miro.handle_crash_dialog(self, self.id())
        type(Key.ESC)  #get rid of any leftover dialogs on teardown
        print "finished test: ",self.id()
        self.assertEqual([], self.verificationErrors)
