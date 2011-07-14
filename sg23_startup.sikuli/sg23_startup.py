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
            
        
            
    def test_236(self):
        """http://litmus.pculture.org/show_test.cgi?id=236 startup, corrupt item_info_cache

        Litmus Test Title:: 236 - rebuild item_info_cache on startup.
        Description: 
        1. Clean up Miro support and vidoes directories
        2. Launch - walk through 1st tieme install dialog and search everywhere
        """

        reg = mirolib._AppRegions()
        folder_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData")
        mirolib.add_watched_folder(self,reg,folder_path)
        mirolib.quit_miro(self)
        if config.get_os_name() == "osx":
            time.sleep(20)
        config.delete_preferences()
        setAutoWaitTimeout(testvars.timeout)
        #set the search regions 
        mirolib.restart_miro(confirm=False)
        mirolib.first_time_startup_dialog(self,lang="Default",run_on_start="No",search="No",search_path=None,itunes="No")    
        waitVanish("Preparing")
        time.sleep(10)
        reg = mirolib._AppRegions()
        mirolib.click_sidebar_tab(self,reg,"Videos")
        mirolib.tab_search(self,reg,title="Deerhunter",confirm_present=True)


    def test_235(self):
        """http://litmus.pculture.org/show_test.cgi?id=235 startup missing movies dir, no downloads

        Litmus Test Title:: 235 - startup missing movies dir.
        Description: 
        1. delete movies dir, launch miro
        2. 
        """
        if exists("Miro",3) or \
           exists("Music",3):
            click(getLastMatch())
        mirolib.quit_miro(self)
        config.set_def_db_and_prefs()
        mirolib.restart_miro(confirm=True)
        mirolib.quit_miro(self)
        config.delete_miro_video_storage_dir()
        setAutoWaitTimeout(testvars.timeout)
        #set the search regions
        mirolib.restart_miro(confirm=True)
        reg = mirolib._AppRegions()



        
    def test_999reset(self):
        """fake test to reset db and preferences.

        """
        mirolib.quit_miro(self)
        config.set_def_db_and_prefs()
        mirolib.restart_miro(confirm=False)
        time.sleep(10)
        

if __name__ == "__main__":
    import LitmusTestRunner
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()


