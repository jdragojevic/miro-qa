import sys
import unittest
import time
from sikuli.Sikuli import *
import base_testcase
import myLib.config
import myLib.testvars
from myLib.miro_regions import MiroRegions
from myLib.miro_app import MiroApp



ONE_CLICK_BADGE = Pattern('patrace1.png')

class Test_One_Click_Subscribe(base_testcase.Miro_unittest_testcase):
    """Subgroup 41 - one-click subscribe tests.

    """
    
    

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

        url = "http://ryanishungry.com/subscribe/"
        switchApp(miro.open_ff())
        if reg.t.exists("Firefox",45):
            click(reg.t.getLastMatch())
        miro.shortcut("l")
        time.sleep(2)
        type(url + "\n")
        time.sleep(20)
        if not exists(ONE_CLICK_BADGE):
            for x in range(0,5):
                type(Key.DOWN)
                click(ONE_CLICK_BADGE)
        else:
            click(ONE_CLICK_BADGE)
        time.sleep(20)
        miro.close_ff()
                       
        miro.close_one_click_confirm()
        miro.click_podcast(reg, feed)
        miro.delete_feed(reg, feed)
            
            


    def skiptest_29(self):
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
        site2 = "Blip"
        miro.add_source_from_tab(reg, site_url)
        miro.click_last_source(reg)
        reg.t.find("Subscribe")
        reg.t.click("Subscribe")
        time.sleep(4)
        p = miro.get_sources_region(reg)
        p.highlight(2)
	if p.exists("blip",10) or \
           p.exists("Blip",10):
            print "Blip site added"
        else:
            self.fail("Blip site not added to sidebar")                        
        miro.delete_site(reg, site)
        miro.delete_site(reg, "Blip")
    
        
            
# TestRunner posts output in xunit format
if __name__ == "__main__":
    from TestRunner import TestRunner
    TestRunner(Test_One_Click_Subscribe).run_tests()
   


