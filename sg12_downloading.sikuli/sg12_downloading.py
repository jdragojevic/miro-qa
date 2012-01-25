import sys
import os
import unittest
import time
from sikuli.Sikuli import *
import base_testcase
import myLib.config
from myLib.miro_regions import MiroRegions
from myLib.miro_app import MiroApp


def download_playback_check_title(reg, miro, item_title, item_image):
        miro.wait_for_item_in_tab(reg, "Videos", item_title)
        if reg.m.exists(Pattern(item_image)):
            doubleClick(reg.m.getLastMatch())
            time.sleep(5)
            miro.verify_video_playback(reg)
            return True
        else:
            print ("item image %s not found" % item_image)
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
        reg = MiroRegions()
        miro = MiroApp()
        miro.cancel_all_downloads(reg)
        miro.download_from_a_url(reg, item_url, item_title)
        assert download_playback_check_title(reg, miro, item_title, item_image)


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
        reg = MiroRegions()
        miro = MiroApp()
        miro.cancel_all_downloads(reg)
        miro.download_from_a_url(reg, item_url, item_title)
        assert download_playback_check_title(reg, miro, item_title, item_image)       
 
    def test_18656_763(self):
        """http://litmus.pculture.org/show_test.cgi?id=763 youtube feed dl.

        1. Add feed
        2. Download item
        3. Verify download completes
        4. Check title display via screenshot
        5. Verify playback

        """
        url_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","youtube-feed.rss")
        feed_url = "file:///"+url_path
        feed_name = "AL JAZEERA"
        item_title = "Alarm spreads"
        item_image = "youtube_alarm_spreads.png"
        reg = MiroRegions()
        miro = MiroApp()
        miro.add_feed(reg, feed_url, feed_name)
        miro.tab_search(reg, item_title)
        miro.download_all_items(reg)
        assert download_playback_check_title(reg, miro, item_title, item_image)

    def test_18656_764(self):
        """http://litmus.pculture.org/show_test.cgi?id=764 vimeo feed dl.

        1. Add feed
        2. Download item
        3. Verify download completes
        4. Check title display via screenshot
        5. Verify playback

        """
        url_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","vimeo-feed")
        feed_url = "file:///"+url_path
        feed_name = "One Day"
        item_title = "Jellyfish"
        item_image = "vimeo-jellyfish.png"
        reg = MiroRegions()
        miro = MiroApp()
        miro.add_feed(reg, feed_url, feed_name)
        miro.tab_search(reg, item_title)
        miro.download_all_items(reg)
        assert download_playback_check_title(reg, miro, item_title, item_image)

    def test_18453_764(self):
        """http://litmus.pculture.org/show_test.cgi?id=764 vimeo likes feed dl.

        1. Add feed
        2. Download item
        3. Verify download completes
        4. Check title display via screenshot
        5. Verify playback

        """
        feed_url = "http://vimeo.com/habi/likes/rss"
        feed_name = "David"
        item_title = "glove"
        item_image = "vimeo-glove.png"
        reg = MiroRegions()
        miro = MiroApp()
        miro.add_feed(reg, feed_url, feed_name)
        miro.tab_search(reg, item_title)
        miro.download_all_items(reg)
        assert download_playback_check_title(reg, miro, item_title, item_image)

    def test_18656_765(self):
        """http://litmus.pculture.org/show_test.cgi?id=764 itunes feed dl.

        1. Add feed
        2. Download item
        3. Verify download completes
        4. Check title display via screenshot
        5. Verify playback

        """
        url_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","dilbert-feed.xml")
        feed_url = "file:///"+url_path
        feed_name = "Dilbert"
        item_title = "Survey"
        item_image = "dilbert_survey_results.png"
        reg = MiroRegions()
        miro = MiroApp()
        miro.add_feed(reg, feed_url, feed_name)
        miro.tab_search(reg, item_title)
        miro.download_all_items(reg)
        assert download_playback_check_title(reg, miro, item_title, item_image) 


    def test_112(self):
        """http://litmus.pculture.org/show_test.cgi?id=112 download errors

        1. Add feed
        2. Download All
        3. Verify error messages
        """
        reg = MiroRegions()
        miro = MiroApp()
        feed_url = "http://participatoryculture.org/feeds_test/feed13.rss"
        feed_name = "Feed"

        error_types = {"Server Closes Connection": "no_connection.png",
                       "Timeout error": "no_connection.png",
                       "File not found": "file_not_found.png",
                       "503 Error": "no_connection.png",
                       "Host not found": "unknown_host.png",
                       "HTTP error": "http_error.png"
                       }
        miro.add_feed(reg, feed_url, feed_name)
        miro.set_podcast_autodownload(reg, setting="All")
        time.sleep(10)
        for error, image in error_types.iteritems():
                miro.tab_search(reg, error)
                assert reg.m.exists(Pattern(image),5)


    def test_444(self):
        """http://litmus.pculture.org/show_test.cgi?id=444 external dl errors.

        1. http file url to download
        2. open with File Download menu
        3. Verify download completes
        4. Check title display via screenshot

        """
        item_url = "http://www.youtube.com/watch?v=LU-ZQWZSGfc&feature=fvhr"
        item_title = "watch"
        reg = MiroRegions()
        miro = MiroApp()
        miro.cancel_all_downloads(reg)
        dl_status = miro.download_from_a_url(reg, item_url, item_title)
        print dl_status
        self.failUnless(dl_status == "errors")
        miro.quit_miro()
        miro.restart_miro()
        miro.click_sidebar_tab(reg, "Downloading")
        assert mr.exists(Pattern("file_not_found.png"))
        miro.click_sidebar_tab(reg, "Videos")
        reg.s.waitVanish("Downloading")
        
 
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
