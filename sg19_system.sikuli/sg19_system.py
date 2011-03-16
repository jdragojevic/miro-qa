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
    """Subgroup 19 - system tests.

    """
    def setUp(self):
        self.verificationErrors = []
                


    def test_55(self):
        """http://litmus.pculture.org/show_test.cgi?id=55 Test Crash Reporter with DB.

        1. Perform a search of crash inducing text
        2. Submit crash dialog with db
        3. Quit Miro
        """
       
        setAutoWaitTimeout(60)
        miroRegions = mirolib.launch_miro()
        s = miroRegions[0] #Sidebar Region
        m = miroRegions[1] #Mainview Region
        t = miroRegions[2] #top half screen
        tl = miroRegions[3] #top left quarter
        mtb = miroRegions[4] #main title bar

        term ="LET'S TEST DTV'S CRASH REPORTER TODAY"
        mirolib.click_sidebar_tab(self,m,s,"search")
        mirolib.tab_search(self,m,s,term)
        time.sleep(2)
        type("\n")
        mirolib.handle_crash_dialog(self)
            
    def test_54(self):
        """http://litmus.pculture.org/show_test.cgi?id=54 Test Crash Reporter no DB.

        1. Perform a search of crash inducing text
        2. Submit crash dialog
        3. Quit Miro
        """
        print self.id()
        setAutoWaitTimeout(60)
        miroRegions = mirolib.launch_miro()
        s = miroRegions[0] #Sidebar Region
        m = miroRegions[1] #Mainview Region
        t = miroRegions[2] #top half screen
        tl = miroRegions[3] #top left quarter
        mtb = miroRegions[4] #main title bar

        term ="LET'S TEST DTV'S CRASH REPORTER TODAY"
        mirolib.click_sidebar_tab(self,m,s,"search")
        mirolib.tab_search(self,m,s,term)
        time.sleep(2)
        type("\n")
        mirolib.handle_crash_dialog(self,db=False) 
        
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

