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
    """Subgroup 31 - playback tests.

    """
    def test_160(self):
        """http://litmus.pculture.org/show_test.cgi?id=160.

        1. File -> Open
        2. Select video file on system
        3. Verify playback starts and item added to Library
        4. Cleanup - just remove from Library
        """
        
        reg = MiroRegions() 
        miro = MiroApp()

        
        try:
        
            vid_path = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","TestData","monkey.flv")
            miro.shortcut('o')
            miro.type_a_path(vid_path)
            time.sleep(3)
            self.assertTrue(exists(Pattern("playback_controls.png")))
            miro.shortcut("d")
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
        LitmusTestRunner.LitmusRunner(sys.argv, ).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite, ).litmus_test_run()
   

