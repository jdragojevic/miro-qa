import sys
import os
import glob
import unittest
import StringIO
import time

mycwd = os.path.join(os.getcwd(),"Miro")
sys.path.append(os.path.join(mycwd,'myLib'))
import config
import mirolib
import testvars
import litmusresult



setBundlePath(config.get_img_path())


class Miro_Suite(unittest.TestCase):
    """Subgroup 72 - convert youbube video

    """
    def setUp(self):
        self.verificationErrors = []
        setAutoWaitTimeout(60)
        switchApp(mirolib.open_miro())
         


    def test_620(self):
        """http://litmus.pculture.org/show_test.cgi?id=620 dl youtube video and convert.

        1. Download youtube video
        2. Convert to video formats
        3. Verify playback
        4. Convert to audio formats
        5. Verify playback
        6. Cleanup
        """
        try:
            # 1. Download youtube vidoe
            vid_url = "http://www.youtube.com/watch?v=baJ43ByylbM&feature=fvw"
            item_title = "Hubble"
            switchApp(mirolib.open_miro())
            click("menu_file.png")
            click("menu_download.png")
            wait("enter_the_url.png")
            type(vid_url+"\n")
            
            mirolib.wait_download_complete(self,item_title)
            mirolib.click_sidebar_tab(self,"video")
            mirolib.tab_search(self,item_title,True)
            click(getLastMatch())
            # 2. Convert to audio formats
            aconvertList = ("mp3","oggvorbis")
            for x in aconvertList:
                click("menu_convert.png")
                click("menu_"+str(x)+".png")
                time.sleep(2)
            mirolib.click_sidebar_tab(self,"conversions")
            mirolib.wait_conversions_complete(self,str(x))
            
            # 3. Verify playback
            mirolib.click_sidebar_tab(self,"music")
            aplaybackList = ("MP3", "Ogg Vorbis")
            for x in aplaybackList:
                mirolib.tab_search(self,"Converted to "+str(x),False)
                self.assertTrue(exists("item_play_unplayed.png"))
                click(getLastMatch())
                self.assertTrue(exists("playback_bar_audio.png"))
                self.assertTrue(exists("item_currently_playing.png"))
                mirolib.shortcut("d")
                waitVanish("playback_bar_audio.png")
                                
            
            # 4. Convert items to video formats
            vconvertList = ("droid","galaxy","g2","ipad","iphone","mp4", "oggtheora","psp")
            
            for x in vconvertList:
                mirolib.click_menu("menu_convert.png")
                mirolib.click_menu("menu_"+str(x)+".png")
                time.sleep(4)
            mirolib.click_sidebar_tab(self,"conversions")
            mirolib.wait_conversions_complete(self,str(x))
            # 5. Verify playback
            mirolib.click_sidebar_tab(self,"video")
            aplaybackList = ("Droid", "Galaxy", "G2", "iPad", "iPhone", "MP4", "Ogg Theora", "Playstation")
            for x in aplaybackList:
                mirolib.tab_search(self,"Converted to "+str(x),False)
                self.assertTrue(exists("item_play_unplayed.png"))
                click(getLastMatch())
                self.assertTrue(exists("playback_bar_video.png"))
                mirolib.shortcut("d")
                waitVanish("playback_bar_audio.png")

        finally:
            # 6. Cleanup
            mirolib.delete_items(self,"Hubble","video")
            mirolib.delete_items(self,"Hubble","music")
            mirolib.delete_items(self,"Converted to")
            
    def tearDown(self):
        self.assertEqual([], self.verificationErrors)
    
# Post the output directly to Litmus

if config.testlitmus == True:
    suite_list = unittest.getTestCaseNames(Miro_Suite,'test')
    suite = unittest.TestSuite()
    for x in suite_list:
        suite.addTest(Miro_Suite(x))

    buf = StringIO.StringIO()
    runner = unittest.TextTestRunner(stream=buf)
    litmusresult.write_header(config.get_os_name())
    for x in suite:
        runner.run(x)
        # check out the output
        byte_output = buf.getvalue()
        id_string = str(x)
        stat = byte_output[0]
        try:
            litmusresult.write_log(id_string,stat,byte_output)
        finally:
            buf.truncate(0)
    litmusresult.write_footer()
#or just run it locally
else:
    unittest.main()

