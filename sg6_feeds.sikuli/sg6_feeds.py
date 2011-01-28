import sys
import os
import glob
import unittest
import StringIO
import time

mycwd = os.path.join(os.getenv("SIKULI_TEST_HOME"),"Miro")
sys.path.append(os.path.join(mycwd,'myLib'))
import config
import mirolib
import testvars
import litmusresult

setBundlePath(config.get_img_path())


class Miro_Suite(unittest.TestCase):
    """Subgroup 6 - Feeds tests.

    """
    def setUp(self):
        self.verificationErrors = []

    def test_123(self):
        """http://litmus.pculture.org/show_test.cgi?id=123 add feed more than once.

        Litmus Test Title:: 123 - add a channel more than once  
        Description: 
         1. Add a channel from the Miro Guide.  
         2. Copy the URL and use the Add Feed dialog to add it.  
         3. Verify feed not duplicated.
         4. Cleanup
        """
        setAutoWaitTimeout(testvars.timeout)
        
        #set the search regions
        miroRegions = mirolib.launch_miro()
        s = miroRegions[0] #Sidebar Region
        m = miroRegions[1] #Mainview Region
        t = miroRegions[2] #top half screen
        tl = miroRegions[3] #top left quarter
        mtb = miroRegions[4] #main title bar
        
        m.click(testvars.guide_search)
        type("stupidvideos.com - the stupid review \n")
        m.find(testvars.guide_add_feed)
        click(m.getLastMatch())
        self.assertTrue(s.exists("StupidVideos"))
        click(s.getLastMatch())
        mtb.find("Stupid")
        #2. Copy the url and attempt to add it
        t.click("File")
        t.click("Copy")
        t.click("File")
        t.click("Add Feed")
        m.find("stupidvideos.com")
        type("\n")
        time.sleep(5)
        #3. Verify feed not duplicated
        fl = s.findall("StupidVideos")
        self.assertTrue(len(fl) == 1)       
        #4. cleanup
        mirolib.delete_feed(self,m,s,"StupidVideos")
        
        
    def test_138(self):
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
        miroRegions = mirolib.launch_miro()
        s = miroRegions[0] #Sidebar Region
        m = miroRegions[1] #Mainview Region
        t = miroRegions[2] #top half screen
        tl = miroRegions[3] #top left quarter
        mtb = miroRegions[4] #main title bar
        
        url = "http://bluesock.org/~willg/cgi-bin/newitemsfeed.cgi"
        feed = "my feed"
        mirolib.add_feed(self,t,s,mtb,url,feed)
        tmpr = Region(mtb.below(30))
        self.assertTrue(tmpr.exists("5 Items"))
        mirolib.shortcut("r")
        tmpr.find("10 Items",5)
        #Set feed setting to 100 and update to verify items kept to limit
        mtb.click("Settings")
        m.click("Keep")
        m.click("100")
        type("\n")
        for x in range(0,25):
            mirolib.shortcut("r")
            time.sleep(3)
        self.assertTrue(tmpr.exists("105 Items"))
        #Set feed setting to 20 (Default) and verify items kept to limit
        mtb.click("Settings")
        m.click("Keep")
        m.click("(Default)")
        m.click("Remove All")
        type("\n")
        self.assertTrue(tmpr.exists("25 Items",5))
        #Set feed setting to 0 and verify items kept to limit
        mtb.click("Settings")
        m.click("Keep")
        m.click("Keep 0")
        type("\n")
        self.assertTrue(tmpr.exists("5 Items",5))
        #4. cleanup
        mirolib.delete_feed(self,m,s,"my feed") 
   
    def test_339(self):
    	"""http://litmus.pculture.org/show_test.cgi?id=339 delete feed with dl items.

        Litmus Test Title:: 339 - channels delete a feed with downloaded items
        Description: 
        1. Add the 2-stupid-videos feed, abd download both items in the feed.  
        2. Remove Feed and Keep the videos.  
        3. Verify videos are displayed in the non-feed section of the Library
        4. Cleanup
        """

    	setAutoWaitTimeout(testvars.timeout)   
        #set the search regions
    	miroRegions = mirolib.launch_miro()
    	s = miroRegions[0] #Sidebar Region
    	m = miroRegions[1] #Mainview Region
    	t = miroRegions[2] #top half screen
    	tl = miroRegions[3] #top left quarter
    	mtb = miroRegions[4] #main title bar

    	url = "http://pculture.org/feeds_test/2stupidvideos.xml"
    	feed = "2-stupid-videos"

    	#1. Add the feed and start dl
    	mirolib.add_feed(self,t,s,mtb,url,feed)
    	tmpr = Region(mtb.below(30))
    	self.assertTrue(tmpr.exists("2 Items"))
    	badges = m.findAll("Download")
    	for x in badges:\
            m.click(x)
    	mirolib.wait_for_item_in_tab(self,m,s,"video","Flip")
    	mirolib.wait_for_item_in_tab(self,m,s,"video","Dinosaur")
    	s.click("feed")
    	type(Key.DELETE)
    	mirolib.remove_confirm(self,m,action="keep")
    	self.assertFalse(s.exists(feed))
    	mirolib.click_sidebar_tab(self,m,s,"video")
    	mirolib.tab_search(self,m,s,"Flip",confirm_present=True)
    	mirolib.tab_search(self,m,s,"Dinosaur",confirm_present=True)
    	#4. cleanup
    	mirolib.delete_items(self,m,s,"Flip","video")
    	mirolib.delete_items(self,m,s,"Dinosaur","video")

    def test_338(self):
        """http://litmus.pculture.org/show_test.cgi?id=338 delete feed with dl items.

        Litmus Test Title:: 338 - channels delete a feed with downloads in progress
        Description: 
        1. Add the 3-blip-videos feed. Start items downloading  
        2. Remove the feed and verify downloads are removed.
        """

        setAutoWaitTimeout(testvars.timeout)   
        #set the search regions
        miroRegions = mirolib.launch_miro()
        s = miroRegions[0] #Sidebar Region
        m = miroRegions[1] #Mainview Region
        t = miroRegions[2] #top half screen
        tl = miroRegions[3] #top left quarter
        mtb = miroRegions[4] #main title bar

        url = "http://pculture.org/feeds_test/3blipvideos.xml"
        feed = "3-blip-videos"

        #1. Add the feed and start dl
        mirolib.cancel_all_downloads(self,m,s,mtb)
        self.assertFalse(s.exists("Downloading",5)) #make sure no in progress downloads
        mirolib.add_feed(self,m,s,url,feed)
        tmpr = Region(mtb.below(30))
        self.assertTrue(tmpr.exists("3 Items"))
        badges = m.findAll("Download")
        for x in badges:
            click(x)
        mirolib.confirm_download_started(self,m,s,"Joo Joo")
        mirolib.delete_feed(self,m,s,"my feed")
        self.assertFalse(s.exists("Downloading",5))


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
        miroRegions = mirolib.launch_miro()
        s = miroRegions[0] #Sidebar Region
        m = miroRegions[1] #Mainview Region
        t = miroRegions[2] #top half screen
        tl = miroRegions[3] #top left quarter
        mtb = miroRegions[4] #main title bar

        url = "http://pculture.org/feeds_test/list-of-guide-feeds.xml"
        feed = "Static List"
        feedlist = ["TechVi", "Uploads by Gimp", "Brooklyn Museum", "LandlineTV"]

        #1. Add the feed and start dl
        mirolib.add_feed(self,m,s,url,feed)
        addlink = m.findAll("Add this channel")
        for x in addlink:
            click(x)
            time.sleep(4)
        #2. Select them all    
        try:
            keyDown(SHIFT_KEY)
            for x in feedlist:
                if s.exists(x):
                    s.click(x)
                else:
                    print "could not find feed" +str(x)
                time.sleep(2)
            self.assertTrue(m.exists("Delete"))
            self.assertTrue(m.exists("New Folder"))
        except:
            self.verificationErrors.append("multi select failed")
        finally:
            keyUp(SHIFT_KEY)
        #3. Delete then cancel.  Verify still exists Static List
        m.click("Delete")
        mirolib.remove_confirm(self,m,"cancel")
        mirolib.click_sidebar_tab(self,m,s,"video")
        self.assertTrue(s.exists("Static List",5))
        #4. Cleanup
        feedlist.append("Static")
        for x in feedlist:
            mirolib.delete_feed(self,m,s,x)

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
        miroRegions = mirolib.launch_miro()
        s = miroRegions[0] #Sidebar Region
        m = miroRegions[1] #Mainview Region
        t = miroRegions[2] #top half screen
        tl = miroRegions[3] #top left quarter
        mtb = miroRegions[4] #main title bar

        FEEDS = {"my feed": "http://bluesock.org/~willg/cgi-bin/newitemsfeed.cgi",
                 "recent posts": "http://blip.tv/rss?pagelen=10",
                 }

        #1. Add the feeds and check num items
        for feed, url in FEEDS.iteritems():
            mirolib.add_feed(self,m,s,url,feed)
            
        #2. Select them and add to a folder    
        try:
            s.click("my feed")
            time.sleep(2)
            keyDown(SHIFT_KEY)
            s.click("recent posts")
            self.assertTrue(m.exists("Delete"))
            self.assertTrue(m.exists("New Folder"))
        except:
            self.verificationErrors.append("multi select failed")
        finally:
            keyUp(SHIFT_KEY)
        #3. Delete then cancel.  Verify still exists Static List
        m.click("New Folder")
        time.sleep(2)
        type("Counter Test \n")
        s.click("Counter Test")
        tmpr = Region(mtb.below(30))
        self.assertTrue(tmpr.exists("15 Items"))
        mirolib.shortcut("r",shift=True)
        time.sleep(3)
        self.assertTrue(tmpr.exists("20 Items"))
        #4. Cleanup
        type(Key.DELETE)
        mirolib.remove_confirm(self,m,action="remove")
        
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
            litmusresult.write_log(id_string,stat,byte_output)
        finally:
            buf.truncate(0)
    litmusresult.write_footer()
#or just run it locally
else:
    unittest.main()

