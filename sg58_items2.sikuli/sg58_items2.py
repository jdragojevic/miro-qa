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
import miro_regions
import prefs
import testvars
import base_testcase

class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 58 - Items - more tests.

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

    def test_653(self):
        """http://litmus.pculture.org/show_test.cgi?id=653 edit album art

        1. add watched folder
        2. Edit artwork for 1 item
        3. Edit artwork for multiple items
        4. Cleanup
        """
        
        reg = miro_regions.MiroRegions()
        time.sleep(5)
        folder_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","ArtTest")
        title = "Pancakes"
        title2 = "summer"
        title3="deerhunter"
        
        #1. add watched folder
        mirolib.add_watched_folder(self,reg,folder_path)
        if reg.s.exists("ArtTest"):
            click(reg.s.getLastMatch())          
            mirolib.log_result("157","test_653")
        art_file = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","album_art1.jpg")    
        #add feed and download flip face item
        mirolib.toggle_normal(reg)
        mirolib.tab_search(self,reg,title)
        try:
            reg.m.click(title)
            mirolib.edit_item_metadata(self,reg,meta_field="art",meta_value=art_file)
            ## Verify new image here:
            reg.m.find(Pattern("album_art1.png"))
        finally:
            prefs.remove_watched_folder(self,reg,folder=folder_path)
            
        
    def test_728(self):
        """http://litmus.pculture.org/show_test.cgi?id=728 edit metadata for mulitple items

        1. add Static List feed
        2. download the Earth Eats item
        3. Edit item metadata
       

        """
        reg = miro_regions.MiroRegions()
        time.sleep(5)
        prefs.set_item_display(self,reg,option="audio",setting="on")
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
            try:
                mirolib.log_result(x[2],"test_647")
            finally:
                time.sleep(2)
        if not mirolib.tab_search(self,reg,"Earth Day",confirm_present=True) == True:
            self.fail("new title not saved")
        #cleanup
        mirolib.delete_feed(self,reg,feed)

        

    def test_441(self):
        """http://litmus.pculture.org/show_test.cgi?id=441 delete podcast item outside of miro

        1. add TwoStupid feed
        2. download the Flip Faceitem
        3. restart miro
        4. delete the item
        5. restart miro
        6. verify item still deleted
        """
        reg = miro_regions.MiroRegions()
        remember = False
        try:
            prefs.set_preference_checkbox(self,reg,tab="General",option="When starting",setting="on")
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
        mirolib.wait_for_item_in_tab(self,reg,tab="Videos",item=title)
        mirolib.click_podcast(self,reg,feed)
        mirolib.tab_search(self,reg,title)
        reg.m.click(title)     
        filepath = mirolib.store_item_path(self,reg)
        if os.path.exists(filepath):
            print "able to verify on os level"
            found_file = True
        mirolib.quit_miro(self,reg)
        mirolib.restart_miro()
        if remember == True and reg.m.exists("title",15):  #check the remember last tab setting
            mirolib.log_result("698","test_441")
        else:
            mirolib.click_podcast(self,reg,feed)
        mirolib.tab_search(self,reg,title)
        reg.m.click(title)
        type(Key.DELETE)

        if found_file == True:
            if os.path.exists(filepath):
                self.fail("file not deleted from filesystem")
        else:
            mirolib.quit_miro(self,reg)
            mirolib.restart_miro()
            mirolib.click_podcast(self,reg,feed)
            mirolib.tab_search(self,reg,term)
            if not reg.m.exists(Pattern("button_download.png")):
                self.fail("no download button, file not deleted")
            else:
                reg.m.click(Pattern("button_download.png"))
            if mirolib.confirm_download_started(self,reg,title) != "in_progress":
                self.fail("item not properely deleted")    
        #cleanup
        mirolib.delete_feed(self,reg,feed)


  

    def test_725(self):
        """http://litmus.pculture.org/show_test.cgi?id=725 item click actions, list view.

        1. add 3-blip-videos feed
        2. download the Joo Joo
        3. verify varios item click scenerios

        """
        reg = miro_regions.MiroRegions()
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



    def test_647(self):
        """http://litmus.pculture.org/show_test.cgi?id=647 edit item metadata

        1. add Static List feed
        2. download the Earth Eats item
        3. Edit item metadata
       

        """
        reg = miro_regions.MiroRegions()
        time.sleep(5)
        prefs.set_item_display(self,reg,option="audio",setting="on")
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
       

    def test_657(self):
        """http://litmus.pculture.org/show_test.cgi?id=657 edit multiple fields

        1. add Static List feed
        2. download the Earth Eats item
        3. Edit item metadata
       

        """
        try:
            reg = miro_regions.MiroRegions()
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
            mirolib.delete_feed(self,reg,feed)
            #add feed and download earth eats item
            mirolib.add_feed(self,reg,url,feed)
            mirolib.toggle_normal(reg)
            mirolib.tab_search(self,reg,title)
            if reg.m.exists("button_download.png",10):
                click(reg.m.getLastMatch())
            mirolib.wait_for_item_in_tab(self,reg,"Videos",item=title)
            mirolib.click_podcast(self,reg,feed)
            mirolib.tab_search(self,reg,title)
            reg.m.click(title)
            mirolib.edit_item_video_metadata_bulk(self,reg,new_metadata_list)
            time.sleep(2)
            mirolib.click_sidebar_tab(self,reg,"Videos")
            mirolib.tab_search(self,reg,title)
            reg.mtb.click("Clip")
            if reg.m.exists(title):
                reg.mtb.click("All")
            else:
                self.fail("item not found in Clips filter")
        
        finally:
            mirolib.quit_miro(self,reg)
            config.set_def_db_and_prefs()

                                     
 
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv, ).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite, ).litmus_test_run()
   
