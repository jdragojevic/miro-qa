import sys
import unittest
import time
from sikuli.Sikuli import *
import base_testcase
import myLib.config
from myLib.miro_regions import MiroRegions
from myLib.miro_app import MiroApp

class Test_MiroGuide(base_testcase.Miro_unittest_testcase):
    """Subgroup 8 - Miro Guide

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
        reg = MiroRegions() 
        miro = MiroApp()
        feed = "Studio"
        search = "Studio sketch"
 
        try:
            miro.click_sidebar_tab(reg, "Miro")
            time.sleep(5)
            gr = Region(reg.mtb)
            gr.setH(300)
            gr.click(Pattern("guide_search.png"))
            type(search +"\n")
            time.sleep(5)
            reg.m.find(Pattern("add_feed.png"))
            click(reg.m.getLastMatch())
            time.sleep(5)
            miro.click_podcast(reg, feed)
                        
        finally:
            #4. cleanup
            miro.delete_feed(reg, feed) 

    
# TestRunner posts output in xunit format
if __name__ == "__main__":
    from TestRunner import TestRunner
    TestRunner(Test_MiroGuide).run_tests()
   

