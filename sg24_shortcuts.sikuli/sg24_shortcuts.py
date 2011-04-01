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
import testvars
import base_testcase


class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 41 - one-click subscribe tests.

    """

    def test_92(self):
        """http://litmus.pculture.org/show_test.cgi?id=361 edit item audio to video.

        1. add 3-blip-videos feed
        2. download the Joo Joo
        3. Edit item from Video to Audio
        4. Verify item played as audio item

        """
        reg = mirolib.AppRegions()
        try:
            feed_url = "http://www.stupidvideos.com/rss/rss.php?chart=new&format=yahoo"
            feed_name = "StupidVideo"
            mirolib.shortcut("n")
            type(feed_url+"\n")
            reg.s.click(feed_name)
            mirolib.delete_feed(self,reg,feed_name)
        except:
            self.verificationErrors.append("delete feed failed")
    
        # Add site - and delete using shortcut key
        try:
            site_url =  "http://blip.tv"
            site = "Blip.tv"
            mirolib.add_website(self,reg,site_url,site)
            mirolib.delete_site(self,reg,site)
        except:
            self.verificationErrors.append("delete site failed")
            
        #Download item and with shortcut key, delete item
        try:
            item_url =  "http://www.boatingsidekicks.com/fish-detective.swf"
            item_title = "fish"
            reg.s.click("File")
            reg.s.click("Download")
            type(item_url+"\n")
            mirolib.wait_download_complete(self,reg,item_title)
            mirolib.delete_items(self,reg,item_title,"Other")
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
            mslib.remove_confirm(self,reg,action="remove")
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
            mslib.remove_confirm(self,reg,action="remove")
            self.assertFalse(reg.s.exists("Playlist-Folder",5))
        except:
            self.verificationErrors.append("delete playlist folder failed")

 
   
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()
   

