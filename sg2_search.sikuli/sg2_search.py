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
        try:
            miroApp = App("Miro")
            setAutoWaitTimeout(60)
            miroRegions = mirolib.launch_miro()
            s = miroRegions[0] #Sidebar Region
            m = miroRegions[1] #Mainview Region
            t = miroRegions[2] #top half screen
            tl = miroRegions[3] #top left quarter

            SEARCHES = {"Blip": 'lizards', "YouTube": 'cosmicomics'}
            for engine, term in SEARCHES.iteritems():
                mirolib.click_sidebar_tab(self,m,s,"search")
                mirolib.tab_search(self,m,s,term)
                #specify the search engine
                t = m.find(term) 
                t1= capture(t.getX()-10, t.getY(), 5, 8,)
                click(t1)
                t.click(engine)
                type("\n") #enter the search
                t.exists("Save as a feed")
                mirolib.click_sidebar_tab(self,m,s,"video")
                mirolib.click_sidebar_tab(self,m,s,"search")
                self.assertTrue(t.exists(term))
        finally:
            pass

        
    def test_322(self):
        """http://litmus.pculture.org/show_test.cgi?id=82 remember last search.

        1. Perform a search
        2. Click off the tab
        3. Click back and verify the search is remembered.
        4. Cleanup
        """
        miroApp = App("Miro")
        setAutoWaitTimeout(60)
        miroRegions = mirolib.launch_miro()
        s = miroRegions[0] #Sidebar Region
        m = miroRegions[1] #Mainview Region
        t = miroRegions[2] #top half screen
        tl = miroRegions[3] #top left quarter

        searches = {"Blip": "lizards", "YouTube": "cosmicomics"}
        for engine, term in searches.iteritems():
            mirolib.click_sidebar_tab(self,m,s,"search")
            mirolib.search_tab_search(self,m,s,term)
            #specify the search engine
            st = m.find("tabsearch_clear.png")
            st.highlight(5)
            st1 = capture(st.getX()-80, st.getY(), 80, 80)
            st1.highlight(10)
            st1.find(term.upper())
            st2 = capture(st.getX()-10, st.getY(), 5, 8)
            st2.highlight()
            click(t2)
            st1.click(engine)
            type("\n") #enter the search
            t.exists("Save Search")
            t.click("Save Search")
            self.assertTrue(s.exists(term))
            s.click(term)
            #FIXME verify feed has items
            #cleanup
            for x in searches.keys():
                mirolib.delete_feed(self,m,s,x)
        
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

