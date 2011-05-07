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
        def delete_feed(self):
            feed_url = "stupidvideos.com/rss/rss.php?chart=new&format=yahoo"
            feed = "StupidVideos"
            mirolib.shortcut("n")
            time.sleep(2)
            type(feed_url+"\n")
            time.sleep(4)
            mirolib.click_podcast(self,reg,feed)
            time.sleep(2)
            mirolib.delete_feed(self,reg,feed)
    
        # Add site - and delete using shortcut key
        def delete_site(self):
            site_url =  "http://blip.tv"
            site = "blip"
            mirolib.add_source(self,reg,site_url,site)
            mirolib.click_source(self,reg,site)
            time.sleep(2)
            mirolib.delete_site(self,reg,site)
            
        #Download item and with shortcut key, delete item
        def delete_item(self):
            item_url =  "http://www.boatingsidekicks.com/fish-detective.swf"
            title = "detective"
            if config.get_os_name() == "osx":
                reg.tl.click("File")
            else:
                type('f',KEY_ALT)
            reg.t.click("Download Items")
            time.sleep(4)
            type(item_url+"\n")
            mirolib.wait_for_item_in_tab(self,reg,"Misc","detective")
            mirolib.delete_items(self,reg,title,"Misc")

        # remove playlist
        def delete_playlist(self):
            mirolib.shortcut("p")
            time.sleep(4)
            type("Testlist"+"\n")
            p = mirolib.get_playlists_region(reg)
            print p
            p.click("Testlist")
            time.sleep(2)
            mirolib.delete_current_selection(self,reg)
            time.sleep(2)
            self.assertFalse(p.exists("Testlist",3))
    
        # remove playlist folder
        def delete_playlist_folder(self):
            mirolib.shortcut("p",shift=True)
            time.sleep(4)
            type("PlayFolder"+"\n")
            p = mirolib.get_playlists_region(reg)
            p.click("PlayFolder")
            time.sleep(2)
            mirolib.delete_current_selection(self,reg)
            time.sleep(2)
            self.assertFalse(p.exists("PlayFolder",3))
        try: 
            delete_feed(self)
            delete_site(self)
            delete_item(self)
            delete_playlist(self)
            delete_playlist_folder(self)
        except FindFailed, debugging:
            self.verificationErrors.append(debugging)
        except AssertionError:
            raise

# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()
   

