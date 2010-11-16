import sys
import os
import glob
import unittest
import StringIO
import time

mycwd = os.path.join(os.getcwd(),"Miro")
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
        setAutoWaitTimeout(60)
        switchApp(mirolib.open_miro())
         


    def stest_7(self):
        """http://litmus.pculture.org/show_test.cgi?id=7 add feed.

        1. Open Ryan is Hungry
        2. click one-click link
        3. Verify feed added
        4. Cleanup
        """
        try:
            switchApp(mirolib.open_ff())
            feed_url = "http://ryanishungry.com/subscribe/"
            feed = "feed_ryan_is_hungry"
            type("l", KEY_CMD)
            type(feed_url + "\n")
            wait(testvars.one_click_badge)
            click(testvars.one_click_badge)
            mirolib.close_one_click_confirm(self)
            switchApp(mirolib.open_miro())
            self.assertTrue(exists(feed))
            click(feed)
        finally:
            mirolib.delete_feed(self,feed)


    def test_29(self):
        """http://litmus.pculture.org/show_test.cgi?id=29 add site from miro site.

        1. Open Awesome website
        2. click one-click subscribe link for revver
        3. Verify site added
        4. Cleanup
        """
        try:
            site_url = "http://pculture.org/feeds_test/subscription-test-guide.html"
            switchApp(mirolib.open_miro())
            click("menu_sidebar.png")
            click("menu_add_website.png")
            wait("enter_the_url.png")
            type(site_url+"\n")
            
            self.assertTrue(exists("site_awesome.png"))
            click("site_awesome.png")
            click("subscribe_to_revver.png")
            click("site_revver.png")
            self.assertTrue(exists("revver.logo.png")
            
        finally:
            mirolib.delete_feed(self,"site_revver.png")
            mirolib.delete_feed(self,"site_awesome.png") 
        
            
    def tearDown(self):
##        switchApp(mirolib.open_miro())
##        type("q", KEY_CMD)
##        time.sleep(10)
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

