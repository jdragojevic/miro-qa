import sys
import os
import unittest
import time
from sikuli.Sikuli import *
import base_testcase
import myLib.config
import myLib.testvars
from myLib.miro_regions import MiroRegions
from myLib.miro_app import MiroApp

class Test_Feed_Folders(base_testcase.Miro_unittest_testcase):
    """Subgroup 40 - Feeds folders.

    """

    def test_001setup(self):
        """Pre subgroup run cleanup and preferences check.

        This isn't a real tests and is just meant to make sure the subgroup is starting with usual preferences settings and clean sidebar.
        """
        miro = MiroApp()
        miro.quit_miro()
        myLib.config.set_def_db_and_prefs()
        miro.restart_miro()
        time.sleep(10)
        

    def test_116(self):
        """http://litmus.pculture.org/show_test.cgi?id=116 add multiple feeds to a folder

        Litmus Test Title:: 116 - add multiple feeds to a new folder
        Description: 
        1. Import 2 OPML file of some feeds and folders
        2. select several feeds and add to new folder
        3. confirm feeds in folders
        4. Cleanup
        """
        setAutoWaitTimeout(myLib.testvars.timeout)
        #set the search regions
        reg = MiroRegions() 
        miro = MiroApp()
        miro.delete_all_podcasts(reg)
        opml_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","folder-test.opml")
        opml_path2 = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","folder-test2.opml")
        feed_list =  ["Google", "Onion","two ronnies","Vimeo"]
        added_feeds = []
        new_folder = "multi folder"

        #1. Add the feeds 
        miro.import_opml(reg, opml_path)
        time.sleep(15) #give a chance to add and update
        miro.import_opml(reg, opml_path2)
        time.sleep(15) #give a chance to add and update
   
        
        #expand all the folders
        p = miro.get_podcasts_region(reg)
        miro.expand_feed_folder(reg, "GEEKY")
        miro.expand_feed_folder(reg, "FUN")
        #set the feeds region
        p = miro.get_podcasts_region(reg)
        #select multiple feeds for the folders
        p.click("BIRCHBOXTV")
        added_feeds = miro.multi_select(region=p,item_list=feed_list)
        if len(added_feeds) > 0:
            added_feeds.append("BIRCHBOXTV")
        else:
            self.fail("feeds not selected properly for adding to a folder")
        time.sleep(5)
        reg.m.click("New Folder")
        time.sleep(2)
        type(new_folder + "\n")
        time.sleep(5)
        feed_match = miro.click_podcast(reg, new_folder)
        rightClick(Location(feed_match))
        if exists("Update",2):
            click(getLastMatch())
        try:
            for feed in added_feeds:
                assert miro.tab_search(reg, title=feed,confirm_present=True), True
        except:
            self.fail("%s feed not found" % feed)
        finally:
            #cleanup
            miro.delete_all_podcasts(reg)
        




    def test_722(self):
        """http://litmus.pculture.org/show_test.cgi?id=722 delete feeds and folders confirm dialog.

        Litmus Test Title:: 722 - delete feeds confirm dialog
        Description: 
        1. Import OPML file of some feeds and folders
        2. 1 feed and 1 folder
        3. Delete, verify confirm dialog, and delete
        4. Cleanup
        """
        setAutoWaitTimeout(myLib.testvars.timeout)
        #set the search regions
        reg = MiroRegions() 
        miro = MiroApp()
        miro.delete_all_podcasts(reg)
        opml_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","folder-test.opml")
        feed = "Featured"
        folder = "GEEKY"
        feedlist = ["Google", "Make", "GEEKY", "Featured"]

        #1. Add the feeds 
        miro.import_opml(reg, opml_path)
   
        p = miro.get_podcasts_region(reg)
        miro.click_podcast(reg, feed)            
        #2. Select the folder too
        keyDown(Key.SHIFT)
        p.click(folder)
        keyUp(Key.SHIFT)
        #3. Delete
        type(Key.DELETE)
        for x in feedlist:
            miro.count_images(reg, img=x,region="main",num_expected=1)             
        type(Key.ENTER)
        time.sleep(2)
        #4. Cleanup
        miro.delete_all_podcasts(reg)
        p = miro.get_podcasts_region(reg)
        for x in feedlist:
            if not p.exists(x):
                miro.log_result("202","test_722")
        

    def test_196(self):
        """http://litmus.pculture.org/show_test.cgi?id=196 create new empty feed folder.

        Litmus Test Title:: 198 - new feed folder
        Description: 
        1. Import OPML file of some feeds and folders
        2. 1 feed and 1 folder
        3. Delete, verify confirm dialog, and delete
        4. Cleanup
        """
        setAutoWaitTimeout(myLib.testvars.timeout)
        #set the search regions
        folder = "GREAT STUFF"        
        reg = MiroRegions() 
        miro = MiroApp()
        reg.t.click("Sidebar")
        reg.t.click("Folder")
        time.sleep(2)
        type(folder + "\n")
        time.sleep(10) #give it 10 seconds to add the folder
        miro.click_podcast(reg, folder)       
        miro.delete_feed(reg, "GREAT")



    def test_197(self):
        """http://litmus.pculture.org/show_test.cgi?id=197 drag feeds to a folder

        Litmus Test Title:: 197 - drag feeds to a folder
        Description: 
        1. Import OPML file of some feeds and folders
        2. drag feeds to the folder
        3. verify feeds in folder
        4. Cleanup
        """
        setAutoWaitTimeout(myLib.testvars.timeout)
        miro = MiroApp()
        #set the search regions
        miro.quit_miro()
        myLib.config.set_def_db_and_prefs()
        miro.restart_miro()
        time.sleep(10)
        reg = MiroRegions() 
        miro = MiroApp()

        opml_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","folder-test2.opml")
        folder = "Best Feeds"
        feedlist = ["Vimeo", "BIRCHBOXTV"]

        #1. Add the feeds 
        miro.import_opml(reg, opml_path)
        p = miro.get_podcasts_region(reg)
        for feed in feedlist:
            x = p.find(feed)
            y = p.find(folder)
            dragDrop(x,y)
            time.sleep(2)
        feed_match = miro.click_podcast(reg, folder)
        rightClick(Location(feed_match))
        if exists("Update",2):
            click(getLastMatch())
        for feed in feedlist:
            miro.tab_search(reg, title=feed,confirm_present=True)
        #cleanup
        miro.delete_all_podcasts(reg)
            

    def test_198(self):
        """http://litmus.pculture.org/show_test.cgi?id=198 rename folder.

        Litmus Test Title:: 198 - rename feed folder
        Description: 
        1. Import OPML file of some feeds and folders
        2. 1 feed and 1 folder
        3. Delete, verify confirm dialog, and delete
        4. Cleanup
        """
        setAutoWaitTimeout(myLib.testvars.timeout)
        #set the search regions
        folder = "Great Stuff"
        new_name1 = "INCREDIBLE"
        new_name2 = "AWFUL"
        
        reg = MiroRegions() 
        miro = MiroApp()
        reg.t.click("Sidebar")
        reg.t.click("Folder")
        time.sleep(2)
        type(folder + "\n")
        time.sleep(10) #give it 10 seconds to add the folder
        miro.click_podcast(reg, feed=folder)
        time.sleep(3)
        reg.t.click("Sidebar")
        reg.t.click("Rename")
        time.sleep(2)
        type(new_name1 + "\n")
        miro.click_podcast(reg, feed=new_name1)
        miro.restart_miro()
        p = miro.get_podcasts_region(reg)
        if not p.exists(new_name1):
            self.fail("rename did not persist after restart")
        else:
            p.rightClick(new_name1)
            p1 = Region(p.getLastMatch().nearby(200))
            p1.click("Rename")
            time.sleep(2)
            type(new_name2 + "\n")
            miro.click_podcast(reg, feed=new_name2)
            
        miro.delete_feed(reg, new_name2)

    def test_199(self):
        """http://litmus.pculture.org/show_test.cgi?id=199 reorder folders in sidebar

        Litmus Test Title:: 199 - reorder folders in the sidebar
        Description: 
        1. Import OPML file of some feeds and folders
        2. drag feeds to the folder
        3. verify feeds in folder
        4. Cleanup
        """
        setAutoWaitTimeout(myLib.testvars.timeout)
        #set the search regions
        miro = MiroApp()
        miro.quit_miro()
        myLib.config.set_def_db_and_prefs()
        miro.restart_miro()
        time.sleep(10)
        reg = MiroRegions() 
        miro = MiroApp()

        opml_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","folder-test.opml")

        
        #1. Add the feeds 
        miro.import_opml(reg, opml_path)
        p = miro.get_podcasts_region(reg)
        x = p.find("GEEKY")
        y = p.find("Featured")
        dragDrop(x,y)
        time.sleep(2)
        p.click("Featured")
        ror = Region(p.getLastMatch().above(250))
        if not ror.exists("GEEKY"):
            self.fail("GEEKY folder not moved above 'Featured' podcast")

        #Cleanup - select all the podcasts and delete
        miro.delete_all_podcasts(reg)

     
    def test_999reset(self):
        """fake test to reset db and preferences.

        """
        miro = MiroApp()
        miro.quit_miro()
        myLib.config.set_def_db_and_prefs()
        miro.restart_miro()
        time.sleep(10)        
        

# TestRunner posts output in xunit format
if __name__ == "__main__":
    from TestRunner import TestRunner
    TestRunner(Test_Feed_Folders).run_tests()


