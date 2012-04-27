import sys
import unittest
import time
from sikuli.Sikuli import *
import base_testcase
import myLib.config
from myLib.miro_regions import MiroRegions
from myLib.miro_app import MiroApp
import myLib.testvars

class Test_Sites(base_testcase.Miro_unittest_testcase):
    """Subgroup 21 - Sites.

    """
    def test_182(self):
        """http://litmus.pculture.org/show_test.cgi?id=182 dl from youtube site.

        1. Open youtube url as site
        2. download button
        3. verify download started
        4. Cleanup
        """
        site_url = "http://www.youtube.com/watch?v=fgg2tpUVbXQ&feature=channel"
        site = "Hubble"
        
        reg = MiroRegions() 
        miro = MiroApp()
        try:
            miro.add_source_from_tab(reg, site_url)
            miro.click_last_source(reg)
            
            if reg.mtb.exists(Pattern("download_this_video.png")) or \
                      reg.mtb.exists("Download this"):
                click(reg.mtb.getLastMatch())
                time.sleep(3)
            miro.confirm_download_started(reg, "Deep")
            try:
                reg.mtb.click("download-cancel.png")
            except:
                pass
        finally:
            miro.delete_site(reg, site)



    def test_194(self):
        """http://litmus.pculture.org/show_test.cgi?id=194 rename source.

        1. Add blip.tv as a source
        2. rename
        3. restart and verify name persists
        4. Cleanup
        """
        site_url = "http://blip.tv"
        site = "blip"
        reg = MiroRegions() 
        miro = MiroApp()

        miro.add_source(reg, site_url,site)
        miro.click_source(reg, site)
        reg.t.click("Sidebar")
        reg.t.click("Rename")
        time.sleep(3)
        type("BLIP TV ROCKS \n")
        self.assertTrue(reg.s.exists("BLIP TV ROCKS"))

        miro.quit_miro()
        reg = MiroRegions() 
        miro = MiroApp()
        self.assertTrue(reg.s.exists("BLIP"))
        miro.delete_site(reg, "BLIP")


    def stest_39(self):
        """http://litmus.pculture.org/show_test.cgi?id=39 site navigation.


        #skipping for now will fix later.
        
        1. Add blip.tv as a source
        2. navigate through site
        3. verify nav buttons and states
        4. Cleanup
        """
        site_url = "http://blip.tv"
        site = "blip"
        reg = MiroRegions() 
        miro = MiroApp()
        miro.add_source(reg, site_url,site)
        miro.click_source(reg, site)
        time.sleep(10)

        find("navstop_disabled.png")
        find("navforward_disabled.png")
        find("navhome.png")
        find("navreload.png")

        reg.m.click(myLib.testvars.blip_browse)
        reg.m.click(myLib.testvars.blip_recent)
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
        miro.delete_site(reg, site)
        

    def test_191(self):
        """http://litmus.pculture.org/show_test.cgi?id=191 Add rss feed to sidebar.

        1. Add ClearBits.net as a source
        2. Open Netlabel Music page and add RSS feed
        3. Verify feed added to the sidebar
        4. Cleanup
        """
        site_url = "http://clearbits.net"
        site = "ClearBits"
        feed = "ClearBits"
        reg = MiroRegions() 
        miro = MiroApp()
        miro.add_source(reg, site_url,site)
        miro.click_source(reg, site)
        reg.m.click("Netlabel Music")
        reg.m.click(myLib.testvars.clearbits_rss)
        miro.click_podcast(reg, site)
        miro.log_result("29","test_191 verify 1-click add site from source.")
        time.sleep(3)
        miro.delete_feed(reg, feed)
        miro.delete_site(reg, site)
        
        


    def test_193(self):
        """http://litmus.pculture.org/show_test.cgi?id=193 torrent direct dl.

        1. Add clearbits.net page as a source
        2. click to dl the torrent file
        3. Verify file starts to download
        4. Cleanup
        """
        site_url = "http://www.clearbits.net/torrents/662-here-be-dragons-ipod"
        site = "ClearBits"
        title = "Dragons"
                        
        reg = MiroRegions() 
        miro = MiroApp()
        miro.cancel_all_downloads(reg)

        miro.add_source(reg, site_url,site)
        miro.click_source(reg, site)
        reg.m.click("Torrent file")
        miro.confirm_download_started(reg, title)

        miro.cancel_all_downloads(reg)
        miro.delete_site(reg, site)


    def skip_192(self):
        """http://litmus.pculture.org/show_test.cgi?id=192 file detection dl.

        1. Add clearbits.net page as a source
        2. click to dl the torrent file
        3. Verify file starts to download
        4. Cleanup
        """
        site_url = "http://pculture.org/feeds_test/http-direct-downloads.html"
        site = "HTTP Direct"

        ## FIX ME - Need new files, can't download from the videolan ftp site anymore
        HTTPDOWNLOADS = {".mpFour download":"big",
                         ".mpThree download":"gd",
                         ".mFoura download":"luckynight",
            #             ".mpeg download":"mighty",
            #             ".ogv download":"popeye",
            #             ".mov download":"Matrix",
            #             ".wmv download":"WindowsMedia",
            #             ".avi download":"Coyote",
            #             ".mpg download":"dothack2",
            #            ".mkv download 2":"mulitple",
            #             ".ogg download":"gd",       
            #            ".wma download":"Bangles",            
            #            ".flac download":"luckynight",
            #            ".mka download":"Widow",
                         }
        reg = MiroRegions() 
        miro = MiroApp()

        miro.add_source(reg, site_url,site)
        miro.click_source(reg, site)
        for filetype, title in HTTPDOWNLOADS.iteritems():
            try:
                if reg.m.exists(filetype):
                    click(reg.m.getLastMatch())
                else:
                    type(Key.PAGE_DOWN)
                    reg.m.find(filetype)
                    click(reg.m.getLastMatch())
                if miro.confirm_download_started(reg, title) == "failed":
                    self.verificationErrors.append("download failed for imagetype" +str(filetype))
                else:
                    miro.cancel_all_downloads(reg)
                miro.click_source(reg, site)
            except:
                self.verificationErrors.append("download failed for imagetype" +str(filetype))
            finally:
                type(Key.ESC) #Close any lingering dialogs
                miro.cancel_all_downloads(reg)
                miro.delete_site(reg, site)

    def test_321(self):
        """http://litmus.pculture.org/show_test.cgi?id=321 delete slow to load site.

        1. Add slow feed as a source
        2. delete it before is loads
        """
        site_url = "http://pculture.org/feeds_test/slowsite.php"
        site = "pculture"
        alt_site = "Miro Guide"
        
        setAutoWaitTimeout(60)                
        reg = MiroRegions() 
        miro = MiroApp()

        miro.add_source_from_tab(reg, site_url)
        miro.click_last_source(reg)
        type(Key.DELETE)
        type(Key.ENTER)
        miro.handle_crash_dialog(db=False,test=False)

    def test_195(self):
        """http://litmus.pculture.org/show_test.cgi?id=196 delete site.

        1. Add header test as a source
        2. delete it 
        """
        site_url = "http://pculture.org/feeds_test/header-test.php"
        site = "Header Test"
        reg = MiroRegions() 
        miro = MiroApp()

        miro.add_source(reg, site_url,site)
        miro.delete_site(reg, site)

    def test_194(self):
        """http://litmus.pculture.org/show_test.cgi?id=194 site with non-utf-8 chars.

        1. Add http://pculture.org/feeds_test/test-guide-unicode.html 
        2. Verify added
        3. Restart and verify still there
        4. Cleanup
        """
        
        site_url = "http://pculture.org/feeds_test/test-guide-unicode.html"
        site = "Awesome"            
        reg = MiroRegions() 
        miro = MiroApp()
        miro.add_source_from_tab(reg, site_url)
        miro.click_last_source(reg)
        reg.m.find("unicode")
        miro.quit_miro()
        miro.restart_miro()
        miro.click_last_source(reg)
        self.assertTrue(reg.m.exists("unicode")
        miro.delete_site(reg, site)


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
        site2 = "Internet"
        reg = MiroRegions() 
        miro = MiroApp()

        miro.add_source(reg, site_url,site)
        miro.add_source(reg, site_url2,site2)
        p = miro.get_sources_region(reg)
        p.click(site)
        keyDown(Key.SHIFT)
        p.click(site2)
        keyUp(Key.SHIFT)
        if reg.m.exists("Delete All",5) or \
           reg.m.exists(Pattern("button_mv_delete_all.png"),5):
            click(reg.m.getLastMatch())
        else:
            self.fail("Delete All button for multi-select not found")
        miro.remove_confirm(reg, "cancel")
        time.sleep(3)
        p = miro.get_sources_region(reg)
        time.sleep(3)
        self.assertTrue(p.exists(site))
        self.assertTrue(p.exists(site2))

        #Cleanup
        miro.delete_site(reg, site)
        miro.delete_site(reg, site2)
        
# TestRunner posts output in xunit format
if __name__ == "__main__":
    from TestRunner import TestRunner
    TestRunner(Test_Sites).run_tests()
   




