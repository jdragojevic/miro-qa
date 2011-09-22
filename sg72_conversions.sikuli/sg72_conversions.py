import sys
import os
import glob
import unittest
import StringIO
import time
from sikuli.Sikuli import *

mycwd = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro")
sys.path.append(os.path.join(mycwd,'myLib'))
import base_testcase
import config
import mirolib 
import miro_regions
import prefs
import testvars


class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 72 - Conversion tests.

    """
      


    def test_620(self):
        """http://litmus.pculture.org/show_test.cgi?id=620 dl youtube video and convert.

        1. Download youtube video
        2. Convert to video formats
        3. Verify playback
        4. Convert to audio formats
        5. Verify playback
        6. Cleanup
        """

        reg = miro_regions.MiroRegions()
        # 1. Download youtube vidoe
        vid_url = "http://www.youtube.com/watch?v=baJ43ByylbM&feature=fvw"
        item_title = "Zoom"
        reg.tl.click("File")
        reg.tl.click("Download from")
        time.sleep(4)
        type(vid_url)
        time.sleep(2)
        type("\n")
        
        mirolib.confirm_download_started(self,reg,item_title)
        mirolib.wait_for_item_in_tab(self,reg,"videos",item_title)
        if reg.m.exists(item_title,3):
            mirolib.log_result("9","test_620 file external download verified.")
        reg.m.click(item_title)
        # 2. Convert to audio formats
        try:
            aconvertList = ("MP3","Vorbis")
            for x in aconvertList:
                mirolib.convert_file(self,reg,x)
                time.sleep(2)
            mirolib.click_sidebar_tab(self,reg,"Converting")
            mirolib.wait_conversions_complete(self,reg,item_title,x)
            
            # 3. Verify playback
            mirolib.click_sidebar_tab(self,reg,"music")
            aplaybackList = ("MP3",)
            for x in aplaybackList:
                mirolib.tab_search(self,reg,"Converted to "+str(x),False)
                if reg.m.exists(Pattern("item_play_unplayed.png")):
                    doubleClick(reg.m.getLastMatch())
                    mirolib.verify_audio_playback(self,reg,"Converted")
                else:
                    self.fail("converted item not found")
        except FindFailed, debugging:
            self.verificationErrors.append(debugging)
        finally:
            while reg.m.exists(item_title,5):
                mirolib.delete_items(self,reg,item_title,"music")
                            
        
        # 4. Convert items to video formats
        try:
            vconvertList = ("Droid","Galaxy","G2","iPad","iPhone","MP4", "Theora","Playstation")
            mirolib.click_sidebar_tab(self,reg,"Videos")
            reg.m.click(item_title)
            
            for x in vconvertList:
                mirolib.convert_file(self,reg,x)
                time.sleep(15)
            mirolib.click_sidebar_tab(self,reg,"Converting")
            mirolib.wait_conversions_complete(self,reg,item_title,str(x))
            # 5. Verify playback
            mirolib.click_sidebar_tab(self,reg,"Videos")
            aplaybackList = ("Droid", "iPhone", "MP4", "Ogg Theora", "Playstation")
            for x in aplaybackList:
                mirolib.tab_search(self,reg,"Converted to "+str(x))
                if reg.m.exists("item_play_unplayed.png"):
                    doubleClick(reg.m.getLastMatch())
                    find(Pattern("playback_bar_video.png"))
                    mirolib.shortcut("d")
                    waitVanish(Pattern("playback_bar_video.png"),20)
                    mirolib.log_result("102","test_620 stop video playback verified.")
                    time.sleep(2)
                    type(Key.DELETE)
                    mirolib.remove_confirm(self,reg,"remove")     
                    time.sleep(3)
                else: self.fail("converted item not found")
        except FindFailed, debugging:
            self.verificationErrors.append(debugging)
        finally:
            while reg.m.exists("Converted to",3):
                click(reg.m.getLastMatch())
                type(Key.DELETE)
                mirolib.remove_confirm(self,reg,"remove")  
        # 6. Cleanup
        mirolib.delete_items(self,reg,item_title,"Videos")
        
            
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv, ).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite, ).litmus_test_run()
   

