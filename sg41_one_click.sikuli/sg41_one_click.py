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

        Open a 1-click link
        """
        
        reg = MiroRegions() 
        miro = MiroApp()
        feed = "Steve"

        url = "http://subscribe.getmiro.com/?url1=http%3A//feeds.feedburner.com/SteveGarfieldsVideoBlog"
        switchApp(miro.open_ff())
        if reg.t.exists("Firefox",45):
            click(reg.t.getLastMatch())
        miro.shortcut("l")
        time.sleep(2)
        type(url + "\n")
                               
        miro.close_one_click_confirm()
        miro.click_podcast(reg, feed)
        miro.delete_feed(reg, feed)
        miro.close_ff()

            
            


    def test_29(self):
        """http://litmus.pculture.org/show_test.cgi?id=29 add site from miro site.

        1. Add website as source
        2. click one-click subscribe link 
        3. Verify site added
        4. Cleanup
        """       
        reg = MiroRegions() 
        miro = MiroApp()

        site_url = 'http://qa.pculture.org/feeds_test/one-click-subscribe-tests.html' 
        miro.add_source_from_tab(reg, site_url)
        miro.click_last_source(reg)
        reg.t.find("Add two sites")
        reg.t.click("Add two sites")
        time.sleep(4)
        p = miro.get_sources_region(reg)
        p.highlight(2)
        self.assertTrue(p.exists('southpark', 10)
        miro.delete_site(reg, site)
        miro.delete_site(reg, "Blip")
    
        
            
# TestRunner posts output in xunit format
if __name__ == "__main__":
    from TestRunner import TestRunner
    TestRunner(Test_One_Click_Subscribe).run_tests()
   


