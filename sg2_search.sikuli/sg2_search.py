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
    """Subgroup 2 - one-click subscribe tests.

    """
    def setUp(self):
        self.verificationErrors = []
                


    def test_82(self):
        """http://litmus.pculture.org/show_test.cgi?id=82 remember last search.

        1. Perform a search
        2. Click off the tab
        3. Click back and verify the search is remembered.
        4. Cleanup
        """
       
        setAutoWaitTimeout(60)
        miroRegions = mirolib.launch_miro()
        s = miroRegions[0] #Sidebar Region
        m = miroRegions[1] #Mainview Region
        t = miroRegions[2] #top half screen
        tl = miroRegions[3] #top left quarter
        mtb = miroRegions[4] #main title bar
        mtb.highlight(3)

        SEARCHES = {"Blip": 'lizards', "YouTube": 'cosmicomics'}
        for engine, term in SEARCHES.iteritems():
            mirolib.click_sidebar_tab(self,m,s,"Search")
            mirolib.search_tab_search(self,mtb,term,engine)
            mirolib.click_sidebar_tab(self,m,s,"Videos")
            mirolib.click_sidebar_tab(self,m,s,"Search")
            self.assertTrue(mtb.exists(term.upper()))


        
    def test_322(self):
        """http://litmus.pculture.org/show_test.cgi?id=82 remember last search.

        1. Perform a search
        2. Click off the tab
        3. Click back and verify the search is remembered.
        4. Cleanup
        """
        setAutoWaitTimeout(60)
        miroRegions = mirolib.launch_miro()
        s = miroRegions[0] #Sidebar Region
        m = miroRegions[1] #Mainview Region
        t = miroRegions[2] #top half screen
        tl = miroRegions[3] #top left quarter
        mtb = miroRegions[4] #main title bar

        searches = {"Blip": "lizards", "YouTube": "cosmicomics"}
        for engine, term in searches.iteritems():
        	mirolib.click_sidebar_tab(self,m,s,"search")
                mirolib.search_tab_search(self,mtb,term,engine)
                mtb.highlight(5)
                mtb.click("button_save_as_podcast.png")
                self.assertTrue(s.exists(term.upper()))
                click(s.getLastMatch())
                #FIXME verify feed has items
        #cleanup
        for x in searches.keys():
            mirolib.delete_feed(self,m,s,x)
        
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
            litmusresult.write_log(id_string,stat,byte_output)
        finally:
            buf.truncate(0)
    litmusresult.write_footer()
#or just run it locally
else:
    unittest.main()

