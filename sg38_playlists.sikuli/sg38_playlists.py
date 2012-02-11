import sys
import os
import unittest
import time
from sikuli.Sikuli import *
import base_testcase
import myLib.config
from myLib.miro_regions import MiroRegions
from myLib.miro_app import MiroApp

class Test_Playlists(base_testcase.Miro_unittest_testcase):
    """Subgroup 38 - Playlists tests.

    """

    def setUp(self):
        """ All playlist tests require data. Going to add feed and watched folder at the start of the subgroup.

        """
        self.verificationErrors = []
        miro = MiroApp()
        print "starting test: ",self.shortDescription()
        myLib.config.set_image_dirs()
        miro.quit_miro()
        myLib.config.set_def_db_and_prefs()
        miro.restart_miro()
        time.sleep(10)
        reg = MiroRegions() 
        miro = MiroApp()
        feed = "TestData"
        folder_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData")
        miro.add_watched_folder(reg, folder_path)

    def test_225(self):
        """http://litmus.pculture.org/show_test.cgi?id=225 add several items to a new playlist.

        1. add a watched folder to get some items in the db
        2. select the items and create a new playlist from menu
        3. verify items in list
        4. repeat with context menu and verify

        """
        watched_feed = "TestData"
        playlist = "MIX LIST"
        reg = MiroRegions() 
        miro = MiroApp()
        miro.click_sidebar_tab(reg, "Podcasts")
        miro.toggle_normal(reg)
        miro.tab_search(reg, watched_feed)
        reg.m.click(Pattern("sort_name_normal.png"))
        item_list = ["Lego", "Pancake", "Deerhunter"]
        keyDown(Key.SHIFT)
        time.sleep(1)
        reg.m.click("Lego")
        reg.m.click("Deerhunter")
        keyUp(Key.SHIFT)
        miro.add_playlist(reg, playlist, style="shortcut")
        miro.toggle_normal(reg)
        for title in item_list:
            miro.tab_search(reg, title, confirm_present=True)

   
        
    def test_679(self):
        """http://litmus.pculture.org/show_test.cgi?id=679 create a playlist via menu.

        Also verifies test_222, remove playlist (via context menu)

        1. add a watched folder to get some items in the db
        2. select the items and create a new playlist from menu
        3. verify items in list
        4. repeat with context menu and verify

        """
        playlist = "EMPTY LIST"
        reg = MiroRegions() 
        miro = MiroApp()
        miro.add_playlist(reg, playlist,style="menu")
        p = miro.get_playlists_region(reg)
        list_loc = miro.click_playlist(reg, playlist)
        rightClick(Location(list_loc))
        p.click("Remove")
        miro.remove_confirm(reg, "remove")
        time.sleep(2)
        if p.exists(playlist):
            print "remove failed"
        else:
            miro.log_result("222","verified remove playlist via context menu")
        
        


    def test_221(self):
        """http://litmus.pculture.org/show_test.cgi?id=221 rename playlist.

        """
        playlist = "TAB LIST"
        reg = MiroRegions() 
        miro = MiroApp()
        miro.add_playlist(reg, playlist,style="tab")
        miro.log_result("708","test_221 - added playlist via Playlist top level tab")
        list_loc = miro.click_playlist(reg, playlist)
        print list_loc
        rightClick(Location(list_loc))
        type(Key.DOWN)
        type(Key.ENTER)
        time.sleep(2)
        type("NEW NAME \n")
        miro.click_playlist(reg, playlist="NEW NAME")
        
        
    def test_709(self):
        """http://litmus.pculture.org/show_test.cgi?id=709 create playlist from library search.

        1. add a watched folder to get some items in the db
        2. search in music tab
        3. click Add to Playist button
        4. accept name and verify created

        """
        watched_feed = "TestData"
        playlist = "Johnson"
        item_list = ["Pancakes","Horizon"]
        reg = MiroRegions() 
        miro = MiroApp()
        miro.click_sidebar_tab(reg, "Music")
        miro.tab_search(reg, playlist)
        reg.mtb.click(Pattern("button_save_as_playlist.png"))
        time.sleep(3)
        type(Key.ENTER)
        miro.click_playlist(reg, playlist.upper())
        miro.toggle_normal(reg)
        
        for title in item_list:
            miro.tab_search(reg, title,confirm_present=True)       
         

# TestRunner posts output in xunit format
if __name__ == "__main__":
    from TestRunner import TestRunner
    TestRunner(Test_Playlists).run_tests()
   

