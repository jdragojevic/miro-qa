import sys
import unittest
import time
from sikuli.Sikuli import *
import base_testcase
import myLib.config
from myLib.miro_regions import MiroRegions
from myLib.miro_app import MiroApp



class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 11 - Torrent tests.

    """

    def test_001setup(self):
        miro = MiroApp()
        miro.quit_miro()
        myLib.config.set_def_db_and_prefs()
        miro.restart_miro()
        time.sleep(10)

    def test_419(self):
        """http://litmus.pculture.org/show_test.cgi?id=419 external torrent dl.

        1. clearbits torrent dl
        2. open with File Download menu
        3. Verify download started and metadata
        4. Cleanup

        """
        reg = MiroRegions()
        miro = MiroApp()
        
        item_url = "http://youtorrent.com/download/7379834/young-broke-and-fameless-the-mixtape.torrent"
        item_title = "Fameless"
        reg.tl.click("File")
        reg.tl.click("Download from")
        time.sleep(5)
        type(item_url+"\n")
        print ("confirm download started")
        status = miro.confirm_download_started(reg, item_title)
        print status
        if status == "downloaded":
            miro.delete_items(reg, item_title,"Misc")
        elif status == "in_progress":
            miro.delete_items(reg, item_title,"Downloading")
        else:
            self.fail("Can not confirm download started")

    def test_719(self):
        """http://litmus.pculture.org/show_test.cgi?id=719 external torrent dl from browser

        1. clearbits torrent dl
        2. open with browser
        3. Verify download started and metadata
        4. Cleanup

        """
        reg = MiroRegions()
        miro = MiroApp()
        
        url = "http://www.clearbits.net/get/993-wurlitztraction---lucidity-cue.torrent"
        item_title = "Enough"
        miro.browser_to_miro(reg, url)
        print ("confirm download started")
        status = miro.confirm_download_started(reg, item_title)
        print status
        if status == "downloaded":
            miro.delete_items(reg, item_title,"Misc")
        elif status == "in_progress":
            miro.delete_items(reg, item_title,"Downloading")
        else:
            self.fail("Can not confirm download started")


        
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    print sys.argv
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv, ).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite, ).litmus_test_run()
   

