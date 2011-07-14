import sys
import os
import glob
import unittest
import StringIO
import time
from sikuli.Sikuli import *
mycwd = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro")
sys.path.append(os.path.join(mycwd,'myLib'))
import config
import mirolib
import testvars
import prefs
import base_testcase

class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 42 - Feedsearch.

    """

    def test_001setup(self):
        """fake test to reset db and preferences.

        """
        mirolib.quit_miro(self)
        config.set_def_db_and_prefs()
        mirolib.restart_miro(confirm=False)
        time.sleep(10)
    
    def test_215(self):
        """http://litmus.pculture.org/show_test.cgi?id=215 Feed search, saved search feed

        1. Add list of guide feeds (Static List)
        2. Perform a search and save it.
        3. Verify Search saved
        4. Cleanup

        """
        reg = mirolib._AppRegions()
        
        url = "http://pculture.org/feeds_test/list-of-guide-feeds.xml"
        feed = "Static"
        term = "Gimp"
        title = "GimpKnowHow"
        
        #1. add feed
        mirolib.add_feed(self,reg,url,feed)
        #2. search
        mirolib.tab_search(self,reg,term)
        reg.mtb.click("button_save_as_podcast.png")
        #3. verify search saved
        mirolib.click_last_podcast(self,reg)
        #4. cleanup
        type(Key.DELETE)
        #Last chance to verify Gimp is the saved search feed.
        self.assertTrue(reg.m.exists("GIMP"),5)
        mirolib.remove_confirm(self,reg,action="remove")
        mirolib.delete_feed(self,reg,"Static List")
        mirolib.handle_crash_dialog(self,db=False,test=False)

    def test_214(self):
        """http://litmus.pculture.org/show_test.cgi?id=214 Feed search, search with spaces

        1. Add 3 blip videos feed
        2. Perform a search with spaces
        3. Verify Search saved
        4. Cleanup

        """
        reg = mirolib._AppRegions()
        
        url = "http://pculture.org/feeds_test/3blipvideos.xml"
        feed = "ThreeBlip"
        term = "strange creature"
        title = "Joo Joo"
        
        #1. add feed
        mirolib.add_feed(self,reg,url,feed)
        #2. search
        mirolib.tab_search(self,reg,term)
        reg.mtb.click("button_save_as_podcast.png")
        #3. verify search saved
        mirolib.click_last_podcast(self,reg)
        mirolib.tab_search(self,reg,term,confirm_present=True)
        
        #4. cleanup
        mirolib.click_remove_podcast(self,reg)
        mirolib.remove_confirm(self,reg,action="remove")
        mirolib.delete_feed(self,reg,"blip")

    def test_213(self):
        """http://litmus.pculture.org/show_test.cgi?id=213 Feed search, delete key.

        1. Add 2-stupid-videos feed
        2. Perform a search
        3. Type in search box the delete key 
        4. Cleanup

        """
        reg = mirolib._AppRegions()
        
        url = "http://pculture.org/feeds_test/2stupidvideos.xml"
        feed = "TwoStupid"
        title = "Flip Face"
        term = "dinosaur"
        
        #1. add feed
        mirolib.add_feed(self,reg,url,feed)
        #2. search
        mirolib.tab_search(self,reg,term)
        self.assertFalse(reg.m.exists("Flip",5))
        reg.mtb.click(term.upper())
        for x in range(0,8):
            type(Key.LEFT)
        
        for x in range(0,8):
            type(Key.DELETE)

        self.assertTrue(reg.m.exists("Flip"))
        #4. cleanup
        mirolib.delete_feed(self,reg,"TwoStupid")

    def test_78(self):
        """http://litmus.pculture.org/show_test.cgi?id=78 Menu New Search Feed.

        1. Add list of guide feeds (Static List)
        2. From Sidebar -> New Search feed, create saved search channel
        3. Verify Search saved
        4. Cleanup

        """
        reg = mirolib._AppRegions()
        
        url = "http://pculture.org/feeds_test/list-of-guide-feeds.xml"
        feed = "Static"
        term = "touring"
        term2 = "Biking"
        title = "Travelling Two"
        dummy_feed_url = "http://pculture.org/feeds_test/2stupidvideos.xml"
        
        #1. add feed
        mirolib.add_feed(self,reg,url,feed)
        mirolib.add_feed(self,reg,dummy_feed_url,"TwoStupid")
        #2. search
        mirolib.new_search_feed(self,reg,term,radio="Podcast",source=feed)
        time.sleep(5)
                        
        #3. verify search saved
        mirolib.click_last_podcast(self,reg)
        self.assertTrue(reg.m.exists(term2))
        
        #4. cleanup
        mirolib.click_remove_podcast(self,reg)
        mirolib.remove_confirm(self,reg,action="remove")
        mirolib.delete_feed(self,reg,"Static List")


    def test_720(self):
        """http://litmus.pculture.org/show_test.cgi?id=720 Menu New Search Feed.

        1. Add list of guide feeds (Static List)
        2. From Sidebar -> New Search feed, create saved search channel
        3. Verify Search saved
        4. Cleanup

        """
        reg = mirolib._AppRegions()
        
        url = "http://pculture.org/feeds_test/list-of-guide-feeds.xml"
        feed = "Static"
        term = "Voice"
        dummy_feed_url = "http://pculture.org/feeds_test/2stupidvideos.xml"
        
        #1. add feed
        mirolib.add_feed(self,reg,dummy_feed_url,"TwoStupid")
        mirolib.add_feed(self,reg,url,feed)
        mirolib.tab_search(self,reg,term)
        #2. search
        mirolib.new_search_feed(self,reg,term,radio="Podcast", source=feed,defaults=True)
                        
        #3. verify search saved
        mirolib.click_last_podcast(self,reg)
        self.assertTrue(reg.m.exists(term))
        
        #4. cleanup
        mirolib.click_remove_podcast(self,reg)
        mirolib.remove_confirm(self,reg,action="remove")
        mirolib.delete_feed(self,reg,"Static List")

    def test_721(self):
        """http://litmus.pculture.org/show_test.cgi?id=721 Menu New Search Watched

        1. Add list of guide feeds (Static List)
        2. From Sidebar -> New Search feed, create saved search channel
        3. Verify Search saved
        4. Cleanup

        """
        reg = mirolib._AppRegions()
        
    
        feed = "TestData"
        term = "monkey"
        folder_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","WatchTest")
        #1. add feed
        mirolib.add_watched_folder(self,reg,folder_path)
        if reg.s.exists("WatchTest"):
            mirolib.log_result("678","test_721")
        #2. search
        mirolib.tab_search(self,reg,term)
        mirolib.new_search_feed(self,reg,term,radio="Podcast",source=feed,watched=True)
        prefs.remove_watched_folder(self,reg,folder=folder_path)
  
        

    def test_23(self):
        """http://litmus.pculture.org/show_test.cgi?id=23 remember search.

        1. Add 2-stupid-videos feed
        2. Perform a search
        3. Type in search box the delete key 
        4. Cleanup

        """
        reg = mirolib._AppRegions()
        url = "http://pculture.org/feeds_test/2stupidvideos.xml"
        feed = "TwoStupid"
        term = "House"
        title = "Dinosaur"
        
        #1. add feed
        mirolib.add_feed(self,reg,url,feed)
        #2. search
        mirolib.tab_search(self,reg,term)
        self.assertTrue(reg.m.exists(title))
        self.assertFalse(reg.m.exists("Flip"))
        mirolib.click_sidebar_tab(self,reg,"Videos")
        reg.s.click(feed)
        self.assertTrue(reg.mtb.exists(term.upper()))
        self.assertTrue(reg.m.exists(title))
        self.assertFalse(reg.m.exists("Flip"))
        #4. cleanup
        mirolib.delete_feed(self,reg,"stupid")


    def test_24(self):
        """http://litmus.pculture.org/show_test.cgi?id=24 edit remembered search.

        1. Add 2-stupid-videos feed
        2. Perform a search
        3. Type in search box the delete key 
        4. Cleanup

        """
        reg = mirolib._AppRegions()
        
        url = "http://pculture.org/feeds_test/2stupidvideos.xml"
        feed = "TwoStupid"
        term = "Face"
        title = "Flip"
        
        #1. add feed
        mirolib.add_feed(self,reg,url,feed)
        mirolib.set_podcast_autodownload(self,reg,setting="All")
        #2. search
        mirolib.tab_search(self,reg,term)
        self.assertTrue(reg.m.exists(title))

        url2 = "http://pculture.org/feeds_test/list-of-guide-feeds.xml"
        feed2 = "Static"
        term2 = "FilmWeek"
        mirolib.add_feed(self,reg,url2,feed2)
        mirolib.tab_search(self,reg,"Brooklyn")
        mirolib.wait_for_item_in_tab(self,reg,"Videos",title)
        reg.m.click(title)
        type(Key.ENTER)
        time.sleep(2)
        type(" ")
        self.assertTrue(exists(Pattern("playback_controls.png")))
        mirolib.shortcut("d")

        reg.s.click(feed2)
        self.assertTrue(reg.mtb.exists("BROOKLYN"))
        mirolib.tab_search(self,reg,term2)
        reg.mtb.click("button_save_as_podcast.png")

        mirolib.click_last_podcast(self,reg)
        mirolib.tab_search(self,reg,term2,confirm_present=True)
        mirolib.clear_search(reg)
        time.sleep(3)
        if not reg.mtb.exists(term2.upper()):
            mirolib.log_result("324","test_24",status="pass")
       

        #4. cleanup
        mirolib.delete_feed(self,reg,"stupid")
        mirolib.click_last_podcast(self,reg)
        mirolib.delete_current_selection(self,reg)
        mirolib.delete_feed(self,reg,"Static List")

 
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()
   

