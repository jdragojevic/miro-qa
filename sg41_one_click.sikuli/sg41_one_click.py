import sys
import os
import glob
import unittest
import StringIO
import time

mycwd = os.path.join(os.getenv("SIKULI_TEST_HOME"),"Miro")
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
        myApp = App("Miro")
        miroRegions = mirolib.launch_miro()
        SidebarRegion = miroRegions[0] #Sidebar Region
        MainviewRegion = miroRegions[1] #Mainview Region
         


    def stest_7(self):
        """http://litmus.pculture.org/show_test.cgi?id=7 add feed.

        1. Open Ryan is Hungry
        2. click one-click link
        3. Verify feed added
        4. Cleanup
        """
        miroApp = App("Miro")
        s = self.SidebarRegion
        m = self.MainviewRegion
        
        try:
            print "open ff"
            switchApp(mirolib.open_ff())
            feed_url = "http://ryanishungry.com/subscribe/"
            feed = "feed_ryan_is_hungry.png"
            mirolib.shortcut("l")
            type(feed_url + "\n")
            wait(testvars.one_click_badge)
            click(testvars.one_click_badge)
            mirolib.close_one_click_confirm(self)
            #Start Miro and set regions
            miroRegions = mirolib.launch_miro()
            s = miroRegions[0] #Sidebar Region
            m = miroRegions[1] #Mainview Region
            
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
            #first_time miro launch
            miroRegions = mirolib.launch_miro()
            s = miroRegions[0] #Sidebar Region
            m = miroRegions[1] #Mainview Region

            
            click("Sidebar")
            click("Add Website")
            wait(2)
            type(site_url+"\n")
            
            self.assertTrue(s.exists("Awesome"))
            click(getLastMatch())
            m.click("subscribe_to_revver.png")
            s.click("Revver Video")
            self.assertTrue(m.exists("Revver Video"))
        finally:
            mirolib.delete_feed(self,"Revver",m,s)
            mirolib.delete_feed(self,"Awesome",m,s) 
        
            
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

