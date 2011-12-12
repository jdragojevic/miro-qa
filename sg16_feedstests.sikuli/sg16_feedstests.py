from urlparse import urlsplit
import sys
import unittest
import time
from sikuli.Sikuli import *
import base_testcase
import myLib.config
from myLib.miro_regions import MiroRegions
from myLib.miro_app import MiroApp
from myLib.preferences_panel import PreferencesPanel



class Test_FeedsTests(base_testcase.Miro_unittest_testcase):
    """Subgroup 16 - Feeds tests.

    """
            
    def test_001setup(self):
        """fake test to reset db and preferences.

        """
        reg = MiroRegions()
        miro = MiroApp()
        
        miro.quit_miro()
        myLib.config.set_def_db_and_prefs()
        miro.restart_miro()
        time.sleep(10)
            


    def test_74(self):
        """http://litmus.pculture.org/show_test.cgi?id=74 Feed search, saved search feed

        1. Add feed1, RSS 2.0 with Yahoo enclosures
        2. Perform a search and save it.
        3. Verify Search saved
        4. Cleanup

        """
        reg = MiroRegions()
        miro = MiroApp()
        
        url = "http://pculture.org/feeds_test/feed1.rss"
        feed = "Yah"
        term = "first test video"
        title = "Video"

        reg = MiroRegions()
        miro = MiroApp()
        
        
        #1. add feed
        miro.add_feed(reg, url, feed)
        #2. search
        miro.tab_search(reg, term)
        #3. verify item metadata
        self.assertTrue(reg.m.exists(title))
        self.assertTrue(reg.m.exists("This is"))
#        self.assertTrue(reg.m.exists("mike_tv.png"))
    
        #4. cleanup
        miro.delete_feed(reg,feed)



    def test_75(self):
        """http://litmus.pculture.org/show_test.cgi?id=75 Absolute and relative links.
        1. Feed 1
        2. View videos 3
        3. Click the links and verify they are opened
        4. Cleanup

        """
        try:
            reg = MiroRegions()
            miro = MiroApp()
        
            
            #1. add feed
            url = "http://pculture.org/feeds_test/feed1.rss"
            feed = "Yah"
            term = "third test video"
            title = "Video 3"
            
            #1. add feed
            miro.add_feed(reg, url, feed)
            #2. search
            miro.tab_search(reg, term)
            
            #3. verify item metadata
            self.assertTrue(reg.m.exists(title))
            #verify the links
            LINKS = {"absolute link": "google", "relative link": "orim_avatar","another relative": "pculture" }
            for link, linkurl in LINKS.iteritems():
                if reg.m.exists(link):
                    click(reg.m.getLastMatch())
                    time.sleep(15)
                    miro.shortcut("l")
                    time.sleep(2)
                    miro.shortcut("c")
                    time.sleep(2)
                    url = Env.getClipboard()
                    print url
                    miro.shortcut('q')
                    time.sleep(2)
                    baseurl = urlsplit(url).netloc
                    url_parts = baseurl.split('.')
                    self.failUnless(linkurl in url_parts)            
        #cleanup
        finally:
            miro.close_ff
            miro.delete_feed(reg, feed)
            
 
    def test_60(self):
        """http://litmus.pculture.org/show_test.cgi?id=60  Feed with no enclosures.

        1. Feed 3
        2. Verify Metadata
        3. Cleanup

        """
        #1. add feed
        url = "http://pculture.org/feeds_test/no-enclosures.rss"
        feed = "Yah"
        term = "first test video"
        title = "Video 1"

        reg = MiroRegions()
        miro = MiroApp()
        
        #1. add feed
        miro.add_feed(reg, url, feed)
        #2. search
        
        #3. verify item metadata
        self.assertTrue(reg.m.exists(title))
        self.assertTrue(reg.m.exists("This is")) #Description text

        miro.tab_search(reg, "Video 2", confirm_present=False)
        if reg.m.exists("second test",1):
            self.fail("video 2 found")
        #cleanup
        miro.delete_feed(reg, feed)
        

    def test_73(self):
        """http://litmus.pculture.org/show_test.cgi?id=73 Feed with Yahoo and RSS enclosures.

        1. Feed 3
        2. Verify Metadata
        3. Cleanup

        """
        try:
            reg = MiroRegions()
            miro = MiroApp()
        
            url = "http://pculture.org/feeds_test/feed3.rss"
            feed = "RSS 2"
            term = "first test video"
            title = "Video 1"
            
            #1. add feed
            miro.add_feed(reg, url, feed)
            #2. search
            miro.tab_search(reg, term)
            
            #3. verify item metadata
            self.assertTrue(reg.m.exists(title))
            self.assertTrue(reg.m.exists("This is"))
            self.assertTrue(reg.m.exists("mike_tv.png"))
       
        finally:#cleanup
            miro.delete_feed(reg, feed)
            

    def test_69(self):
        """http://litmus.pculture.org/show_test.cgi?id=69 Add rss feed via browser.

        1. Add feed The AV Club via the browser (assumes the browser is set to automatically add the feed).
        2. Verify the feed is added
        3. Cleanup

        Assumes that Miro is myLib.config.red as the default application to open rss feeds in FF.
        
        """

        reg = MiroRegions()
        miro = MiroApp()        
        feed = "AV Club"
        
        #SET GLOBAL PREFERENCES
        miro.open_prefs(reg)
        prefs = PreferencesPanel()
        podcasts_tab = prefs.open_tab("Podcasts")
        podcasts_tab.autodownload_setting("Off")
        podcasts_tab.close_prefs()
        
        url = "http://feeds.feedburner.com/theavclub/mainline"
        miro.browser_to_miro(reg, url)
        #3. verify feed added
        miro.click_podcast(reg, feed)
        #4. Cleanup
        miro.delete_feed(reg, feed) 


    def test_726(self):
        """http://litmus.pculture.org/show_test.cgi?id=726 Feed with gzipped enclosures.

        1. Add feeds
        2. verify items are displayed
        3. Verify items are downloadable
        4. Cleanup

        """
        reg = MiroRegions()
        miro = MiroApp()

        ZIPPED_FEEDS = [
            #["http://podcastle.org/feed/rss2","PodCastle",],
            ["http://escapepod.org/feed/","Escape","EP"],
            ["http://pseudopod.org/feed/rss2","Pseudopod","Pseudopod"],
            ]
        for url,feed,item_id in ZIPPED_FEEDS:
           #1. add feed
            miro.add_feed(reg, url, feed)
            #2 verify items displayed
            if reg.m.exists(Pattern("button_download.png"),3):
                click(reg.m.getLastMatch())
            else:
                self.fail("download button not found, no items displayed?")
            #3. verify download started
            status = miro.confirm_download_started(reg, item_id)
            if status == "in_progress":
                miro.log_result("726","verified for feed: "+feed)
            else:
                self.verificationErrors.append("failed for feed: "+feed)
            #4. Cleanup
            miro.delete_feed(reg, feed)

 
    def test_999reset(self):
        """fake test to reset db and preferences.

        """
        reg = MiroRegions()
        miro = MiroApp()
        miro.quit_miro()
        myLib.config.set_def_db_and_prefs()
        miro.restart_miro()
        
        

# TestRunner posts output in xunit format
if __name__ == "__main__":
    from TestRunner import TestRunner
    TestRunner(Test_FeedsTests).run_tests()

