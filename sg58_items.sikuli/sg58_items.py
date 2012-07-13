import sys
import unittest
import time
from sikuli.Sikuli import *
import base_testcase
import myLib.config
from myLib.miro_regions import MiroRegions
from myLib.miro_app import MiroApp
from myLib.preferences_panel import PreferencesPanel


class Test_Items_Group1(base_testcase.Miro_unittest_testcase):
    """Subgroup 58 - Items.

    """
    def setUp(self):
        self.verificationErrors = []
        miro = MiroApp()
        miro.quit_miro()
        myLib.config.set_def_db_and_prefs()
        myLib.config.delete_miro_downloaded_files()

    def test_361(self):
        """http://litmus.pculture.org/show_test.cgi?id=361 edit item video to audio.

        1. add 3-blip-videos feed
        2. download the Joo Joo
        3. Edit item from Video to Audio
        4. Verify item played as audio item

        """
        reg = MiroRegions() 
        miro = MiroApp()
        time.sleep(5)
        url = "http://qa.pculture.org/feeds_test/MixedCats.xml"
        feed = "MIXED"
        title = "Tongue"
        new_type = "Music"
        old_type = "Video"

        #Set Global Preferences
        
        miro.open_prefs(reg)
        prefs = PreferencesPanel()
        general_tab = prefs.open_tab("General")
        general_tab.show_audio_in_music("on")
        general_tab.show_videos_in_videos("on")
        podcasts_tab = prefs.open_tab("Podcasts")
        podcasts_tab.autodownload_setting("Off")
        podcasts_tab.close_prefs()
        
        #start clean
        miro.delete_feed(reg, feed)
        #add feed and download joo joo item
        miro.add_feed(reg, url,feed)
        miro.tab_search(reg, title)
        if reg.m.exists("button_download.png",10):
            click(reg.m.getLastMatch())
        miro.wait_for_item_in_tab(reg, "Videos", item=title)
        reg.m.find(title)
        reg.m.click(title)
        reg.mtb.click("tabsearch_clear.png")
        miro.edit_item_type(reg, new_type, old_type)
        #locate item in audio tab and verify playback
        miro.wait_for_item_in_tab(reg, tab="Music",item=title)
        reg.m.click(title)        
        type(' ') #use spacebar to start playback
        self.assertTrue(miro.verify_audio_playback(reg, title))
        miro.stop_audio_playback(reg, title)
       
        #cleanup
        miro.delete_feed(reg, feed)


    def test_362(self):
        """http://litmus.pculture.org/show_test.cgi?id=362 edit item music to video

        1. add Feed
        2. download Paris mp3
        3. Edit item from Audio to Video
        4. Verify item played as video item

        """
        reg = MiroRegions() 
        miro = MiroApp()
        time.sleep(5)
        url = "http://qa.pculture.org/feeds_test/MixedCats.xml"
        feed = "MIXED"
        term = "Paris"
        title = "Laren"
        new_type = "Video"
        old_type = "Music"
        #Set Global Preferences
        miro.open_prefs(reg)
        prefs = PreferencesPanel()
        general_tab = prefs.open_tab("General")
        general_tab.show_audio_in_music("on")
        general_tab.show_videos_in_videos("on")
        podcasts_tab = prefs.open_tab("Podcasts")
        podcasts_tab.autodownload_setting("Off")
        podcasts_tab.close_prefs()

        
        #add feed and download joo joo item
        miro.add_feed(reg, url,feed)
        miro.tab_search(reg, term)
        if reg.m.exists("button_download.png",10):
            click(reg.m.getLastMatch())
        miro.wait_for_item_in_tab(reg, "Music",item=title)
        reg.m.find(title)
        reg.m.click(title)
        reg.mtb.click("tabsearch_clear.png")
        miro.edit_item_type(reg, new_type, old_type)
        #locate item in audio tab and verify playback
        miro.wait_for_item_in_tab(reg, tab="Video",item=title)
        reg.m.doubleClick(title)
        miro.verify_video_playback(reg)
        miro.quit_miro()
        miro.restart_miro()
        miro.wait_for_item_in_tab(reg, tab="Video",item=title)
        #cleanup
        miro.delete_feed(reg, feed)



    def test_363(self):
        """http://litmus.pculture.org/show_test.cgi?id=363 edit item metadata

        1. add Static List feed
        2. download the Earth Eats item
        3. Edit item metadata
        4. Verify item played as audio item

        """
        reg = MiroRegions() 
        miro = MiroApp()
        time.sleep(5)
        url = "http://qa.pculture.org/feeds_test/list-of-guide-feeds.xml"
        feed = "Static"
        term = "Earth Eats"
        title = "Mushroom" 
        new_type = "Video"
        #Set Global Preferences
        miro.open_prefs(reg)
        prefs = PreferencesPanel()
        general_tab = prefs.open_tab("General")
        general_tab.show_audio_in_music("on")
        general_tab.close_prefs()

        
        miro.delete_feed(reg, feed)
        
        #add feed and download earth eats item
        miro.add_feed(reg, url,feed)
        miro.toggle_normal(reg)
        miro.tab_search(reg, title=term)
        if reg.m.exists("button_download.png",10):
            click(reg.m.getLastMatch())
        miro.wait_for_item_in_tab(reg, "Music", item=title)
        reg.m.find(title)
        reg.m.click(title)
        reg.mtb.click("tabsearch_clear.png")
        miro.edit_item_metadata(reg, meta_field="about",meta_value="hoovercraft full of eels")
        miro.tab_search(reg, "hoovercraft eels")
        if not reg.m.exists(title):
            self.fail("can not verify description edited")
        miro.delete_feed(reg, feed)
        

    def test_364(self):
        """http://litmus.pculture.org/show_test.cgi?id=364 edit item misc to video

        1. Download item that lands in Misc
        2. Edit type to video
        3. start playback and verify play external dialog
        4. cleanup

        """
        reg = MiroRegions() 
        miro = MiroApp()
        time.sleep(5)
        url = "http://vimeo.com/moogaloop_local.swf?clip_id=7335370&server=vimeo.com"
        title = "swf"
        #Set Global Preferences
        miro.open_prefs(reg)
        prefs = PreferencesPanel()
        general_tab = prefs.open_tab("General")
        general_tab.show_videos_in_videos("on")
        general_tab.close_prefs()
        miro.cancel_all_downloads(reg)
        reg.tl.click("File")
        reg.tl.click("Download from")
        time.sleep(4)
        type(url)
        time.sleep(2)
        type("\n")
        x = miro.wait_for_item_in_tab(reg, tab="Misc",item=title)
        reg.s.find("Music")
        tmpr = Region(reg.s.getLastMatch().above())
        tmpr.setW(tmpr.getW()+80)
        tmpr.setX(tmpr.getX()-20)
        y = tmpr.find("Videos")
        dragDrop(x,y)
        #locate item in video tab and verify playback
        click(y)
        if reg.m.exists(title):
            doubleClick(reg.m.getLastMatch())
            miro.verify_video_playback(reg)
            miro.delete_items(reg, title,"Videos")
        else:
            miro.delete_items(reg, title,"Videos")
            self.fail("item not found in videos tab")


    def test_458(self):
        """http://litmus.pculture.org/show_test.cgi?id=458 edit blank item description

        1. add TWO STUPID feed
        2. download the Flip Faceitem
        3. Edit item description
        4. Cleanup
        """
        
        reg = MiroRegions() 
        miro = MiroApp()
        time.sleep(5)
        url = "http://qa.pculture.org/feeds_test/2stupidvideos.xml"
        feed = "TWO STUPID"
        title = "Flip" # item title updates when download completes
             
        #add feed and download flip face item
        miro.add_feed(reg, url,feed)
        miro.toggle_normal(reg)
        miro.tab_search(reg, title)
        if reg.m.exists("button_download.png",10):
            click(reg.m.getLastMatch())
        miro.wait_for_item_in_tab(reg, "Videos",item=title)
        reg.m.find(title)
        reg.m.click(title)
        reg.mtb.click("tabsearch_clear.png")
        miro.edit_item_metadata(reg, meta_field="about",meta_value="Blank description edited")
        miro.tab_search(reg, "blank description")
        #cleanup
        miro.delete_feed(reg, feed)



    def test_122(self):
        """http://litmus.pculture.org/show_test.cgi?id=122 item click actions, normal view.

        1. add 3-blip-videos feed
        2. download the Joo Joo
        3. verify varios item click scenerios

        """
        reg = MiroRegions() 
        miro = MiroApp()
        time.sleep(5)
        url = "http://qa.pculture.org/feeds_test/3blipvideos.xml"
        feed = "ThreeBlip"
        title1 = "The Joo"
        title2 = "York"
        title3 = "Accessing"
        miro.delete_feed(reg, feed)


        miro.open_prefs(reg)
        prefs = PreferencesPanel()
        podcasts_tab = prefs.open_tab("Podcasts")
        podcasts_tab.autodownload_setting("Off")
        podcasts_tab.default_view_setting("Standard")
        podcasts_tab.close_prefs()

        #add feed and download joo joo item
        miro.add_feed(reg, url,feed)
        miro.tab_search(reg, title1)
        if reg.m.exists("button_download.png",10):
            click(reg.m.getLastMatch())

        miro.click_podcast(reg, feed)
        miro.tab_search(reg, title2,confirm_present=True)

        #double-click starts download
        doubleClick(title2)
        if miro.confirm_download_started(reg, title=title2) == "in_progress":
            miro.log_result("122","normal view double-click starts download")
        else:
            self.fail("normal view double-click starts download, failed")
        #double-click pauses download
        miro.click_podcast(reg, feed)
        doubleClick(title2)
        if exists("item-renderer-download-resume.png"):
            miro.log_result("122","normal view double-click pauses download")
        else:
            self.fail("normal view double-click pause download, failed")
        #double-click resumes download
        doubleClick(title2)
        if exists("item-renderer-download-pause.png"):
            miro.log_result("122","normal view double-click resume download")
        else:
            self.fail("normal view double-click resume download, failed")
        #double-click starts playback
        miro.wait_for_item_in_tab(reg, tab="Videos",item=title1)
        miro.click_podcast(reg, feed)
        miro.tab_search(reg, title1)
        doubleClick(title1)
        if exists(Pattern("playback_bar_video.png")):
            miro.log_result("122","normal view double-click starts playback")
        else:
            self.fail("normal view double-click start playback, failed")
        miro.verify_video_playback(reg)

        #single click thumb starts download
        miro.tab_search(reg, title3)
        if reg.m.exists("thumb-default-video.png"):
            print "using default thumb"
            click(reg.m.getLastMatch())
        else:
            print "can't find thumb, best guess"
            reg.m.find(title3)
            click(reg.m.getLastMatch().left(50))
        if miro.confirm_download_started(reg, title=title3) == "in_progress":
            miro.log_result("122","normal view click starts download")
        else:
            self.fail("normal view double-click starts download, failed")
        #single click thumb starts playback
        miro.click_podcast(reg, feed)
        miro.tab_search(reg, title1)
        if reg.m.exists("thumb-default-video.png"):
            print "using default thumb"
            click(reg.m.getLastMatch())
        elif reg.m.exists("thumb-joojoo.png"):
            print "found joo joo thumb"
            click(reg.m.getLastMatch())
        else:
            print "can't find thumb, best guess"
            reg.m.find(title1)
            click(reg.m.getLastMatch().left(50))
        if exists("playback_bar_video.png"):
            miro.log_result("122","normal view double-click starts playback")
        else:
            self.fail("normal view double-click start playback, failed")
        miro.verify_video_playback(reg)   
        #cleanup
        miro.delete_feed(reg, feed)




    def test_76(self):
        """http://litmus.pculture.org/show_test.cgi?id=76 item http auth

        1. add the pass protected feed
        2. click to download the item
        3. enter a few invalid combos, then valid
        4. Verify download starts
       

        """
        reg = MiroRegions() 
        miro = MiroApp()
        
        time.sleep(5)
        url = "http://qa.participatoryculture.org/feeds_test/feed1.rss"
        feed = "Yah"
        term = "fourth test"
        title = "Video 4"
        BAD_PASSW = {"auser":"apassw",
                     "12341234":"12341234",
                     " ": " ",
                     " ":"password",
                     "username": " "
                     }
        miro.remove_http_auth_file(reg)
        #add feed and download 4th item
        miro.add_feed(reg, url,feed)
        miro.tab_search(reg, term)
        reg.m.click("button_download.png")
        for username, passw in BAD_PASSW.iteritems():
            miro.http_auth(reg, username,passw)
        miro.http_auth(reg, username="tester", passw="pcfdudes")
        time.sleep(5)
        miro.confirm_download_started(reg, title)
        #cleanup
        miro.delete_feed(reg, feed)
        if miro.remove_http_auth_file(reg) == False:
            self.fail("auth file not saved on filesystem")
        
        

                                     
 
# TestRunner posts output in xunit format
if __name__ == "__main__":
    from TestRunner import TestRunner
    TestRunner(Test_Items_Group1).run_tests()
   
