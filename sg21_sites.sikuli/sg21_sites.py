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
        setAutoWaitTimeout(60)


    def test_182(self):
        """http://litmus.pculture.org/show_test.cgi?id=182 dl from youtube site.

        1. Open youtube url as site
        2. download button
        3. verify download started
        4. Cleanup
        """
        site_url = "http://www.youtube.com/watch?v=fgg2tpUVbXQ&feature=channel"
        site = "YouTube"
        
        reg = mirolib.AppRegions()

        mirolib.add_website(self,s,tl,site_url,site)
        reg.s.click(site)
        reg.m.find("download_this_video.png")
        self.assertTrue(reg.t.exists("download_this_video.png"))
        reg.t.click("download_this_video.png")
        mirolib.confirm_download_started(self,m,s,"Hubble")
        mirolib.delete_site(self,m,s,site)

    def test_194(self):
        """http://litmus.pculture.org/show_test.cgi?id=194 rename source.

        1. Add blip.tv as a source
        2. rename
        3. restart and verify name persists
        4. Cleanup
        """
        site_url = "http://blip.tv"
        site = "blip.tv (since 2005)"
        reg = mirolib.AppRegions()

        mirolib.add_website(self,s,tl,site_url,site)
        reg.s.click(site)
        reg.t.click("Sidebar")
        reg.t.click("Rename")
        time.sleep(3)
        type("BLIP.TV ROCKS \n")
        self.assertTrue(reg.s.exists("BLIP.TV ROCKS"))

        mirolib.quit_miro(self,m,s)
        miroRegions = mirolib.launch_miro()
        s = miroRegions[0] #Sidebar Region
        self.assertTrue(reg.s.exists("BLIP.TV ROCKS"))

        mirolib.delete_site(self,m,s,"BLIP.TV")


    def test_39(self):
        """http://litmus.pculture.org/show_test.cgi?id=39 site navigation.

        1. Add blip.tv as a source
        2. navigate through site
        3. verify nav buttons and states
        4. Cleanup
        """
        site_url = "http://blip.tv"
        site = "blip.tv (since 2005)"
        reg = mirolib.AppRegions()
        mirolib.add_website(self,s,tl,site_url,site)
        reg.s.click(site)

        self.assertTrue(reg.mtb.exists("navstop_disabled.png"))
        self.assertTrue(reg.mtb.exists("navforward_disabled.png"))
        self.assertTrue(reg.mtb.exists("navhome.png"))
        self.assertTrue(reg.mtb.exists("navreload.png"))

        reg.m.click(testvars.blip_browse)
        reg.m.click(testvars.blip_recent)
        self.assertTrue(reg.mtb.exists("navback.png"))
        self.assertTrue(reg.mtb.exists("navforward_disabled.png"))
        self.assertTrue(reg.mtb.exists("navhome.png"))
        self.assertTrue(reg.mtb.exists("navreload.png"))

        reg.mtb.click("navback.png")
        self.assertTrue(reg.mtb.exists("navforward.png"))
        self.assertTrue(reg.mtb.exists("navback_disabled.png"))
        self.assertTrue(reg.mtb.exists("navhome.png"))
        self.assertTrue(reg.mtb.exists("navreload.png"))

        reg.mtb.click("navforward")
        self.assertTrue(reg.mtb.exists("navback.png"))
        self.assertTrue(reg.mtb.exists("navforward_disabled.png"))
        self.assertTrue(reg.mtb.exists("navhome.png"))
        self.assertTrue(reg.mtb.exists("navreload.png"))
        
        reg.mtb.click("navreload.png")
        reg.mtb.click("navstop.png")
        self.assertTrue(reg.mtb.exists("navback.png"))
        self.assertTrue(reg.mtb.exists("navforward.png"))
        self.assertTrue(reg.mtb.exists("navhome.png"))
        self.assertTrue(reg.mtb.exists("navreload.png"))

        reg.mtb.click("navhome.png")
        #FIX MEwait for the updating icon to appear then disappear
        self.assertTrue(reg.mtb.exists("navback.png"))
        self.assertTrue(reg.mtb.exists("navforward_disabled.png"))
        self.assertTrue(reg.mtb.exists("navhome.png"))
        self.assertTrue(reg.mtb.exists("navreload.png"))
        



        mirolib.delete_site(self,m,s,site)
        

    def test_191(self):
        """http://litmus.pculture.org/show_test.cgi?id=191 Add rss feed to sidebar.

        1. Add clearbits.net as a source
        2. Open Netlabel Music page and add RSS feed
        3. Verify feed added to the sidebar
        4. Cleanup
        """
        site_url = "http://clearbits.net"
        site = "ClearBits"
        reg = mirolib.AppRegions()
        mirolib.add_website(self,s,tl,site_url,site)
        reg.s.click(site)
        reg.m.click("Netlabel Music")
        reg.m.click(testvars.clearbits_rss)
        self.assertTrue(reg.s.exists("Netlabel"))
        mirolib.delete_feed(self,m,s,"Netlabel")
        mirolib.delete_site(self,m,s,"ClearBits")


    def test_193(self):
        """http://litmus.pculture.org/show_test.cgi?id=193 torrent direct dl.

        1. Add clearbits.net page as a source
        2. click to dl the torrent file
        3. Verify file starts to download
        4. Cleanup
        """
        site_url = "http://www.clearbits.net/torrents/662-here-be-dragons-ipod"
        site = "ClearBits"
        title = "Brian Dunning"
                        
        reg = mirolib.AppRegions()

        mirolib.add_website(self,s,tl,site_url,site)
        reg.s.click(site)
        reg.m.click("Torrent file")
        mirolib.confirm_download_started(self,m,s,title)

        mirolib.delete_items(self,m,s,title,"Downloading")
        mirolib.delete_site(self,m,s,"ClearBits")


    def test_192(self):
        """http://litmus.pculture.org/show_test.cgi?id=192 file detection dl.

        1. Add clearbits.net page as a source
        2. click to dl the torrent file
        3. Verify file starts to download
        4. Cleanup
        """
        site_url = "http://pculture.org/feeds_test/http-direct-downloads.html"
        site = "HTTP Direct Downloads"
        HTTPDOWNLOADS = {".mpeg download":"mighty_mouse",
                         ".ogv download":"popeye",
                         ".mp4 download":"the_big_bad_wolf",
                         ".mov download":"Matrix_Reloaded",
                         ".wmv download":"WindowsMedia",
                         ".avi download":"Coyote.Ugly",
                         ".mpg download":"dothack2",
                         ".mkv download 2":"mulitple sub sample",
                         ".ogg download":"gd",
                         ".mp3 download":"gd",
                         ".wma download":"Bangles",
                         ".m4a download":"luckynight",
                         ".flac download":"luckynight",
                         ".mka download":"Widow",
                         }

        reg = mirolib.AppRegions()

        mirolib.add_website(self,s,tl,site_url,site)
        reg.s.click(site)
        for filetype, title in HTTPDOWNLOADS.iteritems():
            try:
                if reg.m.exists(filetype):
                    click(m.getLastMatch())
                else:
                    type(Key.PAGE_DOWN)
                    reg.m.find(filetype)
                    click(m.getLastMatch())
                mslib.confirm_download_started(self,m,s,title)
            except:
                self.verificationErrors.append("download failed for imagetype" +str(x))
            finally:
                mslib.cancel_all_downloads(self,m,s,reg.mtb)
        mirolib.delete_site(self,m,s,site)

    def test_321(self):
        """http://litmus.pculture.org/show_test.cgi?id=321 delete slow to load site.

        1. Add slow feed as a source
        2. delete it before is loads
        """
        site_url = "http://pculture.org/feeds_test/slowsite.php"
        site = "slowsite"
                        
        reg = mirolib.AppRegions()

        mirolib.add_website(self,s,tl,site_url,site)
        mirolib.delete_site(self,m,s,site)

    def test_195(self):
        """http://litmus.pculture.org/show_test.cgi?id=196 delete site.

        1. Add header test as a source
        2. delete it 
        """
        site_url = "http://pculture.org/feeds_test/header-test.php"
        site = "Header Test"
                        
        reg = mirolib.AppRegions()

        mirolib.add_website(self,s,tl,site_url,site)
        mirolib.delete_site(self,m,s,site)

    def test_194(self):
        """http://litmus.pculture.org/show_test.cgi?id=196 site with non-utf-8 chars.

        1. Add http://diziizle.net/
        2. Verify added
        3. Restart and verify still there
        4. Cleanup
        """
        site_url = "http://diziizle.net/"
        site = "http://diziizle"
                        
        reg = mirolib.AppRegions()
        mirolib.add_website(self,s,tl,site_url,site)
        reg.s.click(site)
        reg.m.find(testvars.dizizle_logo)
        mirolib.quit_miro(self,m,s)
        miroRegions = mirolib.launch_miro()
        s = miroRegions[0] #Sidebar Region
        m = miroRegions[1] #Mainview Region
        reg.s.click(site)
        self.assertTrue(reg.m.exists(testvars.dizizle_logo))    
        mirolib.delete_site(self,m,s,site)


    def test_143(self):
        """http://litmus.pculture.org/show_test.cgi?id=143 multiple delete and cancel.

        1. Add clearbits and archive.org
        2. select bogh and delete, the cancel
        3. verify sites not deleted.
        4. Cleanup
        """
        site_url = "http://clearbits.net"
        site_url2 = "http://archive.org"
        site = "ClearBits"
        site2 = "archive.org"
        reg = mirolib.AppRegions()

        mirolib.add_website(self,s,tl,site_url,site)
        mirolib.add_website(self,s,tl,site_url2,site2)
        reg.s.click(site)
        keyDown(SHIFT_KEY)
        reg.s.click(site2)
        keyUp(SHIFT_KEY)
        self.assertTrue(reg.m.exists("Delete All"))
        click(m.getLastMatch())
        reg.m.click("button_cancel.png")
        mslib.click_sidebar_tab(self,m,s,"Videos")
        self.assertTrue(reg.s.exists(site1))
        self.assertTrue(reg.s.exists(site2))

        #Cleanup
        mirolib.delete_site(self,m,s,site)
        mirolib.delete_site(self,m,s,site2)
        
    def tearDown(self):
        mirolib.handle_crash_dialog(self)
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

