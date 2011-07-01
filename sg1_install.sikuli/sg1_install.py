import sys
import os
import shutil
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
    """Subgroup 1 - Install tests - going to delete preferences and database, and video storage before running each test case.

    """
    def setUp(self):
        self.verificationErrors = []
        print "starting test: ",self.shortDescription()
        mirolib.quit_miro(self)

        #Delete Miro support dir
        miro_support_dir = config.get_support_dir()
        if os.path.exists(miro_support_dir):
            shutil.rmtree(miro_support_dir)
        else:
            print "***Warning: didn't find support dir***"
        #Delete Miro default video storage
        miro_video_dir = config.get_video_dir()
        if os.path.exists(miro_video_dir):
            shutil.rmtree(miro_video_dir)
        else:
            print "***Warning: didn't find videos dir***"
        
            

    def test_4(self):
        """http://litmus.pculture.org/show_test.cgi?id=4 1st time install, specify a dir to search.

        Litmus Test Title:: 4 - 1st time install, specify a dir to search
        Description: 
        1. Import 2 OPML file of some feeds and folders
        2. select several feeds and add to new folder
        3. confirm feeds in folders
        4. Cleanup
        """
        setAutoWaitTimeout(testvars.timeout)
        #set the search regions
        mirolib.restart_miro()
        reg = mirolib.AppRegions()
        search_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData")
       

        
        

if __name__ == "__main__":
    import LitmusTestRunner
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()


