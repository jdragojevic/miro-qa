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
import testvars
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
        miroRegions = mirolib.launch_miro()
        s = miroRegions[0] #Sidebar Region
        m = miroRegions[1] #Mainview Region
        t = miroRegions[2] #top half screen
        tl = miroRegions[3] #top left quarter
        try:
            item_url = "http://youtorrent.com/download/7379834/young-broke-and-fameless-the-mixtape.torrent"
            tl.click("File")
            tl.click("Download")
            time.sleep(4)
            type(item_url+"\n")
            status = mslib.confirm_download_started(self,m,s,"Young Broke")
            if status == "downloaded":
                mslib.delete_items(self,m,s,"Young Broke","video")
            elif status == "in_progress":
                mslib.delete_items(self,m,s,"Young Broke","downloading")
            else:
                self.fail("Can not confirm download started")
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

