import sys
import os
import glob
import unittest
import StringIO
import time

mycwd = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro")
sys.path.append(os.path.join(mycwd,'myLib'))
import config
import mirolib
import testvars
import litmusresult

setBundlePath(config.get_img_path())


class Miro_Suite(unittest.TestCase):
    """Subgroup 31 - playback tests.

    """
    def setUp(self):
        self.verificationErrors = []

    def test_160(self):
        """http://litmus.pculture.org/show_test.cgi?id=160.

        1. File -> Open
        2. Select video file on system
        3. Verify playback starts and item added to Library
        4. Cleanup - just remove from Library
        """
        
        miroApp = App("Miro")
        setAutoWaitTimeout(60)
        miroRegions = mirolib.launch_miro()
        s = miroRegions[0] #Sidebar Region
        m = miroRegions[1] #Mainview Region
        t = miroRegions[2] #top half screen
        tl = miroRegions[3] #top left quarter

        
        try:
            vid_path = os.path.join(mycwd,"TestData","short-video.ogv")
            reg.tl.click("File")
            reg.tl.click("Open")
            time.sleep(4)
            type(video_path+"\n")
            self.assertTrue(exists("playback_controls.png"))
            mirolib.shortcut("d")
        finally:
            pass
            #FIXME - should delete item, but only remove from the library
        
            
    def tearDown(self):
        self.assertEqual([], self.verificationErrors)
        
        
# Post the output directly to Litmus
if config.testlitmus == True:
    suite_list = unittest.getTestCaseNames(Miro_Suite,'test')
    suite = unittest.TestSuite()
    for x in suite_list:
        suite.addTest(Miro_Suite(x))

    buf = StringIO.StringIO()
    runner = unittest.TextTestRunner(stream=buf)
    litmusresult.write_header(config.get_os_name())
    for x in suite:
        runner.run(x)
        # check out the output
        byte_output = buf.getvalue()
        id_string = str(x)
        stat = byte_output[0]
        try:
            litmusresult.write_log(id_string,stat,byte_output)
        finally:
            buf.truncate(0)
    litmusresult.write_footer()
#or just run it locally
else:
    unittest.main()

