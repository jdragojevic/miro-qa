import sys
import os
import shutil
import glob
import unittest
import StringIO
import time
import subprocess
from sikuli.Sikuli import *

mycwd = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro")
sys.path.append(os.path.join(mycwd,'myLib'))
import base_testcase
import config
import mirolib
import prefs
import testvars

class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 1 - Install tests - going to delete preferences and database, and video storage before running each test case.

    """
            
        
            
    def test_4(self):
        """http://litmus.pculture.org/show_test.cgi?id=4 1st time install, specify a dir to search.

        Litmus Test Title:: 4 - 1st time install, specify a dir to search
        Description: 
        1. Clean up Miro support and vidoes directories
        2. Launch - walk through 1st tieme install dialog and search everywhere
        """
        if exists("Miro",3) or \
           exists("Music",3):
            click(getLastMatch())
        mirolib.quit_miro(self)
        if config.get_os_name() == "osx":
            time.sleep(20)
        config.delete_database_and_prefs()
        config.delete_miro_video_storage_dir()
        setAutoWaitTimeout(testvars.timeout)
        #set the search regions
        mirolib.restart_miro(confirm=False)
        search_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData")
        mirolib.first_time_startup_dialog(self,lang="Default",run_on_start="No",search="Yes",search_path=search_path,itunes="No")
        reg = mirolib.AppRegions()
        time.sleep(10)
        mirolib.click_sidebar_tab(self,reg,"Videos")
        mirolib.tab_search(self,reg,title="Deerhunter",confirm_present=True)
        mirolib.click_sidebar_tab(self,reg,"Music")
        mirolib.tab_search(self,reg,title="Pancakes",confirm_present=True)
        

    def test_173(self):
        """http://litmus.pculture.org/show_test.cgi?id=173 1st time install, search everywhere

        Litmus Test Title:: 173 - 1st time install, search everywhere
        Description: 
        1. Clean up Miro support and vidoes directories
        2. Launch - walk through 1st tieme install dialog and search everywhere
        """
        if exists("Miro",3) or \
           exists("Music",3):
            click(getLastMatch())
        mirolib.quit_miro(self)
        if config.get_os_name() == "osx":
            time.sleep(20)
        config.delete_database_and_prefs()
        config.delete_miro_video_storage_dir()
        setAutoWaitTimeout(testvars.timeout)
        #set the search regions
        mirolib.restart_miro(confirm=False)
        search_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData")
        mirolib.first_time_startup_dialog(self,lang="Default",run_on_start="No",search="Yes",search_path="Everywhere",itunes="No")
        reg = mirolib.AppRegions()
        time.sleep(10)
        mirolib.click_sidebar_tab(self,reg,"Videos")
        find(Pattern("sort_name_normal.png").exact())
        doubleClick(getLastMatch().below(100))
        mirolib.verify_video_playback(self,reg)
##        mirolib.click_sidebar_tab(self,reg,"Music")            
##        mirolib.toggle_normal(reg)
##        find(Pattern("sort_name_normal.png").exact())
##        doubleClick(getLastMatch().below(100))
##        if reg.m.exists(Pattern("item_currently_playing.png")):
##            click(reg.m.getLastMatch())
##            shortcut("d")
##            reg.m.waitVanish("item_currently_playing.png",20)
##        else:
##            self.fail("can not verify audio playback of imported files")
    

        
        

if __name__ == "__main__":
    import LitmusTestRunner
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()


