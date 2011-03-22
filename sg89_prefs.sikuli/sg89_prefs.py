import sys
import os
import glob
import unittest
import StringIO
import time


sys.path.append(os.path.join(os.getcwd(),'myLib'))
import config
import mirolib
import prefs
import testvars
import litmusresult

setBundlePath(config.get_img_path())




class Miro_Suite(unittest.TestCase):
    """Subgroup 89 - preferences tests.

    """
    def setUp(self):
        self.verificationErrors = []
        setAutoWaitTimeout(3)
        
        
         

    def test_467(self):
        """http://litmus.pculture.org/show_test.cgi?id=467 change sys language.

        1. Open Preferences
        2. Change the system default language
        3. Restart Miro
        4. Verify changes and reset
        5. Restart Miro
        
        """
        reg = mirolib.AppRegions()


        try:
            #1. open preferences
            p = prefs.open_prefs(self)
            prefs.open_tab(self,p,"general")
            #2. change language to croatian (hr)
            p.click("System default")
            
            self.assertTrue(p.exists("pref_lang_hr.png"))
            click(p.getLastMatch())
            mirolib.shortcut("w")
            #3. Restart Miro
            mirolib.quit_miro(self,reg)
            switchApp(mirolib.open_miro())
            wait("Miro",45)
            click(getLastMatch())
            #4. Verify Changes and reset
            p = prefs.open_prefs(self,'hr','Datoteka','Postavke')       
            self.assertTrue(p.exists("pref_language_pulldown.png"))
            click(p.getLastMatch())
            self.assertTrue(p.exists("pref_lang_def.png"))
            click(p.getLastMatch())
            mirolib.shortcut("w")
            #5. Restart Miro
            mirolib.quit_miro(self,reg)
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

