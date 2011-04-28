import sys
import os
import glob
import unittest
import StringIO
import time
from sikuli.Sikuli import *

sys.path.append(os.path.join(os.getcwd(),'myLib'))
import config
import mirolib
import prefs
import testvars
import base_testcase

class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 89 - preferences tests.

    """    

    def test_467(self):
        """http://litmus.pculture.org/show_test.cgi?id=467 change sys language.

        1. Open Preferences
        2. Change the system default language
        3. Restart Miro
        4. Verify changes and reset
        5. Restart Miro
        
        """
        reg = mirolib.AppRegions()
        #1. open preferences
        p = prefs.open_prefs(self,reg)
        #2. change language to croatian (hr)
        p.click("System default")
        for x in range(0,3):
            if not exists("Croatian",1):
                type(Key.PAGE_DOWN)
        click("Croatian")
        mirolib.shortcut("w")
        #3. Restart Miro
        mirolib.quit_miro(self,reg)
        mirolib.restart_miro(self,reg)

        #4. Verify Changes and reset
        prefs.open_prefs(self,reg,lang='hr',menu='Datoteka',option='Postavke')       
        self.assertTrue(exists("Croatian"))
        click(getLastMatch())
        self.assertTrue(exists("System",1))
        for x in range(0,3):
            if not exists("System",1):
                type(Key.PAGE_UP)
        click("System")
        mirolib.shortcut("w")
        #5. Restart Miro
        mirolib.quit_miro(self,reg)
        mirolib.restart_miro(self,reg)
        self.assertTrue(exists("File"))
   
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()
 

