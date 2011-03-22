import sys
import os
import glob
import unittest
import StringIO
import time

mycwd = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro")
sys.path.append(os.path.join(mycwd,'myLib'))
import config
import mirolib
import testvars
import litmusresult

setBundlePath(config.get_img_path())


class Miro_Suite(unittest.TestCase):
    """Subgroup 41 - one-click subscribe tests.

    """
    def setUp(self):
        self.verificationErrors = []

    def test_7(self):
        """http://litmus.pculture.org/show_test.cgi?id=7 add feed.

        1. Open Ryan is Hungry
        2. click one-click link
        3. Verify feed added
        4. Cleanup
        """
        
        ffApp = App("Firefox")
        reg = mirolib.AppRegions()
        
        try:
            print "open ff"
            App.open(mirolib.open_ff())
            find(testvars.ffhome)
            ffApp.focus()
            feed_url = "http://ryanishungry.com/subscribe/"
            mirolib.shortcut("l")
            time.sleep(2)
            type(feed_url + "\n")
            time.sleep(10)
            find(testvars.one_click_badge)
            click(testvars.one_click_badge)
            time.sleep(5)
            mirolib.close_one_click_confirm(self)
            
            #Start Miro 
            reg = mirolib.AppRegions()
            self.assertTrue(reg.s.exists("Ryan is Hungry"))
            reg.s.click("Ryan is Hungry")
        finally:
            mirolib.delete_feed(self,reg,"Ryan is Hungry")
            ffApp.close()
            


    def stest_29(self):
        """http://litmus.pculture.org/show_test.cgi?id=29 add site from miro site.

        1. Open Awesome website
        2. click one-click subscribe link for revver
        3. Verify site added
        4. Cleanup
        """       
        reg = mirolib.AppRegions()

        
        try:
            site_url = "http://pculture.org/feeds_test/subscription-test-guide.html"
            reg.tl.click("Sidebar")
            reg.tl.click("Website")
            time.sleep(4)
            type(site_url+"\n")
            reg.s.click("Awesome")
            reg.m.find("subscribe_to_revver.png")
            reg.m.click("subscribe_to_revver.png")
            time.sleep(4)
            reg.s.find("Revver Video")
            reg.s.click("Revver Video")
            time.sleep(4)
            reg.m.find(testvars.revver_logo)
            self.assertTrue(reg.m.exists(testvars.revver_logo))
        finally:                            
            mirolib.delete_feed(self,reg,"Revver")
            mirolib.delete_feed(self,reg,"Awesome") 
        
            
    def tearDown(self):
        self.assertEqual([], self.verificationErrors)
        
        
# Post the output directly to Litmus
if config.testlitmus == True:
    suite_list = unittest.getTestCaseNames(Miro_Suite,'test')
    suite = unittest.TestSuite()
    for x in suite_list:
        suite.addTest(Miro_Suite(x))

    buf = StringIO.StringIO()
    runner = unittest.TextTestRunner(stream=buf)
    litmusresult.write_header(config.get_os_name())
    for x in suite:
        runner.run(x)
        # check out the output
        byte_output = buf.getvalue()
        id_string = str(x)
        stat = byte_output[0]
        try:
            litmusresult.write_log(id_string,stat,byte_output)
        finally:
            buf.truncate(0)
    litmusresult.write_footer()
#or just run it locally
else:
    unittest.main()

