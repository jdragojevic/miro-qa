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
import prefs
import testvars
import base_testcase

class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 16 - one-click subscribe tests.

    """

    

    def test_74(self):
        """http://litmus.pculture.org/show_test.cgi?id=74 Feed search, saved search feed

        1. Add feed1, RSS 2.0 with Yahoo enclosures
        2. Perform a search and save it.
        3. Verify Search saved
        4. Cleanup

        """
        reg = mirolib.AppRegions()
        
        url = "http://pculture.org/feeds_test/feed1.rss"
        feed = "Yahoo"
        term = "first test video"
        title = "Video"
       
        
        #1. add feed
        mirolib.add_feed(self,reg,url,feed)
        #2. search
        mirolib.tab_search(self,reg,term)
        #3. verify item metadata
        self.assertTrue(reg.m.exists(title))
        self.assertTrue(reg.m.exists("This is"))
        self.assertTrue(reg.m.exists("mike_tv.png"))
        self.assertTrue(reg.m.exists("842 KB"))
        #4. cleanup
        mirolib.delete_feed(self,reg,feed)

    def test_75(self):
        """http://litmus.pculture.org/show_test.cgi?id=75 Absolute and relative links.

        1. Feed 1
        2. View videos 3
        3. Click the links and verify they are opened
        4. Cleanup

        """
        try:
            reg = mirolib.AppRegions()
            
            #1. add feed
            url = "http://pculture.org/feeds_test/feed1.rss"
            feed = "Yahoo"
            term = "third test video"
            title = "Video 3"
            
            #1. add feed
            mirolib.add_feed(self,reg,url,feed)
            #2. search
            mirolib.tab_search(self,reg,term)
            
            #3. verify item metadata
            self.assertTrue(reg.m.exists(title))
##            self.assertTrue(reg.m.exists("This is"))
##            self.assertTrue(reg.m.exists("mike_tv.png"))
##            self.assertTrue(reg.m.exists("842 KB"))

            #verify the links
            LINKS = {"absolute link": "google", "relative link": "feeds_test","another relative": "pculture.org" }
            for link, linkurl in LINKS.iteritems():
                if reg.m.exists(link):
                    print link
                    click(reg.m.getLastMatch())
                    time.sleep(15)
                    mirolib.shortcut("l")
                    time.sleep(1)
                    mirolib.shortcut("c")
                    time.sleep(1)
                    print Env.getClipboard()
                    url = Env.getClipboard()
                    print linkurl
                    self.failUnless(linkurl in url)
                    mirolib.shortcut("q")
                    time.sleep(1)
        #cleanup
        finally:
            mirolib.delete_feed(self,reg,feed)
 
    def test_60(self):
        """http://litmus.pculture.org/show_test.cgi?id=60  Feed with no enclosures.

        1. Feed 3
        2. Verify Metadata
        3. Cleanup

        """
        reg = mirolib.AppRegions()        
        
        #1. add feed
        url = "http://pculture.org/feeds_test/no-enclosures.rss"
        feed = "Yahoo"
        term = "first test video"
        title = "Video 1"
        
        #1. add feed
        mirolib.add_feed(self,reg,url,feed)
        mirolib.download_all_items(self,reg)
        #2. search
        
        #3. verify item metadata
        self.assertTrue(reg.m.exists(title))
        self.assertTrue(reg.m.exists("This is")) #Description text
        self.assertTrue(reg.m.exists("mike_tv.png"))

        mirolib.tab_search(self,reg,"Video 2",confirm_present=False)
        self.assertFalse(reg.m.exists("Video 2",1))
        #cleanup
        mirolib.delete_feed(self,reg,feed)

    def test_73(self):
        """http://litmus.pculture.org/show_test.cgi?id=73 Feed with Yahoo and RSS enclosures.

        1. Feed 3
        2. Verify Metadata
        3. Cleanup

        """
        reg = mirolib.AppRegions()
        
        url = "http://pculture.org/feeds_test/feed3.rss"
        feed = "RSS 2"
        term = "first test video"
        title = "Video 1"
        
        #1. add feed
        mirolib.add_feed(self,reg,url,feed)
        #2. search
        mirolib.tab_search(self,reg,term)
        
        #3. verify item metadata
        self.assertTrue(reg.m.exists(title))
        self.assertTrue(reg.m.exists("This is"))
        self.assertTrue(reg.m.exists("mike_tv.png"))
        self.assertTrue(reg.m.exists("842 KB"))
        #cleanup
        mirolib.delete_feed(self,reg,feed)

    def test_1169(self):
        """http://litmus.pculture.org/show_test.cgi?id=69 Add rss feed via browser.

        1. Add feed The AV Club via the browser (assumes the browser is set to automatically add the feed).
        2. Verify the feed is added
        3. Cleanup

        Assumes that Miro is configured as the default application to open rss feeds in FF.
        
        """
        
        reg = mirolib.AppRegions()
        prefs.set_autodownload(self,reg,setting="Off")
        feed = "The AV"
        print "open ff"
        App.open(mirolib.open_ff())
        time.sleep(20)
        url = "http://feeds.feedburner.com/theavclub/mainline"
        mirolib.shortcut("l")
        time.sleep(2)
        type(url + "\n")
        time.sleep(10)
        mirolib.close_ff()
        #3. verify item metadata
        mirolib.click_podcast(self,reg,feed)
        #cleanup
        mirolib.delete_feed(self,reg,feed) 
 
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()
   

