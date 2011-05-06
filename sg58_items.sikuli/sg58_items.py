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
import prefs
import testvars
import base_testcase

class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 58 - Items.

    """
    def setUp(self):
        self.verificationErrors = []
        setAutoWaitTimeout(60)
         


    def test_361(self):
        """http://litmus.pculture.org/show_test.cgi?id=361 edit item video to audio.

        1. add 3-blip-videos feed
        2. download the Joo Joo
        3. Edit item from Video to Audio
        4. Verify item played as audio item

        """
        reg = mirolib.AppRegions()
        
        url = "http://pculture.org/feeds_test/3blipvideos.xml"
        feed = "ThreeBlip"
        title = "Joo Joo"
        new_type = "Music"
        #Set Global Preferences
        
        prefs.set_item_display(self,reg,option="audio",setting="on")
        prefs.set_item_display(self,reg,option="video",setting="on")
        prefs.set_autodownload(self,reg,setting="Off")

        
        #add feed and download joo joo item
        mirolib.add_feed(self,reg,url,feed)
        mirolib.tab_search(self,reg,title)
        if reg.m.exists("button_download.png",10):
            click(reg.m.getLastMatch())
        mirolib.wait_for_item_in_tab(self,reg,"videos",title)
        reg.m.click(title)
        mirolib.edit_item_type(self,reg,new_type)
        #locate item in audio tab and verify playback
        mirolib.wait_for_item_in_tab(self,reg,tab="Music",item=title)
        mirolib.verify_audio_playback(self,reg,title)
        #cleanup
        mirolib.delete_feed(self,reg,feed)
 
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()
   
