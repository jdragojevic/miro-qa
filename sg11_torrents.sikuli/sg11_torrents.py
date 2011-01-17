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
import myvars
import litmusresult



setBundlePath(config.get_img_path())


class Miro_Suite(unittest.TestCase):
    """Subgroup 41 - one-click subscribe tests.

    """
    def setUp(self):
        self.verificationErrors = []
        setAutoWaitTimeout(60)
        switchApp(mirolib.open_miro())
         


    def test_419(self):
        """http://litmus.pculture.org/show_test.cgi?id=419 add feed.

        1. youtorrent dl link
        2. open with miro
        3. Verify download started and metadata
        4. Cleanup

        Test assumes that browser is configured to automatically open .torrent files with Miro
        """
        try:
            print "open ff"
            switchApp(mirolib.open_ff())
            item_url = "http://youtorrent.com/download/7379834/young-broke-and-fameless-the-mixtape.torrent"
            mirolib.shortcut("l")
            type(item_url + "\n")
            wait(testvars.one_click_badge)
            
            switchApp(mirolib.open_miro())
            self.assertTrue(exists(feed))
            click(feed)
        finally: 
            mirolib.delete_feed(self,feed)

        
            
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

