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
 
        try:
            reg.mtb.click(testvars.guide_search)
            type("StupidVideos \n")
            reg.m.find(testvars.guide_add_feed)
            click(reg.m.getLastMatch())
            time.sleep(5)
            self.assertTrue(reg.s.exists("StupidVideos"))
                        
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
   

