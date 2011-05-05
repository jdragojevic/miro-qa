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
    """Subgroup 31 - playback tests.

    """
    def test_160(self):
        """http://litmus.pculture.org/show_test.cgi?id=160.

        1. File -> Open
        2. Select video file on system
        3. Verify playback starts and item added to Library
        4. Cleanup - just remove from Library
        """
        
        reg = mirolib.AppRegions()

        
        try:
            vid_path = os.path.join(mycwd,"TestData","short-video.ogv")
            mirolib.shortcut('o')
            time.sleep(4)
            type(vid_path+"\n")
            self.assertTrue(exists("playback_controls.png"))
            mirolib.shortcut("d")
        except FindFailed, debugging:
            self.verificationErrors.append(debugging)
        except AssertionError:
            raise
        finally:
            type(Key.ESC)

        
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv,config.testlitmus).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite,config.testlitmus).litmus_test_run()
   

