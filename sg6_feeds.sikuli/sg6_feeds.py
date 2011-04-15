import sys
import os
import glob
import unittest
import StringIO
import time
from sikuli.Sikuli import *

mycwd = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro")
sys.path.append(os.path.join(mycwd,'myLib'))
import base_testcase
import config
import mirolib
import testvars

class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 6 - Feeds tests.

    """
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
        reg = mirolib.AppRegions()
        reg.mtb.click(testvars.guide_search)
        type("stupidvideos.com - the stupid review \n")
        reg.m.find(testvars.guide_add_feed)
        click(reg.m.getLastMatch())
        p = mirolib.get_podcasts_region(reg)
        self.assertTrue(p.exists("StupidVideos"))
        click(p.getLastMatch())
        
        #2. Copy the url and attempt to add it
        reg.t.click("Sidebar")
        reg.t.click("Copy")
        reg.t.click("Sidebar")
        reg.t.click("Add Podcast")
        time.sleep(2)
        type("\n")
        time.sleep(3)
        #3. Verify feed not duplicated
        p = mirolib.get_podcasts_region(reg)
        time.sleep(2)
        mirolib.count_images(self,reg, "StupidVideos",region="sidebar",num_expected=1)
        mirolib.delete_feed(self,reg,"StupidVideos")
        
        
    def skip_test_138(self): #revisit this when item count is back or out, or update to feed with 1 item.
        """http://litmus.pculture.org/show_test.cgi?id=138 clear out old items.

        Litmus Test Title:: 138 Channels - clear out old items 
        Description: 
         1. Add a feed that adds five new items each time it's updated.
         2. Update the feed to add new items.
         3. Modify old items settings to verify items cleared.
         4. Cleanup

        """
        setAutoWaitTimeout(testvars.timeout)
        
        #set the search regions
        reg = mirolib.AppRegions()        
        url = "http://bluesock.org/~willg/cgi-bin/newitemsfeed.cgi"
        feed = "my feed"
        mirolib.add_feed(self,reg,url,feed)
        tmpr = Region(reg.mtb.below(30))
        self.assertTrue(tmpr.exists("5 Items"))
        mirolib.shortcut("r")
        tmpr.find("10 Items",5)
        #Set feed setting to 100 and update to verify items kept to limit
        reg.mtb.click("Settings")
        reg.m.click("Keep")
        reg.m.click("100")
        type("\n")
        for x in range(0,25):
            mirolib.shortcut("r")
            time.sleep(3)
        self.assertTrue(tmpr.exists("105 Items"))
        #Set feed setting to 20 (Default) and verify items kept to limit
        reg.mtb.click("Settings")
        reg.m.click("Keep")
        reg.m.click("(Default)")
        reg.m.click("Remove All")
        type("\n")
        self.assertTrue(tmpr.exists("25 Items",5))
        #Set feed setting to 0 and verify items kept to limit
        reg.mtb.click("Settings")
        reg.m.click("Keep")
        reg.m.click("Keep 0")
        type("\n")
        self.assertTrue(tmpr.exists("5 Items",5))
        #4. cleanup
        mirolib.delete_feed(self,reg,"my feed") 
   
    def test_339(self):
    	"""http://litmus.pculture.org/show_test.cgi?id=339 delete feed with dl items.

        Litmus Test Title:: 339 - channels delete a feed with downloaded items
        Description: 
        1. Add the 2-stupid-videos feed, and download both items in the feed.  
        2. Remove Feed and Keep the videos.  
        3. Verify videos are displayed in the non-feed section of the Library
        4. Cleanup
        """

    	setAutoWaitTimeout(testvars.timeout)   
        #set the search regions
    	reg = mirolib.AppRegions()

    	url = "http://pculture.org/feeds_test/2stupidvideos.xml"
    	feed = "TwoStupid"

    	#1. Add the feed and start dl
    	mirolib.add_feed(self,reg,url,feed)
    	mirolib.count_images(self,reg, "item-context-button.png",region="mainright",num_expected=2)
    	badges = reg.m.findAll("button_download.png")
    	for x in badges:\
            reg.m.click(x)
    	mirolib.wait_for_item_in_tab(self,reg,"videos","Flip")
    	mirolib.wait_for_item_in_tab(self,reg,"videos","Dinosaur")
    	reg.s.click(feed)
    	type(Key.DELETE)
    	mirolib.remove_confirm(self,reg,action="keep")
    	self.assertFalse(reg.s.exists(feed))
    	mirolib.click_sidebar_tab(self,reg,"videos")
    	mirolib.tab_search(self,reg,"Flip",confirm_present=True)
    	mirolib.tab_search(self,reg,"Dinosaur",confirm_present=True)
    	#4. cleanup
    	mirolib.delete_items(self,reg,"Flip","videos")
    	mirolib.delete_items(self,reg,"Dinosaur","videos")

    def test_338(self):
        """http://litmus.pculture.org/show_test.cgi?id=338 delete feed with dl items.

        Litmus Test Title:: 338 - channels delete a feed with downloads in progress
        Description: 
        1. Add the 3-blip-videos feed. Start items downloading  
        2. Remove the feed and verify downloads are removed.
        """

        setAutoWaitTimeout(testvars.timeout)   
        #set the search regions
        reg = mirolib.AppRegions()

        url = "http://pculture.org/feeds_test/3blipvideos.xml"
        feed = "ThreeBlip"

        #1. Add the feed and start dl
        mirolib.cancel_all_downloads(self,reg)
        self.assertFalse(reg.s.exists("Downloading",5)) #make sure no in progress downloads
        mirolib.add_feed(self,reg,url,feed)
        tmpr = Region(reg.mtb.below(30))
        
        self.assertTrue(tmpr.exists("3 Items"))
        mirolib.download_all_items(self,reg)
        mirolib.confirm_download_started(self,reg,"Joo Joo")
        mirolib.delete_feed(self,reg,"my feed")
        self.assertFalse(reg.s.exists("Downloading",5))


    def test_117(self):
        """http://litmus.pculture.org/show_test.cgi?id=117 delete multiple feeds then cancel.

        Litmus Test Title:: 117 - delete multiple feeds then cancel
        Description: 
        1. Add several feeds from list of guide feeds
        2. Select them all
        3. Delete, the cancel the delete
        4. Cleanup
        """
        setAutoWaitTimeout(testvars.timeout)
        #set the search regions
        reg = mirolib.AppRegions()

        url = "http://pculture.org/feeds_test/list-of-guide-feeds.xml"
        feed = "Static"
        feedlist = ["Help", "Film", "Earth"]

        #1. Add the feed and start dl
        mirolib.add_feed(self,reg,url,feed)
        for f in feedlist:
            mirolib.tab_search(self,reg,f)
            self.assertTrue(reg.m.exists("Add this"))
            reg.m.click("Add this")
            time.sleep(4)
        mirolib.tab_search(self,reg,"")

        p = mirolib.get_podcasts_region(reg)
        mirolib.click_sidebar_tab(self,reg,"Music")
        mirolib.click_podcast(self,reg,feed)
##        addlink = reg.m.findAll("Add this")
##        for x in addlink:
##            click(x)
##            time.sleep(4)
            
        #2. Select them all
        try:
            keyDown(Key.SHIFT)
        
            for x in feedlist:
                if p.exists(x):
                    p.click(x)
                else:
                    print "could not find feed" +str(x)
                time.sleep(2)
            self.assertTrue(reg.m.exists("button_mv_delete_all.png"))
            self.assertTrue(reg.m.exists("New Folder"))
        except:
            self.verificationErrors.append("multi select failed")
        finally:
            keyUp(Key.SHIFT)
        #3. Delete then cancel.  Verify still exists Static List
        reg.m.click("button_mv_delete_all.png")
        mirolib.remove_confirm(self,reg,"cancel")
        p = mirolib.get_podcasts_region(reg)
        self.assertTrue(p.exists("Static",5))
        #4. Cleanup
        feedlist.append("Static")
        for x in feedlist:
            mirolib.delete_feed(self,reg,x)

    def test_120(self):
        """http://litmus.pculture.org/show_test.cgi?id=120 full feed counter.

        Litmus Test Title:: 120 full feed counter
        Description: 
        Verify full feed counter accurately displays the number of items in a feed or folder.
        1. Add 2 feeds and verify number of items
        2. Put them in a folder
        3. Update and verify counter
        4. Cleanup
        """
        setAutoWaitTimeout(testvars.timeout)
        #set the search regions
        reg = mirolib.AppRegions()

        FEEDS = {"my feed": "http://bluesock.org/~willg/cgi-bin/newitemsfeed.cgi",
                 "recent posts": "http://blip.tv/rss?pagelen=10",
                 }

        #1. Add the feeds and check num items
        for feed, url in FEEDS.iteritems():
            mirolib.add_feed(self,reg,url,feed)
            
        #2. Select them and add to a folder    
        try:
            reg.s.click("my feed")
            time.sleep(2)
            keyDown(SHIFT_KEY)
            reg.s.click("recent posts")
            self.assertTrue(reg.m.exists("Delete"))
            self.assertTrue(reg.m.exists("New Folder"))
        except:
            self.verificationErrors.append("multi select failed")
        finally:
            keyUp(SHIFT_KEY)
        #3. Delete then cancel.  Verify still exists Static List
        reg.m.click("New Folder")
        time.sleep(2)
        type("Counter Test \n")
        reg.s.click("Counter Test")
        tmpr = Region(reg.mtb.below(30))
        self.assertTrue(tmpr.exists("15 Items"))
        mirolib.shortcut("r",shift=True)
        time.sleep(3)
        self.assertTrue(tmpr.exists("20 Items"))
        #4. Cleanup
        type(Key.DELETE)
        mirolib.remove_confirm(self,reg,action="remove")
        

if __name__ == "__main__":
    import LitmusTestRunner
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()


