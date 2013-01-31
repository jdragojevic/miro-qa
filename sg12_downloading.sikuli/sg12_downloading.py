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
        if item_title == "Punk":  #vimeo user feed updates too frequently to worry about image
            doubleClick(item_title)
            time.sleep(5)
            miro.verify_video_playback(reg)
            return True
        elif reg.m.exists(Pattern(item_image)):
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
        item_url = http://blip.tv/file/get/Miropcf-AboutUniversalSubtitles847.ogv"
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

    def test_16456_674(self):
        """http://litmus.pculture.org/show_test.cgi?id=674 https url download.

        1. http file url to download
        2. open with File Download menu
        3. Verify download completes
        4. Check title display via screenshot

        """
        item_url = "https://www.youtube.com/watch?v=pOle1AnPOc4"
        item_title = "Charlie"
        item_image = "charlie_bit_me.png"
        reg = MiroRegions()
        miro = MiroApp()
        miro.cancel_all_downloads(reg)
        miro.download_from_a_url(reg, item_url, item_title)
        assert download_playback_check_title(reg, miro, item_title, item_image) 

    def test_13827_633(self):
        """http://litmus.pculture.org/show_test.cgi?id=633 503 error retry.

        1. 503 error file url download
        2. open with File Download menu
        3. Verify error message are displayed with retry option

        """
        url = "http://qa.pculture.org/feeds_test/503.php"
        reg = MiroRegions()
        miro = MiroApp()
        miro.cancel_all_downloads(reg)
        reg.tl.click("File")
        reg.tl.click("Download from")
        time.sleep(3)
        type(url+"\n")
        for x in range(0,2):
            time.sleep(3)
            find(Pattern("retry_dialog.png").similar(0.5))
            type(Key.ENTER)
        type(Key.ESC)
        

 
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
        item_title = "Alarm"
        item_image = "youtube_alarm_spreads.png"
        reg = MiroRegions()
        miro = MiroApp()
        miro.add_feed(reg, feed_url, feed_name)
        miro.tab_search(reg, item_title)
        miro.download_all_items(reg)
        assert download_playback_check_title(reg, miro, item_title, item_image)
        miro.delete_feed(reg, feed_name)

    def test_18656_764(self):
        """http://litmus.pculture.org/show_test.cgi?id=764 vimeo feed dl.

        1. Add feed
        2. Download item
        3. Verify download completes
        4. Check title display via screenshot
        5. Verify playback

        """
        feed_url = 'http://vimeo.com/jfinn/likes/rss' 
        feed_name = "janet"
        item_title = "Homework"
        item_image = "vimeo-homeowork.png"
        reg = MiroRegions()
        miro = MiroApp()
        miro.add_feed(reg, feed_url, feed_name)
        miro.tab_search(reg, item_title)
        miro.download_all_items(reg)
        assert download_playback_check_title(reg, miro, item_title, item_image)
        miro.delete_feed(reg, feed_name)

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
        miro.delete_feed(reg, feed_name)

    def test_14289_644(self):
        """http://litmus.pculture.org/show_test.cgi?id=644 feed items with non-ascii chars.

        1. Add feed
        2. Download item
        3. Verify download completes
        4. Check title display via screenshot
        5. Verify playback

        """

        feed_url = "http://gdata.youtube.com/feeds/api/users/4001v63/uploads"
        feed_name = "Uploads"
        item_title = "kerta"
        item_image = "non_ascii_item.png"
        reg = MiroRegions()
        miro = MiroApp()
        miro.add_feed(reg, feed_url, feed_name)
        miro.tab_search(reg, item_title)
        miro.download_all_items(reg)
        assert download_playback_check_title(reg, miro, item_title, item_image)
        miro.delete_feed(reg, feed_name)


    def test_112(self):
        """http://litmus.pculture.org/show_test.cgi?id=112 download errors

        1. Add feed
        2. Download All
        3. Verify error messages
        """
        reg = MiroRegions()
        miro = MiroApp()
        feed_url = "http://qa.pculture.org/feeds_test/feed13.rss"
        feed_name = "Feed"

        error_types = {"Server Closes Connection": "no_connection.png",
                       "File not found": "file_not_found.png",
                       "503 Error": "no_connection.png",
                       "Host not found": "unknown_host.png",
                       "HTTP error": "http_error.png",
                       "Timeout error": "no_connection.png",
                       }
        miro.add_feed(reg, feed_url, feed_name)
        miro.set_podcast_autodownload(reg, setting="All")
        time.sleep(10)
        for error, image in error_types.iteritems():
                miro.tab_search(reg, error)
                assert reg.m.exists(Pattern(image).similar(0.6),60)
        miro.delete_feed(reg, feed_name)


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
        self.assertTrue(dl_status == "failed")
        miro.quit_miro()
        miro.restart_miro()
        miro.click_sidebar_tab(reg, "Downloading")
        assert reg.m.exists(Pattern("file_not_found.png"))
        reg.m.click(item_title)
        type(Key.DELETE)
        miro.click_sidebar_tab(reg, "Videos")
        reg.s.waitVanish("Downloading")
        
 



        
# TestRunner posts output in xunit format
if __name__ == "__main__":
    from TestRunner import TestRunner
    TestRunner(Test_Downloading).run_tests()
