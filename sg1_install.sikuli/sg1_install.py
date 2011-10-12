import sys
import os
import unittest
import time
from sikuli.Sikuli import *
import base_testcase
import myLib.config
from myLib.miro_regions import MiroRegions
from myLib.miro_app import MiroApp

class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 1 - Install tests - going to delete preferences and database, and video storage before running each test case.

    """

    def setUp(self):
    
        miro = MiroApp()
        self.verificationErrors = []
        print "starting test: ",self.shortDescription()
        myLib.config.set_image_dirs()
        miro.quit_miro()
        myLib.config.set_def_db_and_prefs()
        miro.restart_miro()
        time.sleep(10)
        

            
    def test_4(self):
        """http://litmus.pculture.org/show_test.cgi?id=4 1st time install, specify a dir to search.

        Litmus Test Title:: 4 - 1st time install, specify a dir to search
        Description: 
        1. Clean up Miro support and vidoes directories
        2. Launch - walk through 1st tieme install dialog and search everywhere
        """
        reg = MiroRegions()
        miro = MiroApp()
        miro.quit_miro()
        myLib.config.delete_database_and_prefs()
        myLib.config.delete_miro_video_storage_dir()
        #set the search regions
        miro.restart_miro()
        search_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData")
        miro.first_time_startup_dialog(lang="Default",run_on_start="No",search="Yes",search_path=search_path,itunes="No")
        time.sleep(10)
        reg = MiroRegions()
        miro = MiroApp()
        miro.click_sidebar_tab(reg, "Videos")
        miro.tab_search(reg, title="Deerhunter",confirm_present=True)



    def test_5(self):
        """http://litmus.pculture.org/show_test.cgi?id=5 update install.

        Litmus Test Title:: 5 - upgrade from an earlier version of miro (3.5.1)
        Description: 
        1. Copy in Miro 3.5.1 database
        2. Launch miro and verify it is upgraded to current version.
        """
        
        miro = MiroApp()
        miro.quit_miro()
        db = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","databases","351sqlitedb")
        myLib.config.replace_database(db)
        #set the search regions
        miro.restart_miro()
        waitVanish("Upgrading")
        waitVanish("Preparing")
        time.sleep(10)
        miro.handle_crash_dialog('5', db=False, test=False)
        reg = MiroRegions()
        miro = MiroApp()
        
        miro.click_sidebar_tab(reg, "Downloading")
        miro.quit_miro()
        myLib.config.set_def_db_and_prefs()
        


    def test_17556_5(self):
        """http://litmus.pculture.org/show_test.cgi?id=5 update install from recoverably bad db, upgrade_80, bz 17556.

        Litmus Test Title:: 5 - upgrade from an earlier version of miro (3.5.1)
        Description: 
        1. Copy in Miro 3.5.1 database
        2. Launch miro and verify it is upgraded to current version.
        """
        miro = MiroApp()
        miro.quit_miro()
        db = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","databases","bz17556_backup80")
        myLib.config.replace_database(db)
        time.sleep(5)
        #set the search regions
        miro.restart_miro()
        waitVanish("Upgrading")
        waitVanish("Preparing")
        time.sleep(10)
        miro.quit_miro()
        myLib.config.reset_preferences()
        miro.restart_miro()
        reg = MiroRegions()
        miro = MiroApp()
        miro.click_podcast(reg, "Starter")


    def test_173(self):
        """http://litmus.pculture.org/show_test.cgi?id=173 1st time install, search everywhere

        Litmus Test Title:: 173 - 1st time install, search everywhere
        Description: 
        1. Clean up Miro support and vidoes directories
        2. Launch - walk through 1st tieme install dialog and search everywhere
        """
        miro = MiroApp()
        miro.quit_miro()
        myLib.config.delete_database_and_prefs()
        myLib.config.delete_miro_video_storage_dir()
        #set the search regions
        miro.restart_miro()      
        search_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData")
        miro.first_time_startup_dialog(lang="Default",run_on_start="No",search="Yes",search_path="Everywhere",itunes="No")
        time.sleep(10)
        reg = MiroRegions()
        miro = MiroApp()
        miro.click_sidebar_tab(reg, "Videos")
        find(Pattern("sort_name_normal.png").exact())
        doubleClick(getLastMatch().below(100))
        miro.verify_video_playback(reg)

    


    def test_88_460(self):
        """http://litmus.pculture.org/show_test.cgi?id=460 upgrade corrupt db submit crash with db

        Litmus Test Title:: 460 - upgrade with corrupted db submit crash report with db
        Description: 
        1. Replace Miro db with a corrupt database.
        2. Launch miro and submit crash report with db
        """
        try:
            reg = MiroRegions()
            miro = MiroApp()
            miro.quit_miro()
            db = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","databases","corrupt_db")
            myLib.config.replace_database(db)
            #set the search regions
            miro.restart_miro()
            miro.corrupt_db_dialog(action="submit_crash",db=True)
        finally:
            miro.quit_miro()
            myLib.config.set_def_db_and_prefs()



    def test_88_461(self):
        """http://litmus.pculture.org/show_test.cgi?id=461 upgrade corrupt db, submit crash no db

        Litmus Test Title:: 461 - upgrade with corrupted db, submit crash no db
        Description: 
        1. Replace Miro db with a corrupt database.
        2. Launch miro and submit crash report with db
        """
        try:
            miro = MiroApp()
            miro.quit_miro()
            db = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","databases","corrupt_db")
            myLib.config.replace_database(db)
            #set the search regions
            miro.restart_miro()
            miro.corrupt_db_dialog(action="submit_crash",db=False)
        finally:
            miro.quit_miro()
            myLib.config.set_def_db_and_prefs()
        

    def test_88_462(self):
        """http://litmus.pculture.org/show_test.cgi?id=461 upgrade corrupt db, start fresh

        Litmus Test Title:: 461 - upgrade with corrupted db, submit crash no db
        Description: 
        1. Replace Miro db with a corrupt database.
        2. Launch miro and submit crash report with db
        """
        try:
            miro = MiroApp()
            miro.quit_miro()
            db = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","databases","corrupt_db")
            myLib.config.replace_database(db)
            #set the search regions
            miro.corrupt_db_dialog(action="quit")
            time.sleep(5)
            miro.restart_miro()
            miro.corrupt_db_dialog(action="start_fresh")
        finally:
            miro.quit_miro()
            myLib.config.set_def_db_and_prefs()
            
        
        
    def test_999reset(self):
        """fake test to reset db and preferences.

        """
        miro = MiroApp()
        miro.quit_miro()
        myLib.config.set_def_db_and_prefs()
        miro.restart_miro()
        

if __name__ == "__main__":
    import LitmusTestRunner
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv, ).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite, ).litmus_test_run()


