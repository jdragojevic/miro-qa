import sys
import unittest
import time
from sikuli.Sikuli import *
import base_testcase
import myLib.config
from myLib.miro_regions import MiroRegions
from myLib.miro_app import MiroApp
from myLib.pref_podcasts_tab import PrefPodcastsTab


class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 6 - Feeds tests.

    """

    def test_001setup(self):
        """Pre subgroup run cleanup and preferences check.

        This isn't a real tests and is just meant to make sure the subgroup is starting with usual preferences settings and clean sidebar.
        """
        miro = MiroApp()
        miro.quit_miro()
        myLib.config.set_def_db_and_prefs()
        miro.restart_miro()
        time.sleep(10)

        
    
    def test_123(self):
        """http://litmus.pculture.org/show_test.cgi?id=123 add feed more than once.

        Litmus Test Title:: 123 - add a channel more than once  
        Description: 
         1. Add a channel from the Miro Guide.  
         2. Copy the URL and use the Add Feed dialog to add it.  
         3. Verify feed not duplicated.
         4. Cleanup
        """       
        #set the search regions
        reg = MiroRegions() 
        miro = MiroApp()
        feed = "EEVblog"
        feed2 = "TED"
        miro.click_sidebar_tab(reg, "Miro")
        gr = Region(reg.mtb)
        gr.setH(300)
        gr.click(Pattern("guide_search.png"))
        type(feed2 +"\n")
        time.sleep(5)
        reg.m.find(Pattern("add_feed.png"))
        click(reg.m.getLastMatch())
        miro.click_sidebar_tab(reg, "Miro")
        gr.click(Pattern("guide_search.png"))
        type(feed + "\n")
        time.sleep(10)
        reg.m.find(Pattern("add_feed.png"))
        click(reg.m.getLastMatch())
        time.sleep(20)
        miro.click_last_podcast(reg)
        time.sleep(5)
        #2. Copy the url and attempt to add it
        reg.t.click("Sidebar")
        tmpr = Region(reg.t.getLastMatch().below())
        tmpr.setW(tmpr.getW()+200)
        tmpr.highlight(3)
        if tmpr.exists("Copy") or tmpr.exists("URL"):
            click(tmpr.getLastMatch())
        time.sleep(2)
        miro.shortcut("n")        
        time.sleep(2)
        type(Key.ENTER)

        #3. Verify feed not duplicated
        p = miro.get_podcasts_region(reg)
        time.sleep(2)
        miro.count_images(reg,  img=feed,region="sidebar",num_expected=1)
        miro.delete_feed(reg, feed)
        miro.delete_feed(reg, feed2)
        
        
        
    def test_138(self): #shortened as there no more feed counter and can't count too much stuff.
        """http://litmus.pculture.org/show_test.cgi?id=138 clear out old items.

        Litmus Test Title:: 138 Channels - clear out old items 
        Description: 
         1. Add a feed that adds five new items each time it's updated.
         2. Update the feed to add new items.
         3. Modify old items settings to verify items cleared.
         4. Cleanup

        """
        
        #set the search regions
        reg = MiroRegions() 
        miro = MiroApp()        
        url = "http://bluesock.org/~willg/cgi-bin/newitemsfeed.cgi"
        feed = "my feed"
        miro.add_feed(reg, url,feed)
        miro.get_podcasts_region(reg)

        
        miro.tab_search(reg, "my feed")
        miro.toggle_list(reg)
        
        miro.count_images(reg, img="my feed",region="list",num_expected=5)
        miro.click_podcast(reg, feed)
        miro.shortcut("r")
        time.sleep(10)
        miro.get_podcasts_region(reg)
        if miro.count_images(reg, img="my feed",region="list",num_expected=10) == 10:
            miro.log_result("99","test_92") #verifies update podcast shortcut
        miro.click_podcast(reg, feed)
        for x in range(0,3):
            miro.shortcut("r")
            time.sleep(3)
        miro.open_podcast_settings(reg)
        miro.change_podcast_settings(reg, option="Podcast Items",setting="Keep 0")
        time.sleep(2)
        miro.get_podcasts_region(reg)
        miro.count_images(reg, img="my feed",region="list",num_expected=5)
        #4. cleanup
        miro.delete_feed(reg, "my feed") 
   
    def test_339(self):
        """http://litmus.pculture.org/show_test.cgi?id=339 delete feed with dl items.

        Litmus Test Title:: 339 - channels delete a feed with downloaded items
        Description: 
        1. Add the 2-stupid-videos feed, and download both items in the feed.  
        2. Remove Feed and Keep the videos.  
        3. Verify videos are displayed in the non-feed section of the Library
        4. Cleanup
        """

        
        #set the search regions
        reg = MiroRegions() 
        miro = MiroApp()

        url = "http://pculture.org/feeds_test/2stupidvideos.xml"
        feed = "TwoStupid"

        #1. Add the feed and start dl
        miro.add_feed(reg, url,feed)
        time.sleep(3)
        miro.toggle_normal(reg)
#       miro.count_images(reg,  "item-context-button.png",region="mainright",num_expected=2)
        miro.set_podcast_autodownload(reg, setting="All")
        miro.wait_for_item_in_tab(reg, "videos","Flip")
        miro.wait_for_item_in_tab(reg, "videos","Dinosaur")
        miro.click_podcast(reg, feed)
        type(Key.DELETE)
        miro.remove_confirm(reg, action="keep")
        miro.click_sidebar_tab(reg, "videos")
        miro.tab_search(reg, "Flip",confirm_present=True)
        miro.tab_search(reg, "Dinosaur",confirm_present=True)
        #4. cleanup
        miro.delete_items(reg, "Flip","videos")
        miro.delete_items(reg, "Dinosaur","videos")

    def test_338(self):
        """http://litmus.pculture.org/show_test.cgi?id=338 delete feed with dl items.

        Litmus Test Title:: 338 - channels delete a feed with downloads in progress
        Description: 
        1. Add the 3-blip-videos feed. Start items downloading  
        2. Remove the feed and verify downloads are removed.
        """

      

        #set the search regions
        reg = MiroRegions() 
        miro = MiroApp()

        url = "http://pculture.org/feeds_test/3blipvideos.xml"
        feed = "ThreeBlip"

        #1. Add the feed and start dl
        miro.cancel_all_downloads(reg)
        miro.add_feed(reg, url,feed)
        miro.download_all_items(reg)
        time.sleep(2)
        miro.confirm_download_started(reg, "The Joo")
        miro.delete_feed(reg, feed)
        time.sleep(5)
        if reg.s.exists("Downloading",5):
            self.fail("Downloading tab still present")
       


    def test_117(self):
        """http://litmus.pculture.org/show_test.cgi?id=117 delete multiple feeds then cancel.

        Litmus Test Title:: 117 - delete multiple feeds then cancel
        Description: 
        1. Add several feeds from list of guide feeds
        2. Select them all
        3. Delete, the cancel the delete
        4. Cleanup
        """
        
        #set the search regions
        reg = MiroRegions() 
        miro = MiroApp()
        
        miro.open_prefs(reg)
        prefs = PrefPodcastsTab()
        prefs.open_tab("Podcasts")
        prefs.autodownload_setting("Off")
        prefs.default_view_setting("Standard")
        prefs.close_prefs()
        del prefs

        url = "http://pculture.org/feeds_test/list-of-guide-feeds.xml"
        feed = "Static"
        feedlist = ["Center", "Earth"]

        #1. Add the feed and start dl
        miro.add_feed(reg, url,feed)
        for f in feedlist:
            miro.tab_search(reg, f)
            self.assertTrue(reg.m.exists("Add this"))
            reg.m.click("Add this")
            time.sleep(4)
        miro.tab_search(reg, "")
        miro.toggle_normal(reg)

        p = miro.get_podcasts_region(reg)
        miro.click_sidebar_tab(reg, "Music")
        miro.click_podcast(reg, feed)            
        #2. Select them all
       
        keyDown(Key.SHIFT)  
        for x in feedlist:
            if p.exists(x):
                p.click(x)
            else:
                print "could not find feed" +str(x)
            time.sleep(2)
        keyUp(Key.SHIFT)
        #3. Delete then cancel.  Verify still exists Static List
        if reg.m.exists("Delete",4) or reg.m.exists("button_mv_delete_all.png",4):
            click(reg.m.getLastMatch())
        else:
            self.fail("Can't find Delete All button in main view")
        miro.remove_confirm(reg, "cancel")
        p = miro.get_podcasts_region(reg)
        time.sleep(5)
        self.assertTrue(p.exists("Static",5))
        #4. Cleanup
        feedlist.append("Static")
        for x in feedlist:
            print x
            miro.delete_feed(reg, x)


    def test_641(self):
        """http://litmus.pculture.org/show_test.cgi?id=641, delete with invalid url.
       
            Litmus Test Title:: 641 - Deleting podcast with invalid urls
            Steps to Perform:
            1. Select "Add podcast" from Sidebar menu.
            2. Enter URL http://subscribe.getmiro.com/?url1=http%3A%2F%2Fparticipatoryculture.org%2Ffeeds_test%2Ffeed1.rss
            3. Click "Create Podcast" button
            4. Click "Yes" in "This podcast is not compatible with Miro" window
            5. While the podcast is downloading, right click on it and select "Remove" option.
        """

        reg = MiroRegions() 
        miro = MiroApp()
        url = "http://subscribe.getmiro.com/?url1=http%3A%2F%2Fparticipatoryculture.org%2Ffeeds_test%2Ffeed1.rss"
        
        #SET GLOBAL PREFERENCES
        miro.open_prefs(reg)
        prefs = PrefPodcastsTab()
        prefs.open_tab("Podcasts")
        prefs.autodownload_setting("All")
        prefs.close_prefs()
       
        
        reg.t.click("Sidebar")
        reg.t.click("Add Podcast")
        time.sleep(2)
        type(url + "\n")
        if exists("anyway",45):
            type(Key.ENTER)
        miro.click_last_podcast( reg)
        type(Key.DELETE)
        miro.remove_confirm(reg, "remove")
        #Reset autodownload preferences
        miro.open_prefs(reg)
        prefs.open_tab("Podcasts")
        prefs.autodownload_setting("Off")
        prefs.close_prefs()
        del prefs

        

if __name__ == "__main__":
    import LitmusTestRunner
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv, ).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite, ).litmus_test_run()


