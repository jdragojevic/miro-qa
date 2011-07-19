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
import base_testcase
import mirolib
import testvars

class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 2 - one-click subscribe tests.

    """             
    def test_82(self):
        """http://litmus.pculture.org/show_test.cgi?id=82 remember last search.

        1. Perform a search
        2. Click off the tab
        3. Click back and verify the search is remembered.
        4. Cleanup
        """
       
        setAutoWaitTimeout(60)
        reg = mirolib._AppRegions()

        SEARCHES = {"blip": 'octopus', "YouTube": 'cosmicomics'}
        for engine, term in SEARCHES.iteritems():
            mirolib.click_sidebar_tab(self,reg,"Search")
            mirolib.search_tab_search(self,reg,term,engine)
            mirolib.click_sidebar_tab(self,reg,"Videos")
            mirolib.click_sidebar_tab(self,reg,"Search")
            self.assertTrue(reg.mtb.exists(term.upper()))


        
    def test_322(self):
        """http://litmus.pculture.org/show_test.cgi?id=322 search and save as a podcast

        1. Perform a search
        2. Click off the tab
        3. Click back and verify the search is remembered.
        4. Cleanup
        """
        setAutoWaitTimeout(60)
        reg = mirolib._AppRegions()

        searches = {"blip": "python", "YouTube": "cosmicomics", "Revver": "beiber", "Yahoo": "Canada", "DailyMotion": "Russia", "Metavid": "africa", "Mininova": "vancouver", "Video": "toronto"}
        for engine, term in searches.iteritems():
        	mirolib.click_sidebar_tab(self,reg,"search")
                mirolib.search_tab_search(self,reg,term,engine)
                reg.mtb.click("button_save_as_podcast.png")
                if engine == "blip":
                    saved_search = engine
                else:
                    saved_search = engine +" for"
                mirolib.click_podcast(self,reg,saved_search)
                
                #FIXME verify feed has items
        #cleanup
        for x in searches.keys():
            mirolib.delete_feed(self,reg,x)

   
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()
   


