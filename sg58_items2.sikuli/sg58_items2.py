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


class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 58 - Items - more tests.

    """


    def setUp(self):
        reg = MiroRegions() 
        miro = MiroApp()
        self.verificationErrors = []
        print "starting test: ",self.shortDescription()
        myLib.config.set_image_dirs()
        miro.quit_miro()
        myLib.config.set_def_db_and_prefs()
        myLib.config.delete_miro_downloaded_files()
        miro.restart_miro()
        time.sleep(10)

    def test_653(self):
        """http://litmus.pculture.org/show_test.cgi?id=653 edit album art

        1. add watched folder
        2. Edit artwork for 1 item
        3. Edit artwork for multiple items
        4. Cleanup
        """
        
        reg = MiroRegions() 
        miro = MiroApp()
        time.sleep(5)
        folder_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","ArtTest")
        title = "Pancakes"
        title2 = "summer"
        title3="deerhunter"
       
        
        #1. add watched folder
        miro.add_watched_folder(reg, folder_path)
        if reg.s.exists("ArtTest"):
            click(reg.s.getLastMatch())          
            miro.log_result("157","test_653")
        art_file = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","album_art1.jpg")    
        #add feed and download flip face item
        miro.toggle_normal(reg)
        miro.tab_search(reg, title)
        try:
            reg.m.click(title)
            miro.edit_item_metadata(reg, meta_field="art",meta_value=art_file)
            ## Verify new image here:
            reg.m.find(Pattern("album_art1.png"))
        finally:
            miro.open_prefs(reg)
            prefs = PreferencesPanel()
            folder_tab = prefs.open_tab("Folders")
            folder_tab.remove_watched_folder("ArtTest")
            folder_tab.close_prefs()
            
        
    def test_728(self):
        """http://litmus.pculture.org/show_test.cgi?id=728 edit metadata for mulitple items

        1. add Static List feed
        2. download the Earth Eats item
        3. Edit item metadata
       

        """
        reg = MiroRegions() 
        miro = MiroApp()
        
        
        miro.open_prefs(reg)
        prefs = PreferencesPanel()
        general_tab = prefs.open_tab("General")
        general_tab.show_audio_in_music("on")
        general_tab.close_prefs()
        
        url = "http://pculture.org/feeds_test/list-of-guide-feeds.xml"
        feed = "Static"
        term = "Earth Eats"
        title = "Mushroom" # item title updates when download completes
        new_type = "Video"

        edit_itemlist = [
            ["name", "Earth Day Everyday", "647"],
            ["artist", "Oliver and Katerina", "648"],
            ["album", "Barki Barks", "649"],
            ["genre", "family", "650"],
            ["track_num" ,"1", "673"],
            ["track_of" ,"2", "673"],
            ["year", "2010", "655"],
            ["rating", "5", "651"],
            ]
        
        #start clean
        miro.delete_feed(reg, feed)
        #add feed and download earth eats item
        miro.add_feed(reg, url,feed)
        miro.toggle_normal(reg)
        miro.tab_search(reg, term)
        if reg.m.exists("button_download.png",10):
            click(reg.m.getLastMatch())
        miro.wait_for_item_in_tab(reg, "Music",item=title)
        reg.m.click(title)
        for x in edit_itemlist:
            miro.edit_item_metadata(reg, meta_field=x[0],meta_value=x[1])
            try:
                miro.log_result(x[2],"test_647")
            finally:
                time.sleep(2)
        if not miro.tab_search(reg, "Earth Day",confirm_present=True) == True:
            self.fail("new title not saved")
        #cleanup
        miro.delete_feed(reg, feed)

        

    def test_441(self):
        """http://litmus.pculture.org/show_test.cgi?id=441 delete podcast item outside of miro

        1. add TwoStupid feed
        2. download the Flip Faceitem
        3. restart miro
        4. delete the item
        5. restart miro
        6. verify item still deleted
        """
        reg = MiroRegions() 
        miro = MiroApp()

        #Set Global Preferences

        miro.open_prefs(reg)
        prefs = PreferencesPanel()
        general_tab = prefs.open_tab("General")
        general_tab.remember_last_screen_on_startup("on")
        general_tab.close_prefs()
   
        url = "http://pculture.org/feeds_test/2stupidvideos.xml"
        feed = "TwoStupid"
        title = "Flip" # item title updates when download completes
             
        #add feed and download flip face item
        miro.add_feed(reg, url,feed)
        miro.toggle_normal(reg)
        miro.tab_search(reg, title)
        if reg.m.exists("button_download.png",10):
            click(reg.m.getLastMatch())
        miro.wait_for_item_in_tab(reg, tab="Videos",item=title)
        miro.click_podcast(reg, feed)
        miro.tab_search(reg, title)
        reg.m.click(title)     
        filepath = miro.store_item_path(reg)
        if os.path.exists(filepath):
            print "able to verify on os level"
            found_file = True
        miro.quit_miro(reg)
        miro.restart_miro()
        if reg.m.exists("title",15):  #check the remember last tab setting
            miro.log_result("698","test_441")
        else:
            miro.click_podcast(reg, feed)
        miro.tab_search(reg, title)
        reg.m.click(title)
        type(Key.DELETE)

        if found_file == True:
            if os.path.exists(filepath):
                self.fail("file not deleted from filesystem")
        else:
            miro.quit_miro(reg)
            miro.restart_miro()
            miro.click_podcast(reg, feed)
            miro.tab_search(reg, term)
            if not reg.m.exists(Pattern("button_download.png")):
                self.fail("no download button, file not deleted")
            else:
                reg.m.click(Pattern("button_download.png"))
            if miro.confirm_download_started(reg, title) != "in_progress":
                self.fail("item not properely deleted")    
        #cleanup
        miro.delete_feed(reg, feed)


  

    def test_725(self):
        """http://litmus.pculture.org/show_test.cgi?id=725 item click actions, list view.

        1. add 3-blip-videos feed
        2. download the Joo Joo
        3. verify varios item click scenerios

        """
        reg = MiroRegions() 
        miro = MiroApp()
        time.sleep(5)
        url = "http://pculture.org/feeds_test/3blipvideos.xml"
        feed = "ThreeBlip"
        title1 = "The Joo"
        title2 = "York"
        title3 = "Accessing"
        miro.delete_feed(reg, feed)
        #Set Global Preferences
        miro.open_prefs(reg)
        prefs = PreferencesPanel()
        podcasts_tab = prefs.open_tab("Podcasts")
        podcasts_tab.autodownload_setting("Off")
        podcasts_tab.default_view_setting("List")
        podcasts_tab.close_prefs()
        

        time.sleep(2)      
        #add feed and download joo joo item
        miro.add_feed(reg, url,feed)
        miro.tab_search(reg, title1)
        #double-click starts download
        reg.m.find(title1)
        title_loc = reg.m.getLastMatch()
        doubleClick(title_loc)
        if reg.m.exists("video-download-pause.png"):
            miro.log_result("122","list view double-click starts download")
        else:
            self.fail("list view double-click starts download, failed")
        #double-click pauses download
        doubleClick(title_loc)
        if reg.m.exists("video-download-resume.png"):
            miro.log_result("122","list view double-click pauses download")
        else:
            self.fail("list view double-click pause download, failed")
        #double-click resumes download
        doubleClick(title_loc)
        if exists("video-download-pause.png"):
            miro.log_result("122","list view double-click resumes download")
        else:
            self.fail("list view double-click resume download, failed")
        #double-click starts playback
        miro.wait_for_item_in_tab(reg, tab="Videos",item=title1)
        miro.click_podcast(reg, feed)
        miro.tab_search(reg, title1)
        doubleClick(title1)
        if exists(Pattern("playback_bar_video.png")):
            miro.log_result("122","list view double-click starts playback")
        else:
            self.fail("list view double-click start playback, failed")
        miro.verify_video_playback(reg)
        #cleanup
        miro.delete_feed(reg, feed)



    def test_647(self):
        """http://litmus.pculture.org/show_test.cgi?id=647 edit item metadata

        1. add Static List feed
        2. download the Earth Eats item
        3. Edit item metadata
       

        """
        reg = MiroRegions() 
        miro = MiroApp()
        time.sleep(5)

        miro.open_prefs(reg)
        prefs = PreferencesPanel()
        general_tab = prefs.open_tab("General")
        general_tab.show_audio_in_music("on")
        general_tab.close_prefs()
        
        url = "http://pculture.org/feeds_test/list-of-guide-feeds.xml"
        feed = "Static"
        term = "Earth Eats"
        title = "Mushroom" # item title updates when download completes
        new_type = "Video"

        edit_itemlist = [["name", "Earth Day Everyday", "647"],
                      ["artist", "Oliver and Katerina", "648"],
                      ["album", "Barki Barks", "649"],
                      ["genre", "family", "650"],
                      ["rating", "5", "651"],
                      ["year", "2010",  "655"],
                      ["track_num", "1", "673"],
                      ["track_of", "2", "673"],
                      ]
        
        #start clean
        miro.delete_feed(reg, feed)
        #add feed and download earth eats item
        miro.add_feed(reg, url,feed)
        miro.toggle_normal(reg)
        miro.tab_search(reg, term)
        if reg.m.exists("button_download.png",10):
            click(reg.m.getLastMatch())
        miro.wait_for_item_in_tab(reg, "Music",item=title)
        reg.m.click(title)
        for x in edit_itemlist:
            miro.edit_item_metadata(reg, meta_field=x[0],meta_value=x[1])
            miro.log_result(x[2],"test_647")
            time.sleep(2)
            if not miro.tab_search(reg, "Earth Day",confirm_present=True) == True:
                self.fail("new title not saved")
        #cleanup
        miro.delete_feed(reg, feed)
       

    def test_657(self):
        """http://litmus.pculture.org/show_test.cgi?id=657 edit multiple fields

        1. add Static List feed
        2. download the Earth Eats item
        3. Edit item metadata
       

        """
        try:
            reg = MiroRegions()
            miro = MiroApp()
            time.sleep(5)
            url = "http://ringtales.com/nyrss.xml"
            feed = "The New"
            title = "Cat" 

            new_metadata_list = [
                ["show","Animated Cartoons", "658"],
                ["episode_id","nya", "670"],
                ["season_no","25", "671"],
                ["episode_no","43", "672"],
                ["video_kind","Clip", "652"],
                ]
            
            #start clean
            miro.delete_feed(reg, feed)
            #add feed and download earth eats item
            miro.add_feed(reg, url,feed)
            miro.toggle_normal(reg)
            miro.tab_search(reg, title)
            if reg.m.exists("button_download.png",10):
                click(reg.m.getLastMatch())
            miro.wait_for_item_in_tab(reg, "Videos",item=title)
            miro.click_podcast(reg, feed)
            miro.tab_search(reg, title)
            reg.m.click(title)
            miro.edit_item_video_metadata_bulk(reg, new_metadata_list)
            time.sleep(2)
            miro.click_sidebar_tab(reg, "Videos")
            miro.tab_search(reg, title)
            reg.mtb.click("Clip")
            if reg.m.exists(title):
                reg.mtb.click("All")
            else:
                self.fail("item not found in Clips filter")
        
        finally:
            miro.quit_miro(reg)
            myLib.config.set_def_db_and_prefs()

                                     
 
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv, ).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite, ).litmus_test_run()
   
