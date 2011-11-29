import sys
import unittest
import time
from sikuli.Sikuli import *
import base_testcase
import myLib.config
from myLib.miro_regions import MiroRegions
from myLib.miro_app import MiroApp
from myLib.preferences_panel import PreferencesPanel



class Miro_Suite(base_testcase.Miro_unittest_testcase):
    """Subgroup 2 - remember last search

    """             
    def test_82(self):
        """http://litmus.pculture.org/show_test.cgi?id=82 remember last search.

        1. Perform a search
        2. Click off the tab
        3. Click back and verify the search is remembered.
        4. Cleanup
        """
       
        reg = MiroRegions() 
        miro = MiroApp()

        SEARCHES = {"blip": 'octopus', "YouTube": 'cosmicomics'}
        for engine, term in SEARCHES.iteritems():
            miro.click_sidebar_tab(reg, "Search")
            miro.search_tab_search(reg, term, engine)
            miro.click_sidebar_tab(reg, "Videos")
            miro.click_sidebar_tab(reg, "Search")
            self.assertTrue(reg.mtb.exists(term.upper()))


        
    def test_322(self):
        """http://litmus.pculture.org/show_test.cgi?id=322 search and save as a podcast

        1. Perform a search
        2. Click off the tab
        3. Click back and verify the search is remembered.
        4. Cleanup
        """
        setAutoWaitTimeout(60)
        reg = MiroRegions() 
        miro = MiroApp()
        
        #Set Global Preferences

        miro.open_prefs(reg)
        prefs = PreferencesPanel()
        podcasts_tab = prefs.open_tab("Podcasts")
        podcasts_tab.autodownload_setting("Off")
        podcasts_tab.close_prefs()       

        searches = {"blip": "python", "YouTube": "cosmicomics", "Revver": "Beiber", "Yahoo": "Canada", "DailyMotion": "Russia", "Metavid": "africa", "Mininova": "Creative Commons", "Video": "Toronto"}
        for engine, term in searches.iteritems():
            miro.click_sidebar_tab(reg, "search")
            miro.search_tab_search(reg, term,engine)
            time.sleep(10)
            reg.mtb.click("button_save_as_podcast.png")
            if engine == "blip":
                saved_search = engine
            else:
                saved_search = engine +" for"
            time.sleep(10) #give some time for everything to load up
            miro.click_podcast(reg, saved_search)
            miro.shortcut("r")
            time.sleep(5)
            miro.get_podcasts_region(reg)
            miro.tab_search(reg, term)
            try:
                self.assertTrue(reg.m.exists(engine))
                miro.delete_feed(reg, engine)
            except:
                 miro.log_result("322","test 322, failed for " +engine+": "+term,status="fail")
        #cleanup
        for x in searches.keys():
            miro.delete_feed(reg, x)


    def test_80(self):

        """http://litmus.pculture.org/show_test.cgi?id=80 Search - New Search Channel: URL
        1.Select Sidebar -> New Search Podcast
        2.Enter the search term: MP3
        3.Select the URL radio button and enter, http://www.ubu.com in the text box
        4.Click Create Podcast
        5.In the warning dialog - click Yes.
        """

        reg = MiroRegions() 
        miro = MiroApp()
        source = "http://www.ubu.com"
        term =  "mp3"
        search_term = "Gertrude"
        radio = "URL"
        miro.new_search_feed(reg, term,radio,source,defaults=False,watched=False)
        if exists("compatible",45):
            type(Key.ENTER)
        time.sleep(30)  # scraping takes a while - need to wait before confirming element present.
        miro.click_sidebar_tab(reg, "Podcasts")
        miro.tab_search(reg, search_term,confirm_present=True)
        miro.delete_feed(reg, term)  


    def test_79(self):
        """http://litmus.pculture.org/show_test.cgi?id=79 Search - New Search Podcast: Engine
        Steps to Perform:

        1.  Select Sidebar -> New Search Podcast
        2.  Enter a search term
        3.  Select the Search Engine radio button
        4.  Select a search engine from the pulldown menu
        5.  Select Create Podcast
        """

        reg = MiroRegions() 
        miro = MiroApp()

        #Set Global Preferences
        miro.open_prefs(reg)
        prefs = PreferencesPanel()
        podcasts_tab = prefs.open_tab("Podcasts")
        podcasts_tab.autodownload_setting("Off")
        podcasts_tab.close_prefs()
        
        searches = { "Yahoo": "Canada", "DailyMotion": "Ontario", "YouTube": "toronto"}
        radio = "Search"
        for source, term in searches.iteritems():
            miro.new_search_feed(reg, term,radio,source,defaults=False,watched=False)
            time.sleep(10) #give some time for everything to load up
            miro.click_podcast(reg, source)
            miro.shortcut("r")
            time.sleep(5)
            miro.tab_search(reg, term)
            try:
                self.assertTrue(reg.m.exists(source))
                miro.delete_feed(reg, source)
            except:
                 miro.log_result("79","test_79, failed for " +source+": "+term, status="fail")
        
        #cleanup
        for x in searches.keys():
            miro.delete_feed(reg, x)
   
# Post the output directly to Litmus
if __name__ == "__main__":
    import LitmusTestRunner
    print len(sys.argv)
    if len(sys.argv) > 1:
        LitmusTestRunner.LitmusRunner(sys.argv, ).litmus_test_run()
    else:
        LitmusTestRunner.LitmusRunner(Miro_Suite, ).litmus_test_run()
   


