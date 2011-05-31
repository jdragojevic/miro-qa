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
import prefs
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
        feed = "EEVblog"
        feed2 = "TED"
        click(testvars.guide_search)
        type(feed2 +"\n")
        time.sleep(5)
        reg.m.find("add_feed.png")
        click(reg.m.getLastMatch())
        mirolib.click_sidebar_tab(self,reg,"Miro")
        click(testvars.guide_search)
        type(feed + "\n")
        time.sleep(2)
        reg.m.find("add_feed.png")
        click(reg.m.getLastMatch())
        time.sleep(4)
        mirolib.click_last_podcast(self,reg)
        time.sleep(10)
    #2. Copy the url and attempt to add it
        reg.t.click("Sidebar")
        reg.t.click("Copy")
        url = Env.getClipboard()
        mirolib.add_feed(self,reg,url,feed)

        #3. Verify feed not duplicated
        p = mirolib.get_podcasts_region(reg)
        time.sleep(2)
        mirolib.count_images(self,reg, img=feed,region="sidebar",num_expected=1)
        mirolib.delete_feed(self,reg,feed)
        mirolib.delete_feed(self,reg,feed2)
        
        
        
    def test_138(self): #shortened as there no more feed counter and can't count too much stuff.
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
        mirolib.get_podcasts_region(reg)
        mirolib.toggle_list(reg)
        mirolib.tab_search(self,reg,"my feed")
        
        mirolib.count_images(self,reg,img="my feed",region="list",num_expected=5)
        mirolib.click_podcast(self,reg,feed)
        mirolib.shortcut("r")
        time.sleep(10)
        mirolib.get_podcasts_region(reg)
        mirolib.count_images(self,reg,img="my feed",region="list",num_expected=10)
        mirolib.click_podcast(self,reg,feed)
        for x in range(0,3):
            mirolib.shortcut("r")
            time.sleep(3)
        mirolib.open_podcast_settings(self,reg)
        mirolib.change_podcast_settings(self,reg,option="Podcast Items",setting="Keep 0")
        time.sleep(2)
        mirolib.get_podcasts_region(reg)
        mirolib.count_images(self,reg,img="my feed",region="list",num_expected=5)
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
    	time.sleep(3)
    	mirolib.toggle_normal(reg)
#    	mirolib.count_images(self,reg, "item-context-button.png",region="mainright",num_expected=2)
    	mirolib.set_podcast_autodownload(self,reg,setting="All")
    	mirolib.wait_for_item_in_tab(self,reg,"videos","Flip")
    	mirolib.wait_for_item_in_tab(self,reg,"videos","Dinosaur")
    	mirolib.click_podcast(self,reg,feed)
    	type(Key.DELETE)
    	mirolib.remove_confirm(self,reg,action="keep")
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
        mirolib.add_feed(self,reg,url,feed)
        mirolib.download_all_items(self,reg)
        mirolib.confirm_download_started(self,reg,"Joo Joo")
        mirolib.delete_feed(self,reg,feed)
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
        setAutoWaitTimeout(testvars.timeout)
        #set the search regions
        reg = mirolib.AppRegions()
        mirolib.click_sidebar_tab(self,reg,"Music")
        prefs.set_autodownload(self,reg,setting="Off")

        url = "http://pculture.org/feeds_test/list-of-guide-feeds.xml"
        feed = "Static"
        feedlist = ["America", "Earth"]

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
        mirolib.remove_confirm(self,reg,"cancel")
        p = mirolib.get_podcasts_region(reg)
        time.sleep(5)
        self.assertTrue(p.exists("Static",5))
        #4. Cleanup
        feedlist.append("Static")
        for x in feedlist:
            print x
            mirolib.delete_feed(self,reg,x)



    def skiptest_120(self): ## No feed counter, this test is no longer valid.
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
                 "recent posts": "http://blip.tv/rss?pagelen=1",
                 }

        #1. Add the feeds and check num items
        for feed, url in FEEDS.iteritems():
            mirolib.add_feed(self,reg,url,feed)
            
        #2. Select them and add to a folder    
        try:
            reg.s.click("my feed")
            time.sleep(2)
            keyDown(Key.SHIFT)
            reg.s.click("recent posts")
            self.assertTrue(reg.m.exists("Delete"))
            self.assertTrue(reg.m.exists("New Folder"))
        except:
            self.verificationErrors.append("multi select failed")
        finally:
            keyUp(Key.SHIFT)
        #3. Delete then cancel.  Verify still exists Static List
        reg.m.click("New Folder")
        time.sleep(2)
        type("Counter Test \n")
        mirolib.click_feed(self,reg,feed="Counter Test")
        mirolib.toggle_list(reg)
        mirolib.count_images(self,reg,img="Download",region="main",num_expected=6)
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


