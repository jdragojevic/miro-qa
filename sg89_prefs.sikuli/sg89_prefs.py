import sys
import unittest
import time
from sikuli.Sikuli import *
import base_testcase
import myLib.config
from myLib.miro_regions import MiroRegions
from myLib.miro_app import MiroApp
from myLib.pref_general_tab import PrefGeneralTab

class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 89 - preferences tests.

    """    

    def test_1(self):
        """http://litmus.pculture.org/show_test.cgi?id=467 change sys language.

        1. Open Preferences
        2. Change the system default language
        3. Restart Miro
        4. Verify changes and reset
        5. Restart Miro
        
        """
        reg = MiroRegions()
        miro = MiroApp()
        #1. open preferences
        miro.open_prefs(reg)
        prefs = PrefGeneralTab()
        prefs.change_default_language( "Croatian")
        miro.restart()
        
        miro.open_prefs(reg, menu="Datoteka", option="Postavke")
        prefs = PrefGeneralTab()
        prefs.change_to_english_language(from_lang="Croatian")
        prefs.close_prefs()
        

        


    def test_999reset(self):
        """fake test to reset db and preferences.

        """
        miro = MiroApp()
        miro.quit_miro()
        myLib.config.set_def_db_and_prefs()
        miro.restart_miro()
        time.sleep(10) 


   
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv, ).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite, ).litmus_test_run()
 

