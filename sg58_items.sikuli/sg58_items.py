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
        title2 = "New York"
        title3 = "Accessing"
        mirolib.delete_feed(self,reg,feed)
        
        prefs.set_autodownload(self,reg,setting="Off")
        time.sleep(2)      
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
        title2 = "New York"
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
            auth_file = os.path.join(config.get_support_dir(),"httpauth")
        finally:
            if not os.path.exists(auth_file):
                self.fail("auth file not saved")
            else:
                os.remove(auth_file)
        
        
                                     
 
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()
   
