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
    """Subgroup 11 - Torrent tests.

    """
    def setUp(self):
        self.verificationErrors = []
        setAutoWaitTimeout(60)
         


    def test_419(self):
        """http://litmus.pculture.org/show_test.cgi?id=419 external torrent dl.

        1. clearbits torrent dl
        2. open with File Download menu
        3. Verify download started and metadata
        4. Cleanup

        """
        miroRegions = mirolib.launch_miro()
        s = miroRegions[0] #Sidebar Region
        m = miroRegions[1] #Mainview Region
        t = miroRegions[2] #top half screen
        tl = miroRegions[3] #top left quarter
        
        item_url = "http://youtorrent.com/download/7379834/young-broke-and-fameless-the-mixtape.torrent"
        item_title = "Fameless"
        tl.click("File")
        tl.click("Download")
        time.sleep(4)
        type(item_url+"\n")
        print ("confirm download started")
        status = mirolib.confirm_download_started(self,m,s,item_title)
        print status
        if status == "downloaded":
            mirolib.delete_items(self,m,s,item_title,"videos")
        elif status == "in_progress":
            mirolib.delete_items(self,m,s,item_title,"downloading")
        else:
            self.fail("Can not confirm download started")

 
 
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
            print "writing log"
            litmusresult.write_log(id_string,stat,byte_output)
        finally:
            buf.truncate(0)
    litmusresult.write_footer()
#or just run it locally
else:
    unittest.main()
