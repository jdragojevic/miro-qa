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
    """Subgroup 58 - Items.

    """
    def setUp(self):
        self.verificationErrors = []
        setAutoWaitTimeout(60)
         


    def test_361(self):
        """http://litmus.pculture.org/show_test.cgi?id=361 edit item audio to video.

        1. add 3-blip-videos feed
        2. download the Joo Joo
        3. Edit item from Video to Audio
        4. Verify item played as audio item

        """
        reg = mirolib.AppRegions()
        
        url = "http://pculture.org/feeds_test/3blipvideos.xml"
        feed = "blip"
        item_title = "Joo Joo"
        #add feed and download joo joo item
        mirolib.add_feed(self,reg,url,feed)
        reg.s.click(feed)
        mirolib.tab_search(self,reg,item_title)
        reg.m.click("Download")
        mirolib.wait_download_complete(self,reg,item_title)
        #find item in video tab and edit to audio
        mirolib.click_sidebar_tab(self,reg,"Video")
        mirolib.tab_search(self,reg,item_title,confirm_present=True)
        reg.m.click(item_title)
        reg.t.click("File")
        reg.t.click("Edit")
        reg.m.click("Audio")
        reg.m.click("Apply")
        #locate item in audio tab and verify playback
        mirolib.click_sidebar_tab(self,reg,"Music")
        mirolib.tab_search(self,reg,item_title,confirm_present=True)
        m.doubleClick(item_title)
        mirolib.verify_audio_playback(self,reg)
        #cleanup
        mirolib.delete_feed(self,reg,"blip")
 
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()
   
