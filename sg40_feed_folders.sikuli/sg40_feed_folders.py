import sys
import os
import glob
import unittest
import StringIO
import time
from sikuli.Sikuli import *

mycwd = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro")
sys.path.append(os.path.join(mycwd,'myLib'))
import base_testcase
import config
import mirolib 
import miro_regions

import testvars

class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 40 - Feeds folders.

    """

    def test_001setup(self):
        """Pre subgroup run cleanup and preferences check.

        This isn't a real tests and is just meant to make sure the subgroup is starting with usual preferences settings and clean sidebar.
        """
        mirolib.quit_miro(self)
        config.set_def_db_and_prefs()
        mirolib.restart_miro(confirm=False)
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
        setAutoWaitTimeout(testvars.timeout)
        #set the search regions
        reg = miro_regions.MiroRegions()
        mirolib.delete_all_podcasts(self,reg)
        opml_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","folder-test.opml")
        opml_path2 = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","folder-test2.opml")
        feed_list =  ["Google", "Onion","two ronnies","Vimeo"]
        added_feeds = []
        new_folder = "multi folder"

        #1. Add the feeds 
        mirolib.import_opml(self,reg,opml_path)
        time.sleep(15) #give a chance to add and update
        mirolib.import_opml(self,reg,opml_path2)
        time.sleep(15) #give a chance to add and update
   
        
        #expand all the folders
        mirolib.expand_feed_folder(self,reg,"GEEKY")
        mirolib.expand_feed_folder(self,reg,"FUN")
        #set the feeds region
        p = mirolib.get_podcasts_region(reg)
        #select multiple feeds for the folders
        p.click("Birchbox")
        added_feeds = mirolib.multi_select(self,region=p,item_list=feed_list)
        if len(added_feeds) > 0:
            added_feeds.append("Birchbox")
        else:
            self.fail("feeds not selected properly for adding to a folder")
        time.sleep(5)
        reg.m.click("New Folder")
        time.sleep(2)
        type(new_folder + "\n")
        time.sleep(5)
        feed_match = mirolib.click_podcast(self,reg,new_folder)
        rightClick(Location(feed_match))
        if exists("Update",2):
            click(getLastMatch())
        
        
        for feed in added_feeds:
            mirolib.tab_search(self,reg,title=feed,confirm_present=True)
        #cleanup
        mirolib.delete_all_podcasts(self,reg)
        




    def test_722(self):
        """http://litmus.pculture.org/show_test.cgi?id=722 delete feeds and folders confirm dialog.

        Litmus Test Title:: 722 - delete feeds confirm dialog
        Description: 
        1. Import OPML file of some feeds and folders
        2. 1 feed and 1 folder
        3. Delete, verify confirm dialog, and delete
        4. Cleanup
        """
        setAutoWaitTimeout(testvars.timeout)
        #set the search regions
        reg = miro_regions.MiroRegions()
        mirolib.delete_all_podcasts(self,reg)
        opml_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","folder-test.opml")
        feed = "Featured"
        folder = "GEEKY"
        feedlist = ["Google", "Make","GEEKY","Featured"]

        #1. Add the feeds 
        mirolib.import_opml(self,reg,opml_path)
   
        p = mirolib.get_podcasts_region(reg)
        mirolib.click_podcast(self,reg,feed)            
        #2. Select the folder too
        keyDown(Key.SHIFT)
        p.click(folder)
        keyUp(Key.SHIFT)
        #3. Delete then cancel.  Verify still exists Static List
        type(Key.DELETE)
        for x in feedlist:
            mirolib.count_images(self,reg,img=x,region="main",num_expected=1)             
        type(Key.ENTER)
        time.sleep(2)
        #4. Cleanup
        mirolib.delete_all_podcasts(self,reg)
        p = mirolib.get_podcasts_region(reg)
        for x in feedlist:
            if not p.exists(x):
                mirolib.log_result("202","test_722")
        

    def test_196(self):
        """http://litmus.pculture.org/show_test.cgi?id=196 create new empty feed folder.

        Litmus Test Title:: 198 - new feed folder
        Description: 
        1. Import OPML file of some feeds and folders
        2. 1 feed and 1 folder
        3. Delete, verify confirm dialog, and delete
        4. Cleanup
        """
        setAutoWaitTimeout(testvars.timeout)
        #set the search regions
        folder = "GREAT STUFF"        
        reg = miro_regions.MiroRegions()
        reg.t.click("Sidebar")
        reg.t.click("Folder")
        time.sleep(2)
        type(folder + "\n")
        time.sleep(10) #give it 10 seconds to add the folder
        mirolib.click_podcast(self,reg,folder)       
        mirolib.delete_feed(self,reg,"GREAT")



    def test_197(self):
        """http://litmus.pculture.org/show_test.cgi?id=197 drag feeds to a folder

        Litmus Test Title:: 197 - drag feeds to a folder
        Description: 
        1. Import OPML file of some feeds and folders
        2. drag feeds to the folder
        3. verify feeds in folder
        4. Cleanup
        """
        setAutoWaitTimeout(testvars.timeout)
        #set the search regions
        mirolib.quit_miro(self)
        config.set_def_db_and_prefs()
        mirolib.restart_miro(confirm=False)
        time.sleep(10)
        reg = miro_regions.MiroRegions()

        opml_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","folder-test2.opml")
        folder = "Best Feeds"
        feedlist = ["Vimeo", "BirchboxTV"]

        #1. Add the feeds 
        mirolib.import_opml(self,reg,opml_path)
        p = mirolib.get_podcasts_region(reg)
        for feed in feedlist:
            x = p.find(feed)
            y = p.find(folder)
            dragDrop(x,y)
            time.sleep(2)
        feed_match = mirolib.click_podcast(self,reg,folder)
        rightClick(Location(feed_match))
        if exists("Update",2):
            click(getLastMatch())
        for feed in feedlist:
            mirolib.tab_search(self,reg,title=feed,confirm_present=True)
        #cleanup
        mirolib.delete_all_podcasts(self,reg)
            

    def test_198(self):
        """http://litmus.pculture.org/show_test.cgi?id=198 rename folder.

        Litmus Test Title:: 198 - rename feed folder
        Description: 
        1. Import OPML file of some feeds and folders
        2. 1 feed and 1 folder
        3. Delete, verify confirm dialog, and delete
        4. Cleanup
        """
        setAutoWaitTimeout(testvars.timeout)
        #set the search regions
        folder = "Great Stuff"
        new_name1 = "INCREDIBLE"
        new_name2 = "ThisSux"
        
        reg = miro_regions.MiroRegions()
        reg.t.click("Sidebar")
        reg.t.click("Folder")
        time.sleep(2)
        type(folder + "\n")
        time.sleep(10) #give it 10 seconds to add the folder
        mirolib.click_podcast(self,reg,feed=folder)
        time.sleep(3)
        reg.t.click("Sidebar")
        reg.t.click("Rename")
        time.sleep(2)
        type(new_name1 + "\n")
        mirolib.click_podcast(self,reg,feed=new_name1)
        mirolib.restart_miro()
        p = mirolib.get_podcasts_region(reg)
        if not p.exists(new_name1):
            self.fail("rename did not persist after restart")
        else:
            p.rightClick(new_name1)
            p1 = Region(p.getLastMatch().nearby(200))
            p1.click("Rename")
            time.sleep(2)
            type(new_name2 + "\n")
            mirolib.click_podcast(self,reg,feed=new_name2)
            
        mirolib.delete_feed(self,reg,new_name2)

    def test_199(self):
        """http://litmus.pculture.org/show_test.cgi?id=199 reorder folders in sidebar

        Litmus Test Title:: 199 - reorder folders in the sidebar
        Description: 
        1. Import OPML file of some feeds and folders
        2. drag feeds to the folder
        3. verify feeds in folder
        4. Cleanup
        """
        setAutoWaitTimeout(testvars.timeout)
        #set the search regions
        mirolib.quit_miro(self)
        config.set_def_db_and_prefs()
        mirolib.restart_miro(confirm=False)
        time.sleep(10)
        reg = miro_regions.MiroRegions()

        opml_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","folder-test.opml")

        
        #1. Add the feeds 
        mirolib.import_opml(self,reg,opml_path)
        p = mirolib.get_podcasts_region(reg)
        x = p.find("GEEKY")
        y = p.find("Featured")
        dragDrop(x,y)
        time.sleep(2)
        p.click("Featured")
        ror = Region(p.getLastMatch().above(250))
        if not ror.exists("Make"):
            self.fail("GEEKY folder not moved above 'Featured' podcast")

        #Cleanup - select all the podcasts and delete
        mirolib.delete_all_podcasts(self,reg)

     
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
        LitmusTestRunner.LitmusRunner(sys.argv, ).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite, ).litmus_test_run()


