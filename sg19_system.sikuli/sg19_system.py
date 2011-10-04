import sys
import unittest
import time
from sikuli.Sikuli import *
import base_testcase
import myLib.config
from myLib.miro_regions import MiroRegions
from myLib.miro_app import MiroApp


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
        reg = MiroRegions()
        miro = MiroApp()

        term ="LET'S TEST DTV'S CRASH REPORTER TODAY"
        miro.click_sidebar_tab(reg, "Search")
        miro.search_tab_search(reg, term)
        miro.handle_crash_dialog( '55', test=True)
        miro.search_tab_search(reg, term=" ",engine=None)
        
            
    def test_54(self):
        """http://litmus.pculture.org/show_test.cgi?id=54 Test Crash Reporter no DB.

        1. Perform a search of crash inducing text
        2. Submit crash dialog
        3. Quit Miro
        """
        print self.id()
        setAutoWaitTimeout(60)
        reg = MiroRegions()
        miro = MiroApp()

        term ="LET'S TEST DTV'S CRASH REPORTER TODAY"
        miro.click_sidebar_tab(reg, "Search")
        miro.search_tab_search(reg, term)
        miro.handle_crash_dialog( '54', db=False, test=True)


    def test_681(self):
        """http://litmus.pculture.org/show_test.cgi?id=54 Test Crash Reporter no DB.

        1. Perform a search of crash inducing text
        2. Submit crash dialog
        3. Quit Miro
        """
        print self.id()
        setAutoWaitTimeout(60)
        reg = MiroRegions()
        miro = MiroApp()
        if myLib.config.get_os_name() == "osx":
            reg.tl.click("Dev")
        else:
            type('f',KEY_ALT)
            time.sleep(1)
            type(Key.LEFT)
        reg.t.click("Test Soft")
        miro.handle_crash_dialog( '681', db=False, test=True)

    def test_682(self):
        """http://litmus.pculture.org/show_test.cgi?id=54 Test Crash Reporter with DB.

        1. Perform a search of crash inducing text
        2. Submit crash dialog
        3. Quit Miro
        """
        print self.id()
        reg = MiroRegions()
        miro = MiroApp()

        if myLib.config.get_os_name() == "osx":
            reg.tl.click("Dev")
        else:
            type('f',KEY_ALT)
            time.sleep(1)
            type(Key.LEFT)
        reg.t.click("Test Soft")
        miro.handle_crash_dialog( '682', db=True, test=True)      
   
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv, ).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite, ).litmus_test_run()
   
