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
sys.path.append(mycwd)
sys.path.append(os.path.join(mycwd,'myLib'))
import base_testcase
import config
import mirolib 
import miro_regions
import prefs
import testvars

class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 1 - Install tests - going to delete preferences and database, and video storage before running each test case.

    """

    def setUp(self):
        self.verificationErrors = []
        print "starting test: ",self.shortDescription()
        config.set_image_dirs()
        mirolib.quit_miro(self)
        config.set_def_db_and_prefs()
        mirolib.restart_miro(confirm=False)
        time.sleep(10)
        

            
    def test_4(self):
        """http://litmus.pculture.org/show_test.cgi?id=4 1st time install, specify a dir to search.

        Litmus Test Title:: 4 - 1st time install, specify a dir to search
        Description: 
        1. Clean up Miro support and vidoes directories
        2. Launch - walk through 1st tieme install dialog and search everywhere
        """
        reg = miro_regions.MiroRegions()
        mirolib.quit_miro(self)
        config.delete_database_and_prefs()
        config.delete_miro_video_storage_dir()
        setAutoWaitTimeout(testvars.timeout)
        #set the search regions
        mirolib.restart_miro(confirm=False)
        search_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData")
        mirolib.first_time_startup_dialog(self,lang="Default",run_on_start="No",search="Yes",search_path=search_path,itunes="No")
        time.sleep(10)
        reg = miro_regions.MiroRegions()
        mirolib.click_sidebar_tab(self,reg,"Videos")
        mirolib.tab_search(self,reg,title="Deerhunter",confirm_present=True)



    def test_5(self):
        """http://litmus.pculture.org/show_test.cgi?id=5 update install.

        Litmus Test Title:: 5 - upgrade from an earlier version of miro (3.5.1)
        Description: 
        1. Copy in Miro 3.5.1 database
        2. Launch miro and verify it is upgraded to current version.
        """
        
        
        mirolib.quit_miro(self)
        db = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","databases","351sqlitedb")
        config.replace_database(db)
        setAutoWaitTimeout(testvars.timeout)
        #set the search regions
        mirolib.restart_miro(confirm=False)
        waitVanish("Upgrading")
        waitVanish("Preparing")
        time.sleep(10)
        mirolib.handle_crash_dialog(self,db=False,test=False)
        reg = miro_regions.MiroRegions()
        
        mirolib.click_sidebar_tab(self,reg,"Downloading")
        mirolib.quit_miro(self,reg)
        config.set_def_db_and_prefs()
        


    def test_17556_5(self):
        """http://litmus.pculture.org/show_test.cgi?id=5 update install from recoverably bad db, upgrade_80, bz 17556.

        Litmus Test Title:: 5 - upgrade from an earlier version of miro (3.5.1)
        Description: 
        1. Copy in Miro 3.5.1 database
        2. Launch miro and verify it is upgraded to current version.
        """
        
        mirolib.quit_miro(self)
        db = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","databases","bz17556_backup80")
        config.replace_database(db)
        time.sleep(5)
        setAutoWaitTimeout(testvars.timeout)
        #set the search regions
        mirolib.restart_miro(confirm=False)
        waitVanish("Upgrading")
        waitVanish("Preparing")
        time.sleep(10)
        mirolib.quit_miro(self)
        config.reset_preferences()
        mirolib.restart_miro()
        reg = miro_regions.MiroRegions()
        mirolib.click_podcast(self,reg,"Starter")


    def test_173(self):
        """http://litmus.pculture.org/show_test.cgi?id=173 1st time install, search everywhere

        Litmus Test Title:: 173 - 1st time install, search everywhere
        Description: 
        1. Clean up Miro support and vidoes directories
        2. Launch - walk through 1st tieme install dialog and search everywhere
        """
        
        mirolib.quit_miro(self)
        config.delete_database_and_prefs()
        config.delete_miro_video_storage_dir()
        setAutoWaitTimeout(testvars.timeout)
        #set the search regions
        mirolib.restart_miro(confirm=False)      
        search_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData")
        mirolib.first_time_startup_dialog(self,lang="Default",run_on_start="No",search="Yes",search_path="Everywhere",itunes="No")
        time.sleep(10)
        reg = miro_regions.MiroRegions()
        mirolib.click_sidebar_tab(self,reg,"Videos")
        find(Pattern("sort_name_normal.png").exact())
        doubleClick(getLastMatch().below(100))
        mirolib.verify_video_playback(self,reg)

    


    def test_88_460(self):
        """http://litmus.pculture.org/show_test.cgi?id=460 upgrade corrupt db submit crash with db

        Litmus Test Title:: 460 - upgrade with corrupted db submit crash report with db
        Description: 
        1. Replace Miro db with a corrupt database.
        2. Launch miro and submit crash report with db
        """
        try:
            reg = miro_regions.MiroRegions()
            mirolib.quit_miro(self,reg)
            db = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","databases","corrupt_db")
            config.replace_database(db)
            setAutoWaitTimeout(testvars.timeout)
            #set the search regions
            mirolib.restart_miro(confirm=False)
            mirolib.corrupt_db_dialog(action="submit_crash",db=True)
        finally:
            mirolib.quit_miro(self)
            config.set_def_db_and_prefs()



    def test_88_461(self):
        """http://litmus.pculture.org/show_test.cgi?id=461 upgrade corrupt db, submit crash no db

        Litmus Test Title:: 461 - upgrade with corrupted db, submit crash no db
        Description: 
        1. Replace Miro db with a corrupt database.
        2. Launch miro and submit crash report with db
        """
        try:
            mirolib.quit_miro(self)
            db = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","databases","corrupt_db")
            config.replace_database(db)
            setAutoWaitTimeout(testvars.timeout)
            #set the search regions
            mirolib.restart_miro(confirm=False)
            mirolib.corrupt_db_dialog(action="submit_crash",db=False)
        finally:
            mirolib.quit_miro(self)
            config.set_def_db_and_prefs()
        

    def test_88_462(self):
        """http://litmus.pculture.org/show_test.cgi?id=461 upgrade corrupt db, start fresh

        Litmus Test Title:: 461 - upgrade with corrupted db, submit crash no db
        Description: 
        1. Replace Miro db with a corrupt database.
        2. Launch miro and submit crash report with db
        """
        try:
            mirolib.quit_miro(self)
            db = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","databases","corrupt_db")
            config.replace_database(db)
            setAutoWaitTimeout(testvars.timeout)
            #set the search regions
            mirolib.corrupt_db_dialog(action="quit")
            time.sleep(5)
            mirolib.restart_miro(confirm=False)
            mirolib.corrupt_db_dialog(action="start_fresh")
        finally:
            mirolib.quit_miro(self)
            config.set_def_db_and_prefs()
            
        
        
    def test_999reset(self):
        """fake test to reset db and preferences.

        """
        mirolib.quit_miro(self)
        config.set_def_db_and_prefs()
        mirolib.restart_miro(confirm=False)
        

if __name__ == "__main__":
    import LitmusTestRunner
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv, ).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite, ).litmus_test_run()


