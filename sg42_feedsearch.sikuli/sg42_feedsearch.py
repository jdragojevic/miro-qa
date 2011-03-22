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
        setAutoWaitTimeout(60)
         


    def test_215(self):
        """http://litmus.pculture.org/show_test.cgi?id=215 Feed search, saved search feed

        1. Add list of guide feeds (Static List)
        2. Perform a search and save it.
        3. Verify Search saved
        4. Cleanup

        """
        reg = mirolib.AppRegions()
        
        url = "http://pculture.org/feeds_test/list-of-guide-feeds.xml"
        feed = "Static List"
        term = "Gimp"
        title = "GimpKnowHow"
        
        #1. add feed
        mirolib.add_feed(self,t,s,reg.mtb,url,feed)
        #2. search
        mirolib.tab_search(self,m,s,term)
        reg.mtb.click("button_save_search.png")
        #3. verify search saved
        self.assertTrue(reg.s.exists("GIMP"))
        click(reg.s.getLastMatch())
        mirolib.tab_search(self,m,s,title,confirm_present=True)
        #4. cleanup
        mirolib.delete_feed(self,m,s,"GIMP")
        mirolib.delete_feed(self,m,s,"Static List")

    def test_214(self):
        """http://litmus.pculture.org/show_test.cgi?id=214 Feed search, search with spaces

        1. Add 3 blip videos feed
        2. Perform a search with spaces
        3. Verify Search saved
        4. Cleanup

        """
        reg = mirolib.AppRegions()
        
        url = "http://pculture.org/feeds_test/3blipvideos.xml"
        feed = "3 blip"
        term = "strange creature"
        title = "Joo Joo"
        
        #1. add feed
        mirolib.add_feed(self,t,s,reg.mtb,url,feed)
        #2. search
        mirolib.tab_search(self,m,s,term)
        reg.mtb.click("button_save_search.png")
        #3. verify search saved
        self.assertTrue(reg.s.exists("STRANGE"))
        click(reg.s.getLastMatch())
        mirolib.tab_search(self,m,s,title,confirm_present=True)
        #4. cleanup
        mirolib.delete_feed(self,m,s,"STRANGE")
        mirolib.delete_feed(self,m,s,"blip")

    def test_213(self):
        """http://litmus.pculture.org/show_test.cgi?id=213 Feed search, delete key.

        1. Add 2-stupid-videos feed
        2. Perform a search
        3. Type in search box the delete key 
        4. Cleanup

        """
        reg = mirolib.AppRegions()
        
        url = "http://pculture.org/feeds_test/2stupidvideos.xml"
        feed = "2 stupid"
        term = "dinosaur"
        title = "Flip Face"
        
        #1. add feed
        mirolib.add_feed(self,t,s,reg.mtb,url,feed)
        #2. search
        mirolib.download_all_items(self,m)
        mirolib.wait_for_item_in_tab(self,m,s,"videos","Flip")
        mirolib.wait_for_item_in_tab(self,m,s,"videos","Dinosaur")
        mirolib.tab_search(self,m,s,term)
        self.assertFalse(reg.m.exists("Flip"))
        reg.mtb.click(term)
        for x in range(0,8):
            type(Key.LEFT)
        
        for x in range(0,8):
            type(Key.DELETE)

        self.assertTrue(reg.m.exists("Flip"))
        #4. cleanup
        mirolib.delete_feed(self,m,s,"stupid")

    def test_78(self):
        """http://litmus.pculture.org/show_test.cgi?id=78 Menu New Search Feed.

        1. Add list of guide feeds (Static List)
        2. From Sidebar -> New Search feed, create saved search channel
        3. Verify Search saved
        4. Cleanup

        """
        reg = mirolib.AppRegions()
        
        url = "http://pculture.org/feeds_test/list-of-guide-feeds.xml"
        feed = "Static List"
        term = "touring"
        title = "Travelling Two"
        
        #1. add feed
        mirolib.add_feed(self,t,s,reg.mtb,url,feed)
        #2. search
        mirolib.new_search_feed(self,m,t,term,"Feed",feed)
                        
        #3. verify search saved
        self.assertTrue(reg.s.exists("Static List for 'touring'"))
        click(reg.s.getLastMatch())
        mirolib.tab_search(self,m,s,title,confirm_present=True)
        #4. cleanup
        mirolib.delete_feed(self,m,s,"touring")
        mirolib.delete_feed(self,m,s,"Static List")

    def test_23(self):
        """http://litmus.pculture.org/show_test.cgi?id=23 remember search.

        1. Add 2-stupid-videos feed
        2. Perform a search
        3. Type in search box the delete key 
        4. Cleanup

        """
        reg = mirolib.AppRegions()
        url = "http://pculture.org/feeds_test/2stupidvideos.xml"
        feed = "2 stupid"
        term = "House"
        title = "Dinosaur"
        
        #1. add feed
        mirolib.add_feed(self,t,s,reg.mtb,url,feed)
        #2. search
        mirolib.tab_search(self,m,s,term)
        self.assertTrue(reg.m.exists(title))
        self.assertFalse(reg.m.exists("Flip"))
        mirolib.click_sidebar_tab(self,m,s,"Videos")
        reg.s.click(feed)
        self.assertTrue(reg.mtb.exists(term.upper()))
        self.assertTrue(reg.m.exists(title))
        self.assertFalse(reg.m.exists("Flip"))
        #4. cleanup
        mirolib.delete_feed(self,m,s,"stupid")


    def test_24(self):
        """http://litmus.pculture.org/show_test.cgi?id=24 remember search.

        1. Add 2-stupid-videos feed
        2. Perform a search
        3. Type in search box the delete key 
        4. Cleanup

        """
        reg = mirolib.AppRegions()
        
        url = "http://pculture.org/feeds_test/2stupidvideos.xml"
        feed = "2 stupid"
        term = "House"
        title = "Dinosaur"
        
        #1. add feed
        mirolib.add_feed(self,t,s,reg.mtb,url,feed)
        #2. search
        mirolib.tab_search(self,m,s,term)
        self.assertTrue(reg.m.exists(title))
        mirolib.download_all_items(self,m)

        url2 = "http://pculture.org/feeds_test/list-of-guide-feeds.xml"
        feed2 = "Static List"
        mirolib.add_feed(self,t,s,reg.mtb,url2,feed2)
        mirolib.tab_search(self,m,s,"Brooklyn")
        mirolib.wait_for_item_in_tab(self,m,s,"Videos",title)
        reg.m.click(title)
        reg.t.click("Playback")
        reg.t.click("Play")
        self.assertTrue(exists("playback_controls.png"))
        mirolib.shortcut("d")

        reg.s.click(feed2)
        self.assertTrue(reg.mtb.exists("BROOKLYN"))
        mirolib.tab_search(self,m,s,"filmweek")
        reg.mtb.click("Save Search")

        self.assertTrue(reg.s.exists("FILMWEEK"))
        reg.s.click("for 'FILMWEEK'")
        self.assertTrue(reg.m.exists("FilmWeek"))

        #4. cleanup
        mirolib.delete_feed(self,m,s,"stupid")
        mirolib.delete_feed(self,m,s,"FILMWEEK")
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
