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
        prefs.open_tab(self,reg,p,"general")
        #2. change language to croatian (hr)
        p.click("System default")
        
        self.assertTrue(p.exists("pref_lang_hr.png"))
        click(p.getLastMatch())
        mirolib.shortcut("w")
        #3. Restart Miro
        mirolib.quit_miro(self,reg)
        switchApp(mirolib.open_miro())
        wait("Miro",45)
        click(getLastMatch())
        #4. Verify Changes and reset
        p = prefs.open_prefs(self,'hr','Datoteka','Postavke')       
        self.assertTrue(p.exists("pref_language_pulldown.png"))
        click(p.getLastMatch())
        self.assertTrue(p.exists("pref_lang_def.png"))
        click(p.getLastMatch())
        mirolib.shortcut("w")
        #5. Restart Miro
        mirolib.quit_miro(self,reg)
        switchApp(mirolib.open_miro())
   
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()
 

