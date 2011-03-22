import sys
import os
import glob
import unittest
import StringIO
import time


sys.path.append(os.path.join(os.getcwd(),'myLib'))


import config
import mirolib
import testvars
import litmusresult



setBundlePath(config.get_img_path())


class Miro_Suite(unittest.TestCase):
    """Subgroup 16 - one-click subscribe tests.

    """
    def setUp(self):
        self.verificationErrors = []
        setAutoWaitTimeout(60)
         


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

        metadata = {"title":"Video",
                    "description":"This",
                    "icon":testvars.tv_icon,
                    "size":"842 B"}
        
        
        #1. add feed
        mirolib.add_feed(self,t,s,reg.mtb,url,feed)
        #2. search
        mirolib.tab_search(self,m,s,term)
        #3. verify item metadata
        #4. cleanup
        mirolib.delete_feed(self,m,s,feed)

    def stest_75(self):
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
            mirolib.add_feed(self,t,s,reg.mtb,url,feed)
            #2. search
            mirolib.tab_search(self,m,s,term)
            
            #3. verify item metadata
            self.assertTrue(reg.m.exists(title))
            self.assertTrue(reg.m.exists("This is the third test video"))
            self.assertTrue(reg.m.exists("http://participatoryculture.org/feeds_test/mike_tv_drawing_cropped.jpg"))
            self.assertTrue(reg.m.exists("842 B"))

            #verify the links
            LINKS = {"absolute link": "http://www.google.com", "relative link": "appcast.xml","another relative": "index.php" }
            for link, linkurl in LINKS.iteritems():
                if reg.m.exists(link):
                    click(m.getLastMatch())
                    App.open("Firefox")
                    mirolib.shortcut("l")
                    try:
                        self.assertEqual(Env.getClipboard(),link)
                    except:
                        self.verificationErrors.append("relative link not opened in browser")
        #cleanup
        finally:
            mirolib.delete_feed(self,m,s,feed)
 
    def stest_60(self):
        """http://litmus.pculture.org/show_test.cgi?id=60  Feed with no enclosures.

        1. Feed 3
        2. Verify Metadata
        3. Cleanup

        """
        reg = mirolib.AppRegions()
        m.highlight(3)
        reg.mtb.highlight(3)
        s.highlight(3)
        
        
        #1. add feed
        url = "http://pculture.org/feeds_test/no-enclosures.rss"
        feed = "Yahoo"
        term = "first test video"
        title = "Video 1"
        
        #1. add feed
        mirolib.add_feed(self,t,s,reg.mtb,url,feed)
        mirolib.download_all_items(self,m)
        #2. search
        
        #3. verify item metadata
        self.assertTrue(reg.m.exists(title))
        self.assertTrue(reg.m.exists("This is the first test video"))
        self.assertTrue(reg.m.exists("http://participatoryculture.org/feeds_test/mike_tv_drawing_cropped.jpg"))
        self.assertTrue(reg.m.exists("842 B"))

        mirolib.tab_search(self,m,s,"Video 2",confirm_present=False)
        self.assertFalse(reg.m.exists("Video 2",1))
        #cleanup
        mirolib.delete_feed(self,m,s,feed)

    def stest_73(self):
        """http://litmus.pculture.org/show_test.cgi?id=73 Feed with Yahoo and RSS enclosures.

        1. Feed 3
        2. Verify Metadata
        3. Cleanup

        """
        reg = mirolib.AppRegions()
        
        url = "http://pculture.org/feeds_test/feed3.rss"
        feed = "RSS 2.0 and Yahoo"
        term = "first test video"
        title = "Video 1"
        
        #1. add feed
        mirolib.add_feed(self,t,s,reg.mtb,url,feed)
        #2. search
        mirolib.tab_search(self,m,s,term)
        
        #3. verify item metadata
        self.assertTrue(reg.m.exists(title))
        self.assertTrue(reg.m.exists("This is the first test video"))
        self.assertTrue(reg.m.exists("http://participatoryculture.org/feeds_test/mike_tv_drawing_cropped.jpg"))
        self.assertTrue(reg.m.exists("842 B"))
        #cleanup
        mirolib.delete_feed(self,m,s,feed)

    def stest_69(self):
        """http://litmus.pculture.org/show_test.cgi?id=69 Add rss feed via browser.

        1. Add feed The AV Club via the browser (assumes the browser is set to automatically add the feed).
        2. Verify the feed is added
        3. Cleanup

        """
        
        reg = mirolib.AppRegions()
        
        feed = "The AV Club"
        print "open ff"
        App.open(mirolib.open_ff())
        find(testvars.ffhome)
        App.focus("Firefox")
        url = "http://feeds.feedburner.com/theavclub/AVClubPresents?format=xml"
        mirolib.shortcut("l")
        time.sleep(2)
        type(url + "\n")

        #3. verify item metadata
        self.assertTrue(reg.s.exists(feed))
        #cleanup
        mirolib.delete_feed(self,m,s,feed) 
 
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
