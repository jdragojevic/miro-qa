import sys
import os
import unittest
import time
from sikuli.Sikuli import *
import base_testcase
import myLib.config
from myLib.miro_regions import MiroRegions
from myLib.miro_app import MiroApp
from myLib.preferences_panel import PreferencesPanel


class Test_Feed_Search(base_testcase.Miro_unittest_testcase):
    """Subgroup 42 - Feedsearch.

    """

    def test_001setup(self):
        """fake test to reset db and preferences.

        """
        miro = MiroApp()
        miro.quit_miro()
        myLib.config.set_def_db_and_prefs()
        miro.restart_miro()
        time.sleep(10)
    
    def test_215(self):
        """http://litmus.pculture.org/show_test.cgi?id=215 Feed search, saved search feed

        1. Add list of guide feeds (Static List)
        2. Perform a search and save it.
        3. Verify Search saved
        4. Cleanup

        """
        reg = MiroRegions() 
        miro = MiroApp()
        
        url = "http://pculture.org/feeds_test/list-of-guide-feeds.xml"
        feed = "Static"
        term = "Gimp"
        title = "GimpKnowHow"
        
        #1. add feed
        miro.add_feed(reg, url, feed)
        #2. search
        miro.tab_search(reg, term)
        reg.mtb.click("button_save_as_podcast.png")
        #3. verify search saved
        miro.click_last_podcast(reg)
        #4. cleanup
        type(Key.DELETE)
        #Last chance to verify Gimp is the saved search feed.
        self.assertTrue(reg.m.exists("GIMP"),5)
        miro.remove_confirm(reg, action="remove")
        miro.delete_feed(reg, "Static List")
        miro.handle_crash_dialog('215', db=False, test=False)

    def test_214(self):
        """http://litmus.pculture.org/show_test.cgi?id=214 Feed search, search with spaces

        1. Add 3 blip videos feed
        2. Perform a search with spaces
        3. Verify Search saved
        4. Cleanup

        """
        reg = MiroRegions() 
        miro = MiroApp()
        
        url = "http://pculture.org/feeds_test/3blipvideos.xml"
        feed = "ThreeBlip"
        term = "strange creature"
        title = "Joo Joo"
        
        #1. add feed
        miro.add_feed(reg, url,feed)
        #2. search
        miro.tab_search(reg, term)
        reg.mtb.click("button_save_as_podcast.png")
        #3. verify search saved
        miro.click_last_podcast(reg)
        miro.tab_search(reg, term,confirm_present=True)
        
        #4. cleanup
        miro.click_remove_podcast(reg)
        miro.remove_confirm(reg, action="remove")
        miro.delete_feed(reg, "blip")
        miro.delete_feed(reg, feed)

    def test_213(self):
        """http://litmus.pculture.org/show_test.cgi?id=213 Feed search, delete key.

        1. Add 2-stupid-videos feed
        2. Perform a search
        3. Type in search box the delete key 
        4. Cleanup

        """
        reg = MiroRegions() 
        miro = MiroApp()
        
        url = "http://pculture.org/feeds_test/2stupidvideos.xml"
        feed = "TWO STUPID"
        title = "Flip"
        term = "dinosaur"
        
        #1. add feed
        miro.add_feed(reg, url, feed)
        #2. search
        miro.tab_search(reg, term)
        self.assertFalse(reg.m.exists(title, 5))
        reg.mtb.click(term.upper())
        for x in range(0,8):
            type(Key.LEFT)
        
        for x in range(0,8):
            type(Key.DELETE)

        self.assertTrue(reg.m.exists(title))
        #4. cleanup
        miro.delete_feed(reg, feed)

    def test_78(self):
        """http://litmus.pculture.org/show_test.cgi?id=78 Menu New Search Feed.

        1. Add list of guide feeds (Static List)
        2. From Sidebar -> New Search feed, create saved search channel
        3. Verify Search saved
        4. Cleanup

        """
        reg = MiroRegions() 
        miro = MiroApp()
        
        url = "http://pculture.org/feeds_test/list-of-guide-feeds.xml"
        feed = "Static"
        term = "touring"
        term2 = "Biking"
        title = "Travelling Two"
        dummy_feed_url = "http://pculture.org/feeds_test/2stupidvideos.xml"
        
        #1. add feed
        miro.add_feed(reg, url,feed)
        miro.add_feed(reg, dummy_feed_url,"TwoStupid")
        #2. search
        miro.new_search_feed(reg, term,radio="Podcast",source=feed)
        time.sleep(5)
                        
        #3. verify search saved
        miro.click_last_podcast(reg)
        self.assertTrue(reg.m.exists(term2))
        
        #4. cleanup
        miro.click_remove_podcast(reg)
        miro.remove_confirm(reg, action="remove")
        miro.delete_feed(reg, "Static List")


    def test_720(self):
        """http://litmus.pculture.org/show_test.cgi?id=720 Menu New Search Feed.

        1. Add list of guide feeds (Static List)
        2. Search in the tab
        3. From Sidebar -> New Search feed, create saved search channel
        4. Verify Search saved
        5. Cleanup

        """
        reg = MiroRegions() 
        miro = MiroApp()
        
        url = "http://pculture.org/feeds_test/list-of-guide-feeds.xml"
        feed = "Static"
        term = "Voice"
                
        #1. add feed
        miro.add_feed(reg, url,feed)
        miro.tab_search(reg, term)
        #2. search
        miro.new_search_feed(reg, term,radio="Podcast", source=feed,defaults=True)
                        
        #3. verify search saved
        miro.click_last_podcast(reg)
        self.assertTrue(reg.m.exists(term, 45))
        
        #4. cleanup
        miro.click_remove_podcast(reg)
        miro.remove_confirm(reg, action="remove")
        miro.delete_feed(reg, "Static List")

    def test_721(self):
        """http://litmus.pculture.org/show_test.cgi?id=721 Menu New Search Watched

        1. Add list of guide feeds (Static List)
        2. From Sidebar -> New Search feed, create saved search channel
        3. Verify Search saved
        4. Cleanup

        """
        reg = MiroRegions() 
        miro = MiroApp()
        
    
        feed = "TestData"
        term = "monkey"
        folder_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","WatchTest")
        #1. add feed
        miro.add_watched_folder(reg, folder_path)
        if reg.s.exists("WatchTest"):
            miro.log_result("678","test_721")
        #2. search
        miro.tab_search(reg, term)
        miro.new_search_feed(reg, term,radio="Podcast",source=feed,watched=True)

        #Remove Watched Folder
        miro.open_prefs(reg)
        prefs = PreferencesPanel()
        folder_tab = prefs.open_tab("Folders")
        folder_tab.remove_watched_folder("ArtTest")
        folder_tab.close_prefs()
  
        

    def test_23(self):
        """http://litmus.pculture.org/show_test.cgi?id=23 remember search.

        1. Add 2-stupid-videos feed
        2. Perform a search
        3. Type in search box the delete key 
        4. Cleanup

        """
        reg = MiroRegions() 
        miro = MiroApp()
        url = "http://pculture.org/feeds_test/2stupidvideos.xml"
        feed = "TwoStupid"
        term = "House"
        title = "Dinosaur"
        
        #1. add feed
        miro.add_feed(reg, url,feed)
        #2. search
        miro.tab_search(reg, term)
        self.assertTrue(reg.m.exists(title))
        self.assertFalse(reg.m.exists("Flip"))
        miro.click_sidebar_tab(reg, "Videos")
        reg.s.click(feed)
        self.assertTrue(reg.mtb.exists(term.upper()))
        self.assertTrue(reg.m.exists(title))
        self.assertFalse(reg.m.exists("Flip"))
        #4. cleanup
        miro.delete_feed(reg, "stupid")


    def test_24(self):
        """http://litmus.pculture.org/show_test.cgi?id=24 edit remembered search.

        1. Add 2-stupid-videos feed
        2. Perform a search
        3. Type in search box the delete key 
        4. Cleanup

        """
        reg = MiroRegions() 
        miro = MiroApp()
        
        url = "http://pculture.org/feeds_test/2stupidvideos.xml"
        feed = "TwoStupid"
        term = "Face"
        title = "Flip"
        
        #1. add feed
        miro.add_feed(reg, url,feed)
        miro.set_podcast_autodownload(reg, setting="All")
        #2. search
        miro.tab_search(reg, term)
        self.assertTrue(reg.m.exists(title))

        url2 = "http://pculture.org/feeds_test/list-of-guide-feeds.xml"
        feed2 = "Static"
        term2 = "FilmWeek"
        miro.add_feed(reg, url2,feed2)
        miro.tab_search(reg, "Brooklyn")
        miro.wait_for_item_in_tab(reg, "Videos",title)
        reg.m.click(title)
        type(Key.ENTER)
        time.sleep(2)
        type(" ")
        self.assertTrue(exists("playback_controls.png"))
        miro.shortcut("d")

        reg.s.click(feed2)
        self.assertTrue(reg.mtb.exists("BROOKLYN"))
        miro.tab_search(reg, term2)
        reg.mtb.click("button_save_as_podcast.png")

        miro.click_last_podcast(reg)
        miro.tab_search(reg, term2,confirm_present=True)
        miro.clear_search(reg)
        time.sleep(3)
        if not reg.mtb.exists(term2.upper()):
            miro.log_result("324","test_24",status="pass")
       

        #4. cleanup
        miro.delete_feed(reg, "stupid")
        miro.click_last_podcast(reg)
        miro.delete_current_selection(reg)
        miro.delete_feed(reg, "Static List")

 
# TestRunner posts output in xunit format
if __name__ == "__main__":
    from TestRunner import TestRunner
    TestRunner(Test_Feed_Search).run_tests()
   

