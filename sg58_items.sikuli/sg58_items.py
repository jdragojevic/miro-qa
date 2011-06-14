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
        setAutoWaitTimeout(60)
         


    def test_361(self):
        """http://litmus.pculture.org/show_test.cgi?id=361 edit item video to audio.

        1. add 3-blip-videos feed
        2. download the Joo Joo
        3. Edit item from Video to Audio
        4. Verify item played as audio item

        """
        reg = mirolib.AppRegions()
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

        
        #add feed and download joo joo item
        mirolib.add_feed(self,reg,url,feed)
        mirolib.tab_search(self,reg,title)
        if reg.m.exists("button_download.png",10):
            click(reg.m.getLastMatch())
        mirolib.wait_for_item_in_tab(self,reg,"Videos",item=title)
        reg.m.click(title)
        mirolib.edit_item_type(self,reg,new_type)
        #locate item in audio tab and verify playback
        mirolib.wait_for_item_in_tab(self,reg,tab="Music",item=title)
        doubleClick(reg.m.getLastMatch())
        mirolib.verify_audio_playback(self,reg,title)
        mirolib.log_result("652","test_361")
        #cleanup
        mirolib.delete_feed(self,reg,feed)


    def test_362(self):
        """http://litmus.pculture.org/show_test.cgi?id=362 edit item music to video

        1. add Static List Feed
        2. download the Earth Eats
        3. Edit item from Audio to Video
        4. Verify item played as video item

        """
        reg = mirolib.AppRegions()
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
        reg = mirolib.AppRegions()
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
        mirolib.edit_item_metadata(self,reg,meta_field="about",meta_value="New description of earth eats")
        mirolib.tab_search(self,reg,title)
        mirolib.expand_item_details(self,reg)
        if not reg.m.exists("New description"):
            self.fail("can not verify description edited")       
        #skip cleanup so you don't have to re-download for each subsequent metatdata edit  test.

    def test_364(self):
        """http://litmus.pculture.org/show_test.cgi?id=364 edit item misc to video

        1. Download item that lands in Misc
        2. Edit type to video
        3. start playback and verify play external dialog
        4. cleanup

        """
        reg = mirolib.AppRegions()
        time.sleep(5)
        url = "http://vimeo.com/moogaloop_local.swf?clip_id=7335370&server=vimeo.com"
        title = "swf"
        new_type = "Video"
        #Set Global Preferences
        prefs.set_item_display(self,reg,option="video",setting="on")
        time.sleep(2)
        mirolib.cancel_all_downloads(self,reg)
        reg.tl.click("File")
        reg.tl.click("Download from")
        time.sleep(4)
        type(url)
        time.sleep(2)
        type("\n")
        if reg.s.exists("Downloading"):
            print "item dl started"
            reg.s.waitVanish("Downloading",120)
        mirolib.wait_for_item_in_tab(self,reg,"Misc",item=title)
        x = reg.m.find(title)
        y = reg.s.find("Videos")
        dragDrop(x,y)
        #locate item in video tab and verify playback
        mirolib.wait_for_item_in_tab(self,reg,tab="Videos",item=title)
        doubleClick(reg.m.getLastMatch())
        mirolib.verify_video_playback(self,reg)       
        #cleanup
        mirolib.delete_items(self,reg,title,"Videos")



    def test_458(self):
        """http://litmus.pculture.org/show_test.cgi?id=363 edit blank item description

        1. add TwoStupid feed
        2. download the Flip Faceitem
        3. Edit item description
        4. Cleanup
        """
        
        reg = mirolib.AppRegions()
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
        mirolib.expand_item_details(self,reg)
        if not reg.m.exists("Blank description edited"):
            self.fail("can not verify description edited")
        else:
            mirolib.log_result("656","test_458")
        #cleanup
        mirolib.delete_feed(self,reg,feed)


    def test_441(self):
        """http://litmus.pculture.org/show_test.cgi?id=441 delete podcast item outside of miro

        1. add TwoStupid feed
        2. download the Flip Faceitem
        3. restart miro
        4. delete the item
        5. restart mior
        6. verify item still deleted
        """
        reg = mirolib.AppRegions()
        remember = False
        try:
            mirolib.set_preference_checkbox(self,reg,tab="General",option="When starting",setting="on")
            remember = True
        except:
            remember = False
            type(Key.ESC) #close the dialog if it didn't work
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
        mirolib.wait_download_complete(self,reg,title,torrent=False)
        mirolib.click_podcast(self,reg,feed)
        mirolib.tab_search(self,reg,title)
        reg.m.click(title)     
        filepath = mirolib.store_item_path(self,reg)
        if os.path.exists(filepath):
            print "able to verify on os level"
            found_file = True
        mirolib.quit_miro(self,reg)
        mirolib.restart_miro()
        if reg.m.exists("title"):
            mirolib.log_result("698","test_441")
        else:
            click_podcast(self,reg,feed)
        mirolib.tab_search(self,reg,term)
        reg.m.click(title)
        type(Key.DELETE)

        if found_file == True:
            if os.path.exists(filepath):
                self.fail("file not deleted from filesystem")
        else:
            mirolib.quit_miro(self,reg)
            mirolib.restart_miro()
            click_podcast(self,reg,feed)
            mirolib.tab_search(self,reg,term)
            if not reg.m.exists(Pattern("button_download.png")):
                self.fail("no download button, file not deleted")
            else:
                reg.m.click(Pattern("button_download.png"))
            if mirolib.confirm_download_started(self,reg,title) != "in_progress":
                self.fail("item not properely deleted")    
        #cleanup
        mirolib.delete_feed(self,reg,feed)


    def test_122(self):
        """http://litmus.pculture.org/show_test.cgi?id=122 item click actions, normal view.

        1. add 3-blip-videos feed
        2. download the Joo Joo
        3. verify varios item click scenerios

        """
        reg = mirolib.AppRegions()
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
        click("thumb-default-video.png")
        if mirolib.confirm_download_started(self,reg,title=title3) == "in_progress":
            mirolib.log_result("122","normal view click starts download")
        else:
            self.fail("normal view double-click starts download, failed")
        #single click thumb starts playback
        mirolib.tab_search(self,reg,title1)
        if reg.m.exists("thumb-default-video.png"):
            print "using default thumb"
            click(reg.m.getLastMatch())
        elif reg.m.exists("thumb-joojoo.png"):
            print "using default thumb"
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

    def test_725(self):
        """http://litmus.pculture.org/show_test.cgi?id=725 item click actions, list view.

        1. add 3-blip-videos feed
        2. download the Joo Joo
        3. verify varios item click scenerios

        """
        reg = mirolib.AppRegions()
        time.sleep(5)
        url = "http://pculture.org/feeds_test/3blipvideos.xml"
        feed = "ThreeBlip"
        title1 = "The Joo"
        title2 = "York"
        title3 = "Accessing"
        mirolib.delete_feed(self,reg,feed)
        prefs.set_autodownload(self,reg,setting="Off")
        prefs.set_default_view(self,reg,setting="List")
        time.sleep(2)      
        #add feed and download joo joo item
        mirolib.add_feed(self,reg,url,feed)
        mirolib.tab_search(self,reg,title1)
        #double-click starts download
        reg.m.find(title1)
        title_loc = reg.m.getLastMatch()
        doubleClick(title_loc)
        if reg.m.exists("video-download-pause.png"):
            mirolib.log_result("122","list view double-click starts download")
        else:
            self.fail("list view double-click starts download, failed")
        #double-click pauses download
        doubleClick(title_loc)
        if reg.m.exists("video-download-resume.png"):
            mirolib.log_result("122","list view double-click pauses download")
        else:
            self.fail("list view double-click pause download, failed")
        #double-click resumes download
        doubleClick(title_loc)
        if exists("video-download-pause.png"):
            mirolib.log_result("122","list view double-click resumes download")
        else:
            self.fail("list view double-click resume download, failed")
        #double-click starts playback
        mirolib.wait_for_item_in_tab(self,reg,tab="Videos",item=title1)
        mirolib.click_podcast(self,reg,feed)
        mirolib.tab_search(self,reg,title1)
        doubleClick(title1)
        if exists(Pattern("playback_bar_video.png")):
            mirolib.log_result("122","list view double-click starts playback")
        else:
            self.fail("list view double-click start playback, failed")
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
        reg = mirolib.AppRegions()
        
        time.sleep(5)
        url = "http://participatoryculture.org/feeds_test/feed1.rss"
        feed = "Yaho"
        term = "fourth test"
        title = "Video 4"
        BAD_PASSW = {"auser":"apassw",
                     "12341234":"12341234",
                     " ": " ",
                     " ":"password",
                     "username": " "
                     }
        auth_file = os.path.join(config.get_support_dir(),"httpauth")
        try:
            mirolib.remove_http_auth_file()          
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
            mirolib.quit_miro(self,reg)
            
        finally:
            if not os.path.exists(auth_file):
                self.fail("auth file not saved")
            else:
                os.remove(auth_file)
        
def test_647(self):
        """http://litmus.pculture.org/show_test.cgi?id=647 edit item metadata

        1. add Static List feed
        2. download the Earth Eats item
        3. Edit item metadata
       

        """
        reg = mirolib.AppRegions()
        time.sleep(5)
        url = "http://pculture.org/feeds_test/list-of-guide-feeds.xml"
        feed = "Static"
        term = "Earth Eats"
        title = "Mushroom" # item title updates when download completes
        new_type = "Video"

        edit_itemlist = [["name","Earth Day Everyday", "647"],
                      ["artist","Oliver and Katerina", "648"],
                      ["album","Barki Barks", "649"],
                      ["genre","family", "650"],
                      ["rating","5", "651"],
                      ["year","2010" "655"],
                      ["track_num","1", "673"],
                      ["track_of","2", "673"],
                      ]
        
        #start clean
        mirolib.delete_feed(self,reg,feed)
        #add feed and download earth eats item
        mirolib.add_feed(self,reg,url,feed)
        mirolib.toggle_normal(reg)
        mirolib.tab_search(self,reg,term)
        if reg.m.exists("button_download.png",10):
            click(reg.m.getLastMatch())
        mirolib.wait_for_item_in_tab(self,reg,"Music",item=title)
        reg.m.click(title)
        for x in edit_itemlist:
            mirolib.edit_item_metadata(self,reg,meta_field=x[0],meta_value=x[1])
            mirolib.log_result(x[2],"test_647")
            time.sleep(2)
            if not mirolib.tab_search(self,reg,"Earth Day",confirm_present=True) == True:
                self.fail("new title not saved")
        #cleanup
        mirolib.delete_feed(self,reg,feed)
       
                                     
 
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()
   
