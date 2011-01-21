import sys
import os
import glob
import unittest
import StringIO
import time


mycwd = os.path.join(os.getcwd(),"Miro")
sys.path.append(os.path.join(mycwd,'myLib'))
import config
import mirolib
import menus
import testvars
import litmusresult






class Miro_Suite(unittest.TestCase):
    """Subgroup 89 - preferences tests.

    """
    def setUp(self):
        self.verificationErrors = []
        setAutoWaitTimeout(60)
        setBundlePath(config.get_img_path())
        
         

    def test_467(self):
        """http://litmus.pculture.org/show_test.cgi?id=467 change sys language.

        1. Open Preferences
        2. Change the system default language
        3. Restart Miro
        4. Verify changes and reset
        5. Restart Miro
        
        """
        miroApp = App("Miro")
        ffApp = App("Firefox")
        setAutoWaitTimeout(60)
        miroRegions = mirolib.launch_miro()
        s = miroRegions[0] #Sidebar Region
        m = miroRegions[1] #Mainview Region
        t = miroRegions[2] #top half screen
        tl = miroRegions[3] #top left quarter
        try:
            #1. open preferences
            mirolib.open_preferences(self,tl)
            click(testvars.pref_general)
            #2. change language to croatian (hr)
            click("System default")
            
            self.assertTrue(exists("pref_lang_hr.png"))
            click(getLastMatch())
            mirolib.shortcut("w")
            #3. Restart Miro
            mirolib.quit_miro(self)
            switchApp(mirolib.open_miro())           
            #4. Verify Changes and reset
            mirolib.open_preferences(self,'hr')
            self.assertTrue(exists("pref_language_pulldown.png"))
            click(getLastMatch())
            self.assertTrue(exists("pref_lang_def.png"))
            click(getLastMatch())
            mirolib.shortcut("w")
            #5. Restart Miro
            mirolib.quit_miro(self)
            switchApp(mirolib.open_miro())            
            
        finally:
            pass
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

