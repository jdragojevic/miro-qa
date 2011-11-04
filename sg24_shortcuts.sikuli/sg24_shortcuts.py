import sys
import unittest
import time
from sikuli.Sikuli import *
import base_testcase
import myLib.config
from myLib.miro_regions import MiroRegions
from myLib.miro_app import MiroApp


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
        reg = MiroRegions() 
        miro = MiroApp()

        #start the download of the misc file for later delete
        item_url =  "http://www.boatingsidekicks.com/fish-detective.swf"
        if myLib.config.get_os_name() == "osx":
            reg.tl.click("File")
        else:
            type('f',KEY_ALT)
        reg.t.click("Download")
        time.sleep(4)
        type(item_url+"\n")
        
        
        def _delete_feed(self):
            feed_url = "stupidvideos.com/rss/rss.php?chart=new&format=yahoo"
            feed = "StupidVid"
            miro.shortcut("n")
            if reg.m.exists("URL",3):
                miro.log_result("97","test_92")
            time.sleep(2)
            type(feed_url+"\n")
            time.sleep(4)
            miro.delete_feed(reg, feed)
            miro.log_result("92","delte feed shortcut verified")

        def _delete_feed_folder(self):
            folder_name = "My Folder"
            miro.shortcut("n",shift=True)
            if reg.m.exists("Folder",3):
             miro.log_result("98","test_92")
            time.sleep(2)
            type(folder_name+"\n")
            time.sleep(4)
            miro.delete_feed(reg, feed=folder_name)
            miro.log_result("92","delte feed folder")
    
        # Add site - and delete using shortcut key
        def _delete_site(self):
            site_url =  "http://blip.tv"
            site = "blip"
            miro.add_source(reg, site_url,site)
            time.sleep(2)
            miro.delete_site(reg, site)
            miro.log_result("92","delte site shortcut verified")
            time.sleep(2)
            
        #Download item and with shortcut key, delete item
        def _delete_item(self):
            title = "detective"
            miro.wait_for_item_in_tab(reg, "Misc","detective")
            miro.delete_items(reg, title,"Misc")
            miro.log_result("92","delete item shortcut verified")
            time.sleep(5)

        # remove playlist
        def _delete_playlist(self):
            playlist = "Pavarotti"
            miro.add_playlist(reg, playlist, style="shortcut")
            miro.click_playlist(reg, playlist)
            miro.log_result("723","test_92")
            miro.delete_current_selection(reg)
            time.sleep(3)
            self.assertFalse(reg.s.exists(playlist))
            miro.log_result("92","delete playlist shortcut verified")
    
        # remove playlist folder
        def _delete_playlist_folder(self):
            miro.shortcut("p",shift=True)
            time.sleep(4)
            if reg.m.exists("playlist folder",3):
                miro.log_result("724","test_92")
            type("SUPERPLAYS"+"\n")
            time.sleep(3)
            p = miro.get_playlists_region(reg)
            p.click("SUPERPLAYS")
            time.sleep(2)
            miro.delete_current_selection(reg)
            time.sleep(2)
            self.assertFalse(p.exists("SUPERPLAYS",3))
            miro.log_result("92","delete playlist folder shortcut verified")
        try: 
            _delete_feed(self)
            _delete_site(self)
            _delete_item(self)
            _delete_playlist(self)
            _delete_playlist_folder(self)
            _delete_feed_folder(self)
        except FindFailed, debugging:
            print debugging
        finally:
            miro.quit_miro()
            miro.log_result("96","test_92") #verifies quit shortcut test
            


# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv, ).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite, ).litmus_test_run()
   

