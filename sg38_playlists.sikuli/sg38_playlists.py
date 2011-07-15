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
import testvars
import base_testcase


class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 38 - Playlists tests.

    """

    def setUp(self):
        """ All playlist tests require data. Going to add feed and watched folder at the start of the subgroup.

        """
        self.verificationErrors = []
        print "starting test: ",self.shortDescription()
        config.set_image_dirs()
        mirolib.quit_miro(self)
        config.set_def_db_and_prefs()
        mirolib.restart_miro(confirm=False)
        time.sleep(10)
        reg = mirolib._AppRegions()
        feed = "TestData"
        folder_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData")
        mirolib.add_watched_folder(self,reg,folder_path)

    def test_225(self):
        """http://litmus.pculture.org/show_test.cgi?id=225 add several items to a new playlist.

        1. add a watched folder to get some items in the db
        2. select the items and create a new playlist from menu
        3. verify items in list
        4. repeat with context menu and verify

        """
        watched_feed = "TestData"
        playlist = "MIX LIST"
        reg = mirolib._AppRegions()
        mirolib.click_sidebar_tab(self,reg,"Podcasts")
        mirolib.toggle_normal(reg)
        mirolib.tab_search(self,reg,"Lego")
        reg.m.click("Lego")
        mirolib.tab_search(self,reg,watched_feed)
        reg.mr.click(Pattern("sort_name_normal.png"))
        item_list = ["Lego","Pancake","Deerhunter"]        
        selected_items = mirolib.multi_select(self,region=reg.m,item_list=item_list)
        mirolib.add_playlist(self,reg,playlist,style="shortcut")
        mirolib.toggle_normal(reg)
        for title in selected_items:
            mirolib.tab_search(self,reg,title,confirm_present=True)

   
        
    def test_679(self):
        """http://litmus.pculture.org/show_test.cgi?id=679 create a playlist via menu.

        Also verifies test_222, remove playlist (via context menu)

        1. add a watched folder to get some items in the db
        2. select the items and create a new playlist from menu
        3. verify items in list
        4. repeat with context menu and verify

        """
        playlist = "EMPTY LIST"
        reg = mirolib._AppRegions()
        mirolib.add_playlist(self,reg,playlist,style="menu")
        p = mirolib.get_playlists_region(reg)
        list_loc = mirolib.click_playlist(self,reg,playlist)
        rightClick(Location(list_loc))
        p.click("Remove")
        mirolib.remove_confirm(self,reg,"remove")
        time.sleep(2)
        if p.exists(playlist):
            print "remove failed"
        else:
            mirolib.log_result("222","verified remove playlist via context menu")
        
        


    def test_221(self):
        """http://litmus.pculture.org/show_test.cgi?id=221 rename playlist.

        """
        playlist = "TAB LIST"
        reg = mirolib._AppRegions()
        mirolib.add_playlist(self,reg,playlist,style="tab")
        mirolib.log_result("708","test_221 - added playlist via Playlist top level tab")
        list_loc = mirolib.click_playlist(self,reg,playlist)
        print list_loc
        rightClick(Location(list_loc))
        type(Key.DOWN)
        type(Key.ENTER)
        time.sleep(2)
        type("NEW NAME \n")
        mirolib.click_playlist(self,reg,playlist="NEW NAME")
        
        
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
        reg = mirolib._AppRegions()
        p = mirolib.get_podcasts_region(reg)
        mirolib.click_sidebar_tab(self,reg,"Music")
        mirolib.tab_search(self,reg,playlist)
        reg.mtb.click(Pattern("button_save_as_playlist.png"))
        time.sleep(3)
        type(Key.ENTER)
        mirolib.click_playlist(self,reg,playlist.upper())
        mirolib.toggle_normal(reg)
        
        for title in item_list:
            mirolib.tab_search(self,reg,title,confirm_present=True)       
         

# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()
   

