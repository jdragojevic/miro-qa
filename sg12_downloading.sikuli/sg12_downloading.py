import sys
import unittest
import time
from sikuli.Sikuli import *
import base_testcase
import myLib.config
from myLib.miro_regions import MiroRegions
from myLib.miro_app import MiroApp


def download_playback_check_title(item_url, item_title, item_image):
        reg = MiroRegions()
        miro = MiroApp()
        miro.cancel_all_downloads(reg)
        miro.download_from_a_url(reg, item_url, item_title)
        miro.wait_for_item_in_tab(reg, "Videos", item_title)
        miro.click_sidebar_tab(reg, "Videos")
        miro.tab_search(reg, item_title, confirm_present=True)
        if reg.m.exists(Pattern(item_image)):
            doubleClick(reg.m.getLastMatch())
            miro.verify_video_playback(reg)
            return True
        else:
            return False
    



class Test_Downloading(base_testcase.Miro_unittest_testcase):
    """Subgroup 12 - Download tests.

    """
        

    def test_9(self):
        """http://litmus.pculture.org/show_test.cgi?id=9 external dl.

        1. http file url to download
        2. open with File Download menu
        3. Verify download completes
        4. Check title display via screenshot

        """
        item_url = "http://j2.video2.blip.tv/7790005512538/Miropcf-TurnASearchIntoAChannel756.mp4"
        item_title = "Miropcf"
        item_image = "Miropcf_TurnASearch.png"
        assert download_playback_check_title(item_url, item_title, item_image)

    def test_youtube_9(self):
        """http://litmus.pculture.org/show_test.cgi?id=9 external dl youtube.

        1. http file url to download
        2. open with File Download menu
        3. Verify download completes
        4. Check title display via screenshot

        """
        item_url = "http://www.youtube.com/watch?v=5pB3gAjivrY"
        item_title = "Andrew"
        item_image = "andrew_garcia_straight_up.png"
        assert download_playback_check_title(item_url, item_title, item_image)       
 
##    def test_dilbert_9(self):
##        """http://litmus.pculture.org/show_test.cgi?id=9 external dl youtube.
##
##        1. http file url to download
##        2. open with File Download menu
##        3. Verify download completes
##        4. Check title display via screenshot
##
##        """
##        item_url = "http://traffic.libsyn.com/dilbert/d295.m4v"
##        item_title = "Head Count"
##        item_image = "dilbert_head_count.png"
##        assert download_playback_check_title(item_url, item_title, item_image)

##    def test_719(self):
##        """http://litmus.pculture.org/show_test.cgi?id=719 external torrent dl from browser
##
##        1. clearbits torrent dl
##        2. open with browser
##        3. Verify download started and metadata
##        4. Cleanup
##
##        """
##        reg = MiroRegions()
##        miro = MiroApp()
##        
##        url = "http://www.clearbits.net/get/993-wurlitztraction---lucidity-cue.torrent"
##        item_title = "Enough"
##        miro.browser_to_miro(reg, url)
##        print ("confirm download started")
##        status = miro.confirm_download_started(reg, item_title)
##        print status
##        if status == "downloaded":
##            miro.delete_items(reg, item_title,"Misc")
##        elif status == "in_progress":
##            miro.delete_items(reg, item_title,"Downloading")
##        else:
##            self.fail("Can not confirm download started")


        
# TestRunner posts output in xunit format
if __name__ == "__main__":
    from TestRunner import TestRunner
    TestRunner(Test_Downloading).run_tests()
