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
    """Subgroup 26 - Playlists tests.

    """

    def setUp(self):
        """ All playlist tests require data. Going to add feed and watched folder at the start of the subgroup.

        """
        self.verificationErrors = []
        print "starting test: ",self.shortDescription()
        config.set_image_dirs()
        mirolib.quit_miro(self)
        config.set_def_db_and_prefs()
        mirolib.restart_miro(confirm=False)
        time.sleep(10)
 
    def test_108(self):
        """http://litmus.pculture.org/show_test.cgi?id=108 playback through unplayed items.

        1. add a feed url feed of small items
        2. download a few items 
        3. verify unplayed - playback through list
        4. verify marked as unplayed.

        """
        url_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","ShortCats.xml")
        url = "file:///"+url_path
        feed = "Short Cats"
        reg = mirolib._AppRegions()
        mirolib.add_feed(self,reg,url,feed)
        mirolib.set_podcast_autodownload(self,reg,setting="All")
        time.sleep(5)
        if reg.s.exists("Downloading"):
            reg.s.waitVanish("Downloading")
        mirolib.click_sidebar_tab(self,reg,"Videos")
        mirolib.toggle_normal(reg)
        if reg.m.exists("item_play_unplayed.png"):
            find(Pattern("sort_name_normal.png").exact())
            doubleClick(getLastMatch().below(100))
            waitExists(Pattern("playback_bar_video.png"))
        else:
            self.fail("no unplayed badges found")
        if exists(Pattern("playback_bar_video.png")):
            print "playback started"
            waitVanish(Pattern("playback_bar_video.png"))
        if reg.m.exists("item_play_unplayed.png"):
            self.fail("items not marked as unplayed")

        #cleanup

   
        
 

# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()
   

