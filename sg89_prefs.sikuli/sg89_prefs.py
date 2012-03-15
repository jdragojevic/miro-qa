import sys
import unittest
import time
from sikuli.Sikuli import *
import base_testcase
import myLib.config
from myLib.miro_regions import MiroRegions
from myLib.miro_app import MiroApp
from myLib.pref_general_tab import PrefGeneralTab
from myLib.preferences_panel import PreferencesPanel

class Test_Preferences(base_testcase.Miro_unittest_testcase):
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
        prefs = PreferencesPanel()
        general_tab = prefs.open_tab("General")
        general_tab.change_default_language( "Croatian")
        general_tab.close_prefs()
       
        miro.restart_miro()
        
        miro.open_prefs(reg, menu="Datoteka", option="Postavke")
        prefs = PreferencesPanel()
        general_tab = prefs.open_tab("General")
        general_tab.change_to_english_language(from_lang="Croatian")
        general_tab.close_prefs()
        
    def test_999reset(self):
        """fake test to reset db and preferences.

        """
        miro = MiroApp()
        miro.quit_miro()
        myLib.config.set_def_db_and_prefs()
        miro.restart_miro()
        time.sleep(10) 


   
# TestRunner posts output in xunit format
if __name__ == "__main__":
    from TestRunner import TestRunner
    TestRunner(Test_Preferences).run_tests()
 

