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
         


    def test_215(self):
        """http://litmus.pculture.org/show_test.cgi?id=215 Feed search, saved search feed

        1. Add list of guide feeds (Static List)
        2. Perform a search and save it.
        3. Verify Search saved
        4. Cleanup

        """
        miroRegions = mirolib.launch_miro()
        s = miroRegions[0] #Sidebar Region
        m = miroRegions[1] #Mainview Region
        t = miroRegions[2] #top half screen
        tl = miroRegions[3] #top left quarter
        mtb = miroRegions[4] #main title bar
        
        url = "http://pculture.org/feeds_test/list-of-guide-feeds.xml"
        feed = "Static List"
        term = "Gimp"
        title = "GimpKnowHow"
        
        #1. add feed
        mirolib.add_feed(self,t,s,mtb,url,feed)
        #2. search
        mirolib.tab_search(self,m,s,term)
        mtb.click("button_save_search.png")
        #3. verify search saved
        self.assertTrue(s.exists("GIMP"))
        click(s.getLastMatch())
        mirolib.tab_search(self,m,s,title,confirm_present=True)
        #4. cleanup
        mirolib.delete_feed(self,m,s,"GIMP")
        mirolib.delete_feed(self,m,s,"Static List")
 
    def tearDown(self):
        mirolib.handle_crash_dialog(self)
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
            print "writing log"
            litmusresult.write_log(id_string,stat,byte_output)
        finally:
            buf.truncate(0)
    litmusresult.write_footer()
#or just run it locally
else:
    unittest.main()
