import sys
import unittest
import time
from sikuli.Sikuli import *
import base_testcase
import myLib.config
from myLib.miro_regions import MiroRegions
from myLib.miro_app import MiroApp


class Test_System(base_testcase.Miro_unittest_testcase):
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
            type(Key.F2, KeyModifier.CTRL)
            for x in range(0,11):
                type(Key.RIGHT)
            type(Key.DOWN)
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
            type(Key.F2, KeyModifier.CTRL)
            for x in range(0,11):
                type(Key.RIGHT)
            type(Key.DOWN)
        else:
            type('f', KEY_ALT)
            time.sleep(1)
            type(Key.LEFT)
        reg.t.click("Test Soft")
        miro.handle_crash_dialog( '682', db=True, test=True)      
   
# TestRunner posts output in xunit format
if __name__ == "__main__":
    from TestRunner import TestRunner
    TestRunner(Test_System).run_tests()
