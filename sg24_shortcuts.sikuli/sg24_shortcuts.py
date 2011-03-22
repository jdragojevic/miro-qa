import sys
import os
import glob
import unittest
import StringIO
import time

mycwd = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro")
sys.path.append(os.path.join(mycwd,'myLib'))
import config
import mirolib
import testvars
import litmusresult



setBundlePath(config.get_img_path())


class Miro_Suite(unittest.TestCase):
    """Subgroup 41 - one-click subscribe tests.

    """
    def setUp(self):
        self.verificationErrors = []
        setAutoWaitTimeout(60)
         


    def test_92(self):
        """http://litmus.pculture.org/show_test.cgi?id=361 edit item audio to video.

        1. add 3-blip-videos feed
        2. download the Joo Joo
        3. Edit item from Video to Audio
        4. Verify item played as audio item

        """
        miroRegions = mirolib.launch_miro()
        s = miroRegions[0] #Sidebar Region
        m = miroRegions[1] #Mainview Region
        t = miroRegions[2] #top half screen
        tl = miroRegions[3] #top left quarter

        # Add a feed and delete it with keyboard shortcut
        try:
            feed_url = "http://www.stupidvideos.com/rss/rss.php?chart=new&format=yahoo"
            feed_name = "StupidVideo"
            mirolib.shortcut("n")
            type(feed_url+"\n")
            reg.s.click(feed_name)
            mirolib.delete_feed(self,m,s,feed_name)
        except:
            self.verificationErrors.append("delete feed failed")
    
        # Add site - and delete using shortcut key
        try:
            site_url =  "http://blip.tv"
            site = "Blip.tv"
            mirolib.add_website(self,m,s,site_url,site)
            mirolib.delete_site(self,m,s,site)
        except:
            self.verificationErrors.append("delete site failed")
            
        #Download item and with shortcut key, delete item
        try:
            item_url =  "http://www.boatingsidekicks.com/fish-detective.swf"
            item_title = "fish"
            reg.s.click("File")
            reg.s.click("Download")
            type(item_url+"\n")
            mirolib.wait_download_complete(self,m,s,item_title)
            mirolib.delete_items(self,m,s,item_title,"Other")
        except:
            self.verificationErrors.append("delete item failed")

        # remove playlist
        try:
            mirolib.shortcut("p")
            type("Testlist"+"\n")
            reg.s.find("Testlist")
            reg.s.click("Testlist")
            time.sleep(2)
            type(Key.DELETE)
            mslib.remove_confirm(self,m,action="remove")
            self.assertFalse(reg.s.exists("Testlist",5))
        except:
            self.verificationErrors.append("delete playlist failed")

        # remove playlist folder
        try:
            shortcut("p",shift=True)
            type("Playlist-Folder"+"\n")
            reg.s.find("Playlist-Folder")
            reg.s.click("Playlit-Folder")
            time.sleep(2)
            type(Key.DELETE)
            mslib.remove_confirm(self,m,action="remove")
            self.assertFalse(reg.s.exists("Playlist-Folder",5))
        except:
            self.verificationErrors.append("delete playlist folder failed")

 
    def tearDown(self):
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
