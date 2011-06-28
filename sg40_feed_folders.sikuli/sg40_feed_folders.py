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
import prefs
import testvars

class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 40 - Feeds folders.

    """
 

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
        reg = mirolib.AppRegions()

        opml_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","folder-test.opml")
        feed = "Featured"
        folder = "geeky"
        feedlist = ["Google", "Make","geeky","Featured"]

        #1. Add the feeds 
        mirolib.import_opml(self,reg,opml_path)
   
        p = mirolib.get_podcasts_region(reg)
        mirolib.click_sidebar_tab(self,reg,"Music")
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
        mirolib.delete_feed(self,reg,"fun")



  
        

if __name__ == "__main__":
    import LitmusTestRunner
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()


