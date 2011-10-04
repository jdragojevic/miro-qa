import sys
import unittest
import time
from sikuli.Sikuli import *
import base_testcase
import myLib.config
from myLib.miro_regions import MiroRegions
from myLib.miro_app import MiroApp


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

        reg = MiroRegions() 
        miro = MiroApp()
        # 1. Download youtube vidoe
        vid_url = "http://www.youtube.com/watch?v=baJ43ByylbM&feature=fvw"
        item_title = "Zoom"
        reg.tl.click("File")
        reg.tl.click("Download from")
        time.sleep(4)
        type(vid_url)
        time.sleep(2)
        type("\n")
        
        miro.confirm_download_started(reg, item_title)
        miro.wait_for_item_in_tab(reg, "videos",item_title)
        if reg.m.exists(item_title,3):
            miro.log_result("9","test_620 file external download verified.")
        reg.m.click(item_title)
        # 2. Convert to audio formats
        try:
            aconvertList = ("MP3","Vorbis")
            for x in aconvertList:
                miro.convert_file(reg, x)
                time.sleep(2)
            miro.click_sidebar_tab(reg, "Converting")
            miro.wait_conversions_complete(reg, item_title,x)
            
            # 3. Verify playback
            miro.click_sidebar_tab(reg, "music")
            aplaybackList = ("MP3",)
            for x in aplaybackList:
                miro.tab_search(reg, "Converted to "+str(x),False)
                if reg.m.exists(Pattern("item_play_unplayed.png")):
                    doubleClick(reg.m.getLastMatch())
                    miro.verify_audio_playback(reg, "Converted")
                else:
                    self.fail("converted item not found")
        except FindFailed, debugging:
            self.verificationErrors.append(debugging)
        finally:
            while reg.m.exists(item_title,5):
                miro.delete_items(reg, item_title,"music")
                            
        
        # 4. Convert items to video formats
        try:
            vconvertList = ("Droid","Galaxy","G2","iPad","iPhone","MP4", "Theora","Playstation")
            miro.click_sidebar_tab(reg, "Videos")
            reg.m.click(item_title)
            
            for x in vconvertList:
                miro.convert_file(reg, x)
                time.sleep(15)
            miro.click_sidebar_tab(reg, "Converting")
            miro.wait_conversions_complete(reg, item_title,str(x))
            # 5. Verify playback
            miro.click_sidebar_tab(reg, "Videos")
            aplaybackList = ("Droid", "iPhone", "MP4", "Ogg Theora", "Playstation")
            for x in aplaybackList:
                miro.tab_search(reg, "Converted to "+str(x))
                if reg.m.exists("item_play_unplayed.png"):
                    doubleClick(reg.m.getLastMatch())
                    find(Pattern("playback_bar_video.png"))
                    miro.shortcut("d")
                    waitVanish(Pattern("playback_bar_video.png"),20)
                    miro.log_result("102","test_620 stop video playback verified.")
                    time.sleep(2)
                    type(Key.DELETE)
                    miro.remove_confirm(reg, "remove")     
                    time.sleep(3)
                else: self.fail("converted item not found")
        except FindFailed, debugging:
            self.verificationErrors.append(debugging)
        finally:
            while reg.m.exists("Converted to",3):
                click(reg.m.getLastMatch())
                type(Key.DELETE)
                miro.remove_confirm(reg, "remove")  
        # 6. Cleanup
        miro.delete_items(reg, item_title,"Videos")
        
            
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv, ).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite, ).litmus_test_run()
   

