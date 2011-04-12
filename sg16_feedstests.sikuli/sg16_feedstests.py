import sys
import os
import glob
import unittest
import StringIO
import time
from sikuli.Sikuli import *

sys.path.append(os.path.join(os.getcwd(),'myLib'))
import config
import mirolib
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

    def test_175(self):
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
            self.assertTrue(reg.m.exists("This is"))
            self.assertTrue(reg.m.exists("mike_tv.png"))
            self.assertTrue(reg.m.exists("842 KB"))

            #verify the links
            LINKS = {"absolute link": "http://www.google.com", "relative link": "appcast.xml","another relative": "index.php" }
            for link, linkurl in LINKS.iteritems():
                if reg.m.exists(link):
                    click(reg.m.getLastMatch())
                    App.open("Firefox")
                    time.sleep(20)
                    mirolib.shortcut("l")
                    try:
                        self.assertEqual(Env.getClipboard(),linkurl)
                    except:
                        self.verificationErrors.append("relative link not opened in browser")
                    mirolib.shortcut("w")
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
        self.assertTrue(reg.m.exists("842 KB"))

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

    def test_69(self):
        """http://litmus.pculture.org/show_test.cgi?id=69 Add rss feed via browser.

        1. Add feed The AV Club via the browser (assumes the browser is set to automatically add the feed).
        2. Verify the feed is added
        3. Cleanup

        Assumes that Miro is configured as the default application to open rss feeds in FF.
        
        """
        
        reg = mirolib.AppRegions()
        
        feed = "The AV"
        print "open ff"
        App.open(mirolib.open_ff())
        time.sleep(2)
        url = "http://feeds.feedburner.com/theavclub/AVClubPresents?format=xml"
        mirolib.shortcut("l")
        time.sleep(2)
        type(url + "\n")
        time.sleep(5)
        mirolib.shortcut('w')
        reg = mirolib.AppRegions()
        #3. verify item metadata
        mirolib.click_podcast(self,reg,feed)
        #cleanup
        mirolib.delete_feed(self,reg,feed) 
 
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()
   

