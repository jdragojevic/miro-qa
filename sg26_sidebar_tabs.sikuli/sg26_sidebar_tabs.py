import sys
import os
import unittest
import time
from sikuli.Sikuli import *
import base_testcase
import myLib.config
from myLib.miro_regions import MiroRegions
from myLib.miro_app import MiroApp
from myLib.preferences_panel import PreferencesPanel


class Test_Playlists(base_testcase.Miro_unittest_testcase):
    """Subgroup 26 - Playlists tests.

    """


 
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
##        url = "http://pculture.org/feeds_test/2stupidvideos.xml"
##        feed = "TWO STUPID"
        
        reg = MiroRegions() 
        miro = MiroApp()


        #Set Global Preferences
        miro.open_prefs(reg)
        prefs = PreferencesPanel()
        playback_tab = prefs.open_tab("Playback")
        playback_tab.play_continuous("on", "Podcast")
        playback_tab.close_prefs()
        
        miro.add_feed(reg, url, feed)
        miro.set_podcast_autodownload(reg, setting="All")
        time.sleep(15)
        if reg.s.exists("Downloading"):
            reg.s.waitVanish("Downloading")
        miro.click_sidebar_tab(reg, "Videos")
        miro.toggle_normal(reg)
        if reg.m.exists("item_play_unplayed.png"):
            find(Pattern("sort_name_normal.png").exact())
            doubleClick(getLastMatch().below(100))
            wait(Pattern("playback_bar_video.png"),15)
        else:
            self.fail("no unplayed badges found")
        if exists(Pattern("playback_bar_video.png")):
            print "playback started"
            waitVanish(Pattern("playback_bar_video.png"))
        if reg.m.exists("item_play_unplayed.png"):
            self.fail("items not marked as unplayed")

        #cleanup

   
        
 

# TestRunner posts output in xunit format
if __name__ == "__main__":
    from TestRunner import TestRunner
    TestRunner(Test_Playlists).run_tests()
   

