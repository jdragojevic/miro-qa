import sys
import os
import glob
import unittest
import StringIO
import time
from sikuli.Sikuli import *
mycwd = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro")
sys.path.append(os.path.join(os.getcwd(),'myLib'))
import base_testcase
import config
import mirolib
import testvars



class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 11 - Torrent tests.

    """

    def test_001setup(self):
        mirolib.quit_miro(self)
        config.set_def_db_and_prefs()
        mirolib.restart_miro(confirm=False)
        time.sleep(10)

    def test_419(self):
        """http://litmus.pculture.org/show_test.cgi?id=419 external torrent dl.

        1. clearbits torrent dl
        2. open with File Download menu
        3. Verify download started and metadata
        4. Cleanup

        """
        reg = mirolib._AppRegions()
        
        item_url = "http://youtorrent.com/download/7379834/young-broke-and-fameless-the-mixtape.torrent"
        item_title = "Fameless"
        reg.tl.click("File")
        reg.tl.click("Download from")
        time.sleep(5)
        type(item_url+"\n")
        print ("confirm download started")
        status = mirolib.confirm_download_started(self,reg,item_title)
        print status
        if status == "downloaded":
            mirolib.delete_items(self,reg,item_title,"Misc")
        elif status == "in_progress":
            mirolib.delete_items(self,reg,item_title,"Downloading")
        else:
            self.fail("Can not confirm download started")

    def test_719(self):
        """http://litmus.pculture.org/show_test.cgi?id=719 external torrent dl from browser

        1. clearbits torrent dl
        2. open with browser
        3. Verify download started and metadata
        4. Cleanup

        """
        reg = mirolib._AppRegions()
        
        url = "http://www.clearbits.net/get/993-wurlitztraction---lucidity-cue.torrent"
        item_title = "Enough"
        mirolib.browser_to_miro(self,reg,url)
        print ("confirm download started")
        status = mirolib.confirm_download_started(self,reg,item_title)
        print status
        if status == "downloaded":
            mirolib.delete_items(self,reg,item_title,"Misc")
        elif status == "in_progress":
            mirolib.delete_items(self,reg,item_title,"Downloading")
        else:
            self.fail("Can not confirm download started")


        
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    print sys.argv
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()
   

