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
import mirolib
import testvars
import base_testcase

class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 41 - one-click subscribe tests.

    """

    def stest_7(self):
        """http://litmus.pculture.org/show_test.cgi?id=7 add feed.

        1. Open Ryan is Hungry
        2. click one-click link
        3. Verify feed added
        4. Cleanup
        """
        
        reg = mirolib.AppRegions()
        mirolib.open_ff()
        try:
            time.sleep(10)
            feed_url = "http://ryanishungry.com/subscribe/"
            mirolib.shortcut("l")
            time.sleep(2)
            type(feed_url + "\n")
            time.sleep(10)
            find(testvars.one_click_badge)
            click(testvars.one_click_badge)
            time.sleep(5)
            mirolib.shortcut('w')
            mirolib.close_ff()
                        
            #Start Miro 
            feed = "Ryan"
            mirolib.close_one_click_confirm(self)
            mirolib.shortcut("r",shift=True)
            mirolib.click_podcast(self,reg,feed)
        finally:
            mirolib.delete_feed(self,reg,feed)
            
            


    def test_29(self):
        """http://litmus.pculture.org/show_test.cgi?id=29 add site from miro site.

        1. Open Awesome website
        2. click one-click subscribe link for revver
        3. Verify site added
        4. Cleanup
        """       
        reg = mirolib.AppRegions()

        
        try:
            site_url = "http://pculture.org/feeds_test/subscription-test-guide.html"
            site = "Awesome"
            site2 = "Revver"
            mirolib.add_source(self,reg,site_url,site)
            mirolib.click_source(self,reg,site)
            reg.t.find("Subscribe")
            reg.t.click("Subscribe")
            time.sleep(4)
            mirolib.click_source(self,reg,site2)
            self.assertTrue(reg.t.exists(testvars.revver_logo))
        finally:                            
            mirolib.delete_site(self,reg,site)
            mirolib.delete_site(self,reg,site2)
    
        
            
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()
   


