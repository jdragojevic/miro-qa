import sys
import os
import glob
import unittest
import StringIO
import time
from sikuli.Sikuli import *
mycwd = os.path.join(os.getcwd(),"Miro")
sys.path.append(os.path.join(mycwd,'myLib'))
import config
import mirolib
import testvars
import base_testcase

class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 72 - convert youbube video

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

        ffApp = App("Firefox")
        reg = mirolib.AppRegions()
        try:
            # 1. Download youtube vidoe
            vid_url = "http://www.youtube.com/watch?v=baJ43ByylbM&feature=fvw"
            item_title = "Hubble"
            switchApp(mirolib.open_miro())
            reg.tl.click("File")
            reg.tl.click("Download")
            time.sleep(4)
            type(vid_url+"\n")
            
            mirolib.wait_download_complete(self,reg,item_title)
            mirolib.click_sidebar_tab(self,reg,"video")
            mirolib.tab_search(self,reg,item_title,True)
            reg.m.click(item_title)
            # 2. Convert to audio formats
            aconvertList = ("mp3","oggvorbis")
            for x in aconvertList:
                reg.tl.click("Convert")
                reg.tl.click(x)
                time.sleep(2)
            mirolib.click_sidebar_tab(self,reg,"conversions")
            mirolib.wait_conversions_complete(self,reg,title,str(x))
            
            # 3. Verify playback
            mirolib.click_sidebar_tab(self,"music")
            aplaybackList = ("MP3", "Ogg Vorbis")
            for x in aplaybackList:
                mirolib.tab_search(self,reg,"Converted to "+str(x),False)
                self.assertTrue(reg.m.exists("item_play_unplayed.png"))
                click(reg.m.getLastMatch())
                mirolib.verify_audio_playback(self,reg)
                                
            
            # 4. Convert items to video formats
            vconvertList = ("droid","galaxy","g2","ipad","iphone","mp4", "oggtheora","psp")
            
            for x in vconvertList:
                reg.tl.click("Convert")
                reg.tl.click(x)
                time.sleep(4)
            mirolib.click_sidebar_tab(self,reg,"conversions")
            mirolib.wait_conversions_complete(self,reg,title,str(x))
            # 5. Verify playback
            mirolib.click_sidebar_tab(self,"video")
            aplaybackList = ("Droid", "Galaxy", "G2", "iPad", "iPhone", "MP4", "Ogg Theora", "Playstation")
            for x in aplaybackList:
                mirolib.tab_search(self,reg,"Converted to "+str(x))
                self.assertTrue(reg.m.exists("item_play_unplayed.png"))
                click(reg.m.getLastMatch())
                self.assertTrue(exists("playback_bar_video.png"))
                mirolib.shortcut("d")
                waitVanish("playback_bar_video.png")

        finally:
            # 6. Cleanup
            mirolib.delete_items(self,reg,item_title,"video")
            mirolib.delete_items(self,reg,item_title,"music")
            
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()
   

