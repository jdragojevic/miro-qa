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
    """Subgroup 41 - one-click subscribe tests.

    """
    def setUp(self):
        self.verificationErrors = []

    def test_6(self):
        """http://litmus.pculture.org/show_test.cgi?id=6 add feed from MiroGuide.

        1. Open Miro
        2. search for a feed and add it.
        3. Verify feed added
        4. Cleanup
        """
        miroApp = App("Miro")
        setAutoWaitTimeout(60)
        
        #set the search regions
        miroRegions = mirolib.launch_miro()
        s = miroRegions[0] #Sidebar Region
        m = miroRegions[1] #Mainview Region
        t = miroRegions[2] #top half screen
        tl = miroRegions[3] #top left quarter
 
        try:
            reg.m.click(testvars.guide_search)
            type("StupidVideos \n")
            reg.m.find(testvars.guide_add_feed)
            click(m.getLastMatch())            self.assertTrue(s.exists("StupidVideos"))
                        
        finally:
            #4. cleanup
            mirolib.delete_feed(self,m,s,"StupidVideos") 

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

