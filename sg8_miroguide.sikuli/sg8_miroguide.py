import sys
import os
import glob
import unittest
import StringIO
import time
from sikuli.Sikuli import *

mycwd = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro")
sys.path.append(os.path.join(mycwd,'myLib'))
import base_testcase
import config
import mirolib
import testvars


class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 41 - one-click subscribe tests.

    """
  
    def test_6(self):
        """http://litmus.pculture.org/show_test.cgi?id=6 add feed from MiroGuide.

        1. Open Miro
        2. search for a feed and add it.
        3. Verify feed added
        4. Cleanup
        """
        setAutoWaitTimeout(60)
        pass
        
        #set the search regions
        reg = mirolib.AppRegions()
        feed = "StupidVideos"
 
        try:
            mirolib.click_sidebar_tab(self,reg,"Miro")
            reg.mtb.click(testvars.guide_search)
            type("StupidVideos\n")
            time.sleep(5)
            reg.m.find(Pattern("add_feed.png"))
            click(reg.m.getLastMatch())
            time.sleep(5)
            mirolib.click_podcast(self,reg,feed)
                        
        finally:
            #4. cleanup
            mirolib.delete_feed(self,reg,"StupidVideos") 

    
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()
   

