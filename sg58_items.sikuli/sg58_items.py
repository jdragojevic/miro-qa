# -*- coding: utf-8 -*-
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
import prefs
import testvars
import base_testcase

class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 58 - Items.

    """

         
    def setUp(self):
        self.verificationErrors = []
        print "starting test: ",self.shortDescription()
        config.set_image_dirs()
        mirolib.quit_miro(self)
        config.set_def_db_and_prefs()
        config.delete_miro_video_storage_dir()
        mirolib.restart_miro(confirm=False)
        time.sleep(10)

    def test_361(self):
        """http://litmus.pculture.org/show_test.cgi?id=361 edit item video to audio.

        1. add 3-blip-videos feed
        2. download the Joo Joo
        3. Edit item from Video to Audio
        4. Verify item played as audio item

        """
        reg = mirolib._AppRegions()
        time.sleep(5)
        url = "http://pculture.org/feeds_test/3blipvideos.xml"
        feed = "ThreeBlip"
        title = "The Joo"
        new_type = "Music"
        
        

        #Set Global Preferences        
        prefs.set_item_display(self,reg,option="audio",setting="on")
        time.sleep(2)
        prefs.set_item_display(self,reg,option="video",setting="on")
        time.sleep(2)
        prefs.set_autodownload(self,reg,setting="Off")
        time.sleep(2)
        #start clean
        mirolib.delete_feed(self,reg,feed)
        #add feed and download joo joo item
        mirolib.add_feed(self,reg,url,feed)
        mirolib.tab_search(self,reg,title)
        if reg.m.exists("button_download.png",10):
            click(reg.m.getLastMatch())
        mirolib.wait_for_item_in_tab(self,reg,"Videos",item=title)
        reg.m.click(title)
        mirolib.click_sidebar_tab(self,reg,"Videos") #stupid workaround for bug, not recognizing selected item after search.
        time.sleep(2)
        mirolib.edit_item_type(self,reg,new_type)
        #locate item in audio tab and verify playback
        mirolib.wait_for_item_in_tab(self,reg,tab="Music",item=title)
        doubleClick(reg.m.getLastMatch())
        mirolib.verify_audio_playback(self,reg,title)
       
        #cleanup
        mirolib.delete_feed(self,reg,feed)


    def test_362(self):
        """http://litmus.pculture.org/show_test.cgi?id=362 edit item music to video

        1. add Static List Feed
        2. download the Earth Eats
        3. Edit item from Audio to Video
        4. Verify item played as video item

        """
        reg = mirolib._AppRegions()
        time.sleep(5)
        url = "http://pculture.org/feeds_test/list-of-guide-feeds.xml"
        feed = "Static"
        term = "Earth Eats"
        title = "Mushroom"
        new_type = "Video"
        #Set Global Preferences
        mirolib.delete_feed(self,reg,feed)
        prefs.set_item_display(self,reg,option="audio",setting="on")
        time.sleep(2)
        prefs.set_item_display(self,reg,option="video",setting="on")
        time.sleep(2)
        prefs.set_autodownload(self,reg,setting="Off")
        time.sleep(2)

        
        #add feed and download joo joo item
        mirolib.add_feed(self,reg,url,feed)
        mirolib.tab_search(self,reg,term)
        if reg.m.exists("button_download.png",10):
            click(reg.m.getLastMatch())
        mirolib.wait_for_item_in_tab(self,reg,"Music",item=title)
        reg.m.click(title)
        mirolib.click_sidebar_tab(self,reg,"Music") #stupid workaround for bug, not recognizing selected item after search.
        mirolib.edit_item_type(self,reg,new_type)
        #locate item in audio tab and verify playback
        mirolib.wait_for_item_in_tab(self,reg,tab="Video",item=title)
        doubleClick(reg.m.getLastMatch())
        mirolib.verify_video_playback(self,reg)
        mirolib.quit_miro(self,reg)
        mirolib.restart_miro()
        mirolib.wait_for_item_in_tab(self,reg,tab="Video",item=title)
        #cleanup
        mirolib.delete_feed(self,reg,feed)



    def test_363(self):
        """http://litmus.pculture.org/show_test.cgi?id=363 edit item metadata

        1. add Static List feed
        2. download the Earth Eats item
        3. Edit item metadata
        4. Verify item played as audio item

        """
        reg = mirolib._AppRegions()
        time.sleep(5)
        url = "http://pculture.org/feeds_test/list-of-guide-feeds.xml"
        feed = "Static"
        term = "Earth Eats"
        title = "Mushroom" # item title updates when download completes
        new_type = "Video"
        #Set Global Preferences
        prefs.set_item_display(self,reg,option="audio",setting="on")
        time.sleep(2)
        mirolib.delete_feed(self,reg,feed)
        
        #add feed and download earth eats item
        mirolib.add_feed(self,reg,url,feed)
        mirolib.toggle_normal(reg)
        mirolib.tab_search(self,reg,title=term)
        if reg.m.exists("button_download.png",10):
            click(reg.m.getLastMatch())
        mirolib.wait_for_item_in_tab(self,reg,"Music",item=title)
        reg.m.click(title)
        mirolib.click_sidebar_tab(self,reg,"Music") #stupid workaround for bug, not recognizing selected item after search.
        mirolib.edit_item_metadata(self,reg,meta_field="about",meta_value="hoovercraft full of eels")
        mirolib.tab_search(self,reg,"hoovercraft eels")
        if not reg.m.exists(title):
            self.fail("can not verify description edited")
        mirolib.delete_feed(self,reg,feed)
        

    def test_364(self):
        """http://litmus.pculture.org/show_test.cgi?id=364 edit item misc to video

        1. Download item that lands in Misc
        2. Edit type to video
        3. start playback and verify play external dialog
        4. cleanup

        """
        reg = mirolib._AppRegions()
        time.sleep(5)
        url = "http://vimeo.com/moogaloop_local.swf?clip_id=7335370&server=vimeo.com"
        title = "local"
        #Set Global Preferences
        prefs.set_item_display(self,reg,option="video",setting="on")
        time.sleep(2)
        mirolib.cancel_all_downloads(self,reg)
        reg.tl.click("File")
        reg.tl.click("Download from")
        time.sleep(4)
        type(url)
        time.sleep(10)
        type("\n")
        if reg.s.exists("Downloading"):
            print "item dl started"
            reg.s.waitVanish("Downloading",120)
            time.sleep(5)
        mirolib.wait_for_item_in_tab(self,reg,tab="Misc",item=title)
        x = reg.m.find(title)
        click(x)
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
            mirolib.verify_video_playback(self,reg)
            mirolib.delete_items(self,reg,title,"Videos")
        else:
            mirolib.delete_items(self,reg,title,"Videos")
            self.fail("item not found in videos tab")


    def test_458(self):
        """http://litmus.pculture.org/show_test.cgi?id=458 edit blank item description

        1. add TwoStupid feed
        2. download the Flip Faceitem
        3. Edit item description
        4. Cleanup
        """
        
        reg = mirolib._AppRegions()
        time.sleep(5)
        url = "http://pculture.org/feeds_test/2stupidvideos.xml"
        feed = "TwoStupid"
        title = "Flip" # item title updates when download completes
             
        #add feed and download flip face item
        mirolib.add_feed(self,reg,url,feed)
        mirolib.toggle_normal(reg)
        mirolib.tab_search(self,reg,title)
        if reg.m.exists("button_download.png",10):
            click(reg.m.getLastMatch())
        mirolib.wait_for_item_in_tab(self,reg,"Videos",item=title)
        reg.m.click(title)
        mirolib.edit_item_metadata(self,reg,meta_field="about",meta_value="Blank description edited")
        mirolib.tab_search(self,reg,"blank description")
        if reg.m.exists(title):
            mirolib.log_result("656","test_458")           
        else:
            mirolib.log_result("656","test_458",status="fail")
        #cleanup
        mirolib.delete_feed(self,reg,feed)





    def test_122(self):
        """http://litmus.pculture.org/show_test.cgi?id=122 item click actions, normal view.

        1. add 3-blip-videos feed
        2. download the Joo Joo
        3. verify varios item click scenerios

        """
        reg = mirolib._AppRegions()
        time.sleep(5)
        url = "http://pculture.org/feeds_test/3blipvideos.xml"
        feed = "ThreeBlip"
        title1 = "The Joo"
        title2 = "York"
        title3 = "Accessing"
        mirolib.delete_feed(self,reg,feed)
        
        prefs.set_autodownload(self,reg,setting="Off")
        time.sleep(2)
        prefs.set_default_view(self,reg,setting="Standard")

        #add feed and download joo joo item
        mirolib.add_feed(self,reg,url,feed)
        mirolib.tab_search(self,reg,title1)
        if reg.m.exists("button_download.png",10):
            click(reg.m.getLastMatch())

        mirolib.click_podcast(self,reg,feed)
        mirolib.tab_search(self,reg,title2,confirm_present=True)

        #double-click starts download
        doubleClick(title2)
        if mirolib.confirm_download_started(self,reg,title=title2) == "in_progress":
            mirolib.log_result("122","normal view double-click starts download")
        else:
            self.fail("normal view double-click starts download, failed")
        #double-click pauses download
        mirolib.click_podcast(self,reg,feed)
        doubleClick(title2)
        if exists("item-renderer-download-resume.png"):
            mirolib.log_result("122","normal view double-click pauses download")
        else:
            self.fail("normal view double-click pause download, failed")
        #double-click resumes download
        doubleClick(title2)
        if exists("item-renderer-download-pause.png"):
            mirolib.log_result("122","normal view double-click resume download")
        else:
            self.fail("normal view double-click resume download, failed")
        #double-click starts playback
        mirolib.wait_for_item_in_tab(self,reg,tab="Videos",item=title1)
        mirolib.click_podcast(self,reg,feed)
        mirolib.tab_search(self,reg,title1)
        doubleClick(title1)
        if exists(Pattern("playback_bar_video.png")):
            mirolib.log_result("122","normal view double-click starts playback")
        else:
            self.fail("normal view double-click start playback, failed")
        mirolib.verify_video_playback(self,reg)

        #single click thumb starts download
        mirolib.tab_search(self,reg,title3)
        if reg.m.exists("thumb-default-video.png"):
            print "using default thumb"
            click(reg.m.getLastMatch())
        else:
            print "can't find thumb, best guess"
            reg.m.find(title1)
            click(reg.m.getLastMatch().left(50))
        if mirolib.confirm_download_started(self,reg,title=title3) == "in_progress":
            mirolib.log_result("122","normal view click starts download")
        else:
            self.fail("normal view double-click starts download, failed")
        #single click thumb starts playback
        mirolib.click_podcast(self,reg,feed)
        mirolib.tab_search(self,reg,title1)
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
            mirolib.log_result("122","normal view double-click starts playback")
        else:
            self.fail("normal view double-click start playback, failed")
        mirolib.verify_video_playback(self,reg)   
        #cleanup
        mirolib.delete_feed(self,reg,feed)




    def test_76(self):
        """http://litmus.pculture.org/show_test.cgi?id=76 item http auth

        1. add the pass protected feed
        2. click to download the item
        3. enter a few invalid combos, then valid
        4. Verify download starts
       

        """
        reg = mirolib._AppRegions()
        
        time.sleep(5)
        url = "http://participatoryculture.org/feeds_test/feed1.rss"
        feed = "Yah"
        term = "fourth test"
        title = "Video 4"
        BAD_PASSW = {"auser":"apassw",
                     "12341234":"12341234",
                     " ": " ",
                     " ":"password",
                     "username": " "
                     }
        mirolib.remove_http_auth_file(self,reg)
        #add feed and download 4th item
        mirolib.add_feed(self,reg,url,feed)
        mirolib.tab_search(self,reg,term)
        reg.m.click("button_download.png")
        for username, passw in BAD_PASSW.iteritems():
            mirolib.http_auth(self,reg,username,passw)
        mirolib.http_auth(self,reg,username="tester", passw="pcfdudes")
        time.sleep(5)
        mirolib.confirm_download_started(self,reg,title)
        #cleanup
        mirolib.delete_feed(self,reg,feed)
        if mirolib.remove_http_auth_file(self,reg) == False:
            self.fail("auth file not saved on filesystem")
        
        

                                     
 
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()
   
