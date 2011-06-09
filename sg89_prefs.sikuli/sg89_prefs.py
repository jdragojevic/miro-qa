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
        if p.exists("System default") or p.exists("English"):
            click(p.getLastMatch())
        for x in range(0,3):
            if not exists("Croatian",3):
                type(Key.PAGE_DOWN)
        for x in range(0,6):
            if not exists("Croatian",3):
                type(Key.PAGE_UP)
        click("Croatian")
        time.sleep(2)
        type(Key.TAB)
        type(Key.TAB)
        type(Key.ENTER)
        #mirolib.shortcut("w")
        type(Key.ESC)
        #3. Restart Miro
        mirolib.quit_miro(self,reg)
        mirolib.restart_miro()

        #4. Verify Changes and reset
        prefs.open_prefs(self,reg,lang='hr',menu='Datoteka',option='Postavke')
        if p.exists("Croatian"):
            click(p.getLastMatch())
        else:
            find("Jezik")
            click(getLastMatch().right(40))
        type(Key.PAGE_UP)
        for x in range(0,3):
            if exists("English",3):
                break
            else:
                type(Key.PAGE_UP)
        click("English")
        time.sleep(2)
        type(Key.TAB)
        type(Key.TAB)
        type(Key.ENTER)
        type(Key.ESC)
        time.sleep(2)
        #5. Restart Miro
        if reg.s.exists("icon-search.png",3) or \
           reg.s.exists("icon-video.png",3):
            click(reg.s.getLastMatch())
            time.sleep(3)
        mirolib.shortcut('q')
        time.sleep(2)
        mirolib.restart_miro()
        self.assertTrue(exists("File"))
   
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()
 

