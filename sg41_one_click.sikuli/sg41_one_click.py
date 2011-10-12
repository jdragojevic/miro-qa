import sys
import unittest
import time
from sikuli.Sikuli import *
import base_testcase
import myLib.config
import myLib.testvars
from myLib.miro_regions import MiroRegions
from myLib.miro_app import MiroApp

class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 41 - one-click subscribe tests.

    """
    
    ONE_CLICK_BADGE = Pattern('patrace.png')

    def test_7(self):
        """http://litmus.pculture.org/show_test.cgi?id=7 add feed.

        1. Open Ryan is Hungry
        2. click one-click link
        3. Verify feed added
        4. Cleanup
        """
        
        reg = MiroRegions() 
        miro = MiroApp()
        feed = "Ryan"
        try:
            url = "http://ryanishungry.com/subscribe/"
            switchApp(miro.open_ff())
            if reg.t.exists("Firefox",45):
                click(reg.t.getLastMatch())
            miro.shortcut("l")
            time.sleep(2)
            type(url + "\n")
            time.sleep(20)
            find(ONE_CLICK_BADGE)
            click(ONE_CLICK_BADGE)
            time.sleep(25)
            miro.close_ff()
                        
            #Start Miro    
            miro.close_one_click_confirm(self)
            miro.shortcut("r",shift=True)
            miro.click_podcast(reg, feed)
        finally:
            miro.delete_feed(reg, feed)
            
            


    def test_29(self):
        """http://litmus.pculture.org/show_test.cgi?id=29 add site from miro site.

        1. Open Awesome website
        2. click one-click subscribe link for revver
        3. Verify site added
        4. Cleanup
        """       
        reg = MiroRegions() 
        miro = MiroApp()

        
        site_url = "http://pculture.org/feeds_test/subscription-test-guide.html"
        site = "Awesome"
        site2 = "Revver"
        miro.add_source_from_tab(reg, site_url)
        miro.click_last_source(reg)
        reg.t.find("Subscribe")
        reg.t.click("Subscribe")
        time.sleep(4)
        p = miro.get_sources_region(reg)
	if p.exists("http://rev",3) or \
           p.exists("revver",3):
            print "revver site added"
        else:
            self.fail("revver site not added to sidebar")                        
        miro.delete_site(reg, site)
        miro.delete_site(reg, "revver")
    
        
            
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv, ).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite, ).litmus_test_run()
   


