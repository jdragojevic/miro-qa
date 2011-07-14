import sys
import os
import glob
import unittest
import StringIO
import time
from sikuli.Sikuli import *
mycwd = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro")
sys.path.append(os.path.join(mycwd,'myLib'))
import config
import mirolib
import testvars
import base_testcase


class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 19 - system tests.

    """


    def test_55(self):
        """http://litmus.pculture.org/show_test.cgi?id=55 Test Crash Reporter with DB.

        1. Perform a search of crash inducing text
        2. Submit crash dialog with db
        3. Quit Miro
        """
       
        setAutoWaitTimeout(60)
        reg = mirolib._AppRegions()

        term ="LET'S TEST DTV'S CRASH REPORTER TODAY"
        mirolib.click_sidebar_tab(self,reg,"Search")
        mirolib.search_tab_search(self,reg,term)
        mirolib.handle_crash_dialog(self,test=True)
        mirolib.search_tab_search(self,reg,term=" ",engine=None)
        
            
    def test_54(self):
        """http://litmus.pculture.org/show_test.cgi?id=54 Test Crash Reporter no DB.

        1. Perform a search of crash inducing text
        2. Submit crash dialog
        3. Quit Miro
        """
        print self.id()
        setAutoWaitTimeout(60)
        reg = mirolib._AppRegions()

        term ="LET'S TEST DTV'S CRASH REPORTER TODAY"
        mirolib.click_sidebar_tab(self,reg,"Search")
        mirolib.search_tab_search(self,reg,term)
        mirolib.handle_crash_dialog(self,db=False,test=True)


    def test_681(self):
        """http://litmus.pculture.org/show_test.cgi?id=54 Test Crash Reporter no DB.

        1. Perform a search of crash inducing text
        2. Submit crash dialog
        3. Quit Miro
        """
        print self.id()
        setAutoWaitTimeout(60)
        reg = mirolib._AppRegions()
        if config.get_os_name() == "osx":
            reg.tl.click("Dev")
        else:
            type('f',KEY_ALT)
            time.sleep(1)
            type(Key.LEFT)
        reg.t.click("Test Soft")
        mirolib.handle_crash_dialog(self,db=False,test=True)

    def test_682(self):
        """http://litmus.pculture.org/show_test.cgi?id=54 Test Crash Reporter with DB.

        1. Perform a search of crash inducing text
        2. Submit crash dialog
        3. Quit Miro
        """
        print self.id()
        reg = mirolib._AppRegions()

        if config.get_os_name() == "osx":
            reg.tl.click("Dev")
        else:
            type('f',KEY_ALT)
            time.sleep(1)
            type(Key.LEFT)
        reg.t.click("Test Soft")
        mirolib.handle_crash_dialog(self,db=True,test=True)      
   
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()
   
