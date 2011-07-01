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
        """http://litmus.pculture.org/show_test.cgi?id=92 delete shortcut.

        1. add a feed and delete
        2. add a site and delete
        3. download an item and delete
        4. Verify item played as audio item

        """
        reg = mirolib.AppRegions()

        #start the download of the misc file for later delete
        item_url =  "http://www.boatingsidekicks.com/fish-detective.swf"
        if config.get_os_name() == "osx":
            reg.tl.click("File")
        else:
            type('f',KEY_ALT)
        reg.t.click("Download")
        time.sleep(4)
        type(item_url+"\n")
        
        
        def _delete_feed(self):
            feed_url = "stupidvideos.com/rss/rss.php?chart=new&format=yahoo"
            feed = "StupidVid"
            mirolib.shortcut("n")
            if reg.m.exists("URL",3):
                mirolib.log_result("97","test_92")
            time.sleep(2)
            type(feed_url+"\n")
            time.sleep(4)
            mirolib.delete_feed(self,reg,feed)
            mirolib.log_result("92","delte feed shortcut verified")

        def _delete_feed_folder(self):
            folder_name = "My Folder"
            mirolib.shortcut("n",shift=True)
            if reg.m.exists("Folder",3):
             mirolib.log_result("98","test_92")
            time.sleep(2)
            type(folder_name+"\n")
            time.sleep(4)
            mirolib.delete_feed(self,reg,feed=folder_name)
            mirolib.log_result("92","delte feed folder")
    
        # Add site - and delete using shortcut key
        def _delete_site(self):
            site_url =  "http://blip.tv"
            site = "blip"
            mirolib.add_source(self,reg,site_url,site)
            time.sleep(2)
            mirolib.delete_site(self,reg,site)
            mirolib.log_result("92","delte site shortcut verified")
            time.sleep(2)
            
        #Download item and with shortcut key, delete item
        def _delete_item(self)
            title = "detective"
            mirolib.wait_for_item_in_tab(self,reg,"Misc","detective")
            mirolib.delete_items(self,reg,title,"Misc")
            mirolib.log_result("92","delete item shortcut verified")
            time.sleep(5)

        # remove playlist
        def _delete_playlist(self):
            mirolib.shortcut("p")
            if reg.m.exists("Enter a",3):
                mirolib.log_result("723","test_92")
            time.sleep(4)
            type("FaveList"+"\n")
            p = mirolib.get_playlists_region(reg)
            p.click("FaveList",2)
            time.sleep(2)
            mirolib.delete_current_selection(self,reg)
            time.sleep(2)
            self.assertFalse(p.exists("FaveList",3))
            mirolib.log_result("92","delte playlist shortcut verified")
    
        # remove playlist folder
        def _delete_playlist_folder(self):
            mirolib.shortcut("p",shift=True)
            time.sleep(4)
            if reg.m.exists("playlist folder",3):
                mirolib.log_result("724","test_92")
            type("SUPERPLAYS"+"\n")
            time.sleep(3)
            p = mirolib.get_playlists_region(reg)
            p.click("SUPERPLAYS")
            time.sleep(2)
            mirolib.delete_current_selection(self,reg)
            time.sleep(2)
            self.assertFalse(p.exists("SUPERPLAYS",3))
            mirolib.log_result("92","delte playlist folder shortcut verified")
        try: 
            _delete_feed(self)
            _delete_site(self)
            _delete_item(self)
            _delete_playlist(self)
            _delete_playlist_folder(self)
            _delete_feed_folder(self)
        except FindFailed, debugging:
            self.verificationErrors.append(debugging)
        finally:
            mirolib.quit_miro(self)
            mirolib.log_result("96","test_92") #verifies quit shortcut test
            


# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()
   

