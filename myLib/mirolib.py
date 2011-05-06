

#mirolib.py

import os
import time
import glob
import config
import testvars
from sikuli.Sikuli import *

#setBundlePath(config.get_img_path())



def open_miro():
    """Returns the launch path for the application.

    launch is an os specific command
    """
    if config.get_os_name() == "osx":
        return "/Applications/Miro.app"
    elif config.get_os_name() == "win":
        return "C:\\Program Files\\Participatory Culture Foundation\\Miro\\Miro.exe"
    elif config.get_os_name() == "lin":
        print "trying to run on linux - make sure MIRONIGHTLYDIR is set"
        return "linux"
    else:
        print config.get_os_name()

class AppRegions():
    def get_regions():
        regions = []
        if exists("Music",2):
            click(getLastMatch())
        elif exists("Videos",5):
            click(getLastMatch())
        libr = Region(getLastMatch().above(500))
        libr.click("Miro")
        if not exists(testvars.feedback,5):
            try:
                click("navhome.png")
                wait("navstop_disabled.png",15)
            except:
                pass
            print ("network either off or slow, no feeback icon")
            find("Videos")
            sidex = int(getLastMatch().getX())+200
        else:
            wait(testvars.feedback)
            sidex = getLastMatch().getX()

        find("Music")
        topx =  int(getLastMatch().getX())-55
        topy = int(getLastMatch().getY())-90
        
        find("BottomCorner.png")
        vbarx =  int(getLastMatch().getX())+30
        vbary = int(getLastMatch().getY())+10
        vbarw = getLastMatch().getW()

        sidebar_width = int(sidex-topx)
        app_height = int(vbary-topy)
        tbar_height = 100
        
        #Sidebar Region
        SidebarRegion = Region(topx,topy,sidebar_width,app_height)
        SidebarRegion.setAutoWaitTimeout(30)
        regions.append(SidebarRegion)                
        #Mainview Region
        mainwidth = int((vbarx-sidex)+vbarw)
        MainViewRegion = Region(sidex,topy+tbar_height,mainwidth,app_height-155)
        MainViewRegion.setAutoWaitTimeout(30)
        regions.append(MainViewRegion)
        #Top Half of screen, width of Miro app Region
        TopHalfRegion = Region(0,0,mainwidth+sidebar_width,app_height/2)
        TopHalfRegion.setAutoWaitTimeout(30)
        regions.append(TopHalfRegion)
        #Top Left Half of screen, 1/2 width of Miro app from left side
        TopLeftRegion = Region(0,0,mainwidth/2,app_height/2)
        TopLeftRegion.setAutoWaitTimeout(30)
        regions.append(TopLeftRegion)
        #Main Title bar section of the main view
        MainTitleBarRegion = Region(sidex,topy,mainwidth,tbar_height)
        MainTitleBarRegion.setAutoWaitTimeout(30)
        regions.append(MainTitleBarRegion)
        return regions




    def launch_miro():
        """Open the Miro Application, the sets the region coords for searching.
        
        Uses the Miro Guides, Feedback, Bottom Corner, and VolumeBar to find coordinates.
        Returns the:
            
        SidebarRegion (s) - miro sidebar 
        MainViewRegion(m) - miro mainview
        TopHalfRegion (t) - top 1/2 of whole screen
        TopLeftRegion (tl) - top left of whole screen
        MainTitleBarRegion (mtb) - miro mainview title bar region

        Note - order mattters, this would be better as a dict.
        """
        if open_miro() == "linux":
            config.start_miro_on_linux()
        else:
            App.open(open_miro())
        wait("Sidebar",45)

    config.set_image_dirs()
    launch_miro()
    setAutoWaitTimeout(testvars.timeout) 
    miroRegions = get_regions()
    s = miroRegions[0] #Sidebar Region
#    s.highlight(5)
    m = miroRegions[1] #Mainview Region
#    m.highlight(5)
    t= miroRegions[2] #top half screen
#    t.highlight(5)
    tl = miroRegions[3] #top left quarter
#    tl.highlight(5)
    mtb = miroRegions[4] #main title bar
#    mtb.highlight(5)
    miroapp = App("Miro")
      
        


def shortcut(key,shift=False):
    """Keyboard press of the correct shortcut key

    for os x = cmd + key
    for win and linux = ctrl + key

    """
    if shift == False:
        if config.get_os_name() == "osx":
            type(key,KEY_CMD)
        elif config.get_os_name() == "win":
            type(key,KEY_CTRL)
        elif config.get_os_name() == "lin":
            type(key,KEY_CTRL)
        else:
            print config.get_os_name()
            type(key,KEY_CTRL)
    else:
        if config.get_os_name() == "osx":
            type(key,KEY_CMD+KEY_SHIFT)
        elif config.get_os_name() == "win":
            type(key,KEY_CTRL+KEY_SHIFT)
        elif config.get_os_name() == "lin":
            type(key,KEY_CTRL+KEY_SHIFT)
        else:
            print config.get_os_name()
            type(key,KEY_CTRL+KEY_SHIFT)

    

def quit_miro(self,reg=None):
    if reg == None:
        shortcut("q")
        time.sleep(10)
    else:
        click_sidebar_tab(self,reg,"Videos")
        shortcut("q")
        while reg.m.exists("dialog_confirm_quit.png",5):
            reg.m.click("dialog_quit.png")
        self.assertFalse(reg.s.exists("Music",10))

def restart_miro(self,reg):
    if config.get_os_name() == "lin":
        config.start_miro_on_linux()
    else:
        reg.miroapp.focus()
    time.sleep(5)
    wait("Miro",45)    
    
def cmd_ctrl():
    """Based on the operating systems, returns the correct key modifier for shortcuts.
    
    """
    if config.get_os_name() == "osx":
        return "CMD"
    elif config.get_os_name() == "win":
        return "CTRL"
    else:
        print config.get_os_name()
        return "CTRL"


def open_ff():
    """Returns the launch path for the application.

    launch is an os specific command
    """
    if config.get_os_name() == "osx":
        return "/Applications/Firefox.app"
    elif config.get_os_name() == "win":
        return "C:\\Program Files\\Mozilla Firefox\\Firefox.exe"
    elif config.get_os_name() == "lin":
        config.start_ff_on_linux()
        return "firefox"
    else:
        print "no clue"

def close_ff():
    App.close("firefox")
    time.sleep(3)
    for x in range(0,2):
        while exists("Firefox",2):
            shortcut('w')
            time.sleep(2)
        


def toggle_radio(self,button):
    
    """Looks for the specified tab by image base name.
    Should be able to find the image if it is selected or not selected.
    """
    if noreg.t.exists (imagemap.Buttons[button +"_selected"]):
        click (imagemap.Buttons[(button)])   
 


def cclick(self,img,ddir=getBundlePath()):
    """Look through the image dir and click any image that matches the given name.

    """                                    
    for image in glob.glob(os.path.join(ddir, img+'*.png')):
        print image
        if exists(image,3):
            click(image)
            break


def close_one_click_confirm(self):
    """Close any os confirm dialogs when opening 1-click subscribe feeds."


    """
    if exists("sys_open_alert.png",30):
        click("sys_ok_button.png")

def remove_confirm(self,reg,action="remove"):
    """If the remove confirmation is displayed, remove or cancel.

    action = (remove_feed, remove_item or cancel)
    m = Mainview region from testcase
    need to add remove_library option
    """
    time.sleep(3)       
    if reg.m.exists("Remove",5) or \
       reg.m.exists(Pattern("dialog_are_you_sure.png"),3) or \
       reg.m.exists(Pattern("dialog_one_of_these.png"),3) or \
       reg.t.exists("Cancel",3)or \
       reg.t.exists(Pattern("dialog_are_you_sure.png"),3) or \
       reg.t.exists(Pattern("dialog_one_of_these.png"),3):
        
        print "got confirmation dialog"
        time.sleep(3)
        if action == "remove":
            print "clicking remove button"
            type(Key.ENTER)
        elif action == "delete_item":
            print "clicking delete button"
            if config.get_os_name() == "osx":
                reg.t.click("button_delete_file.png")
            else:
                reg.m.click("Delete File")
        elif action == "cancel":
            print "clicking cancel"
            type(Key.ESC)
        elif action == "keep":
            print "keeping"
            reg.m.click("Keep")
            type(Key.ENTER)
        else:
            print "not sure what to do in this dialog"
    
def get_sources_region(reg):
    """takes the main and sidebar regions to create a region for the websites section.
    
    """
    if not reg.s.exists("Sources",1):
        reg.s.click("Music")
    reg.s.click("Sources")
    topx =  reg.s.getX()
    topy =  reg.s.getLastMatch().getY()
    reg.s.find("Stores")
    boty =  reg.s.getLastMatch().getY()
    height = (boty-topy)+40
    width = reg.s.getW()
    SourcesRegion = Region(topx,topy, width, height)
    SourcesRegion.setAutoWaitTimeout(20)
    return SourcesRegion

def get_podcasts_region(reg):
    if not reg.s.exists("Podcasts",1):
        reg.s.click("Sources")
    reg.s.click("Podcasts")
    topx =  (reg.s.getLastMatch().getX())-10
    topy =  reg.s.getLastMatch().getY()
    reg.s.find("Playlists")
    boty =  reg.s.getLastMatch().getY()
    height = (boty-topy)+50
    width = reg.s.getW()
    PodcastsRegion = Region(topx,topy, width, height)
    PodcastsRegion.setAutoWaitTimeout(20)
    return PodcastsRegion
    
def get_playlists_region(reg):
    if not reg.s.exists("Playlists",1):
        reg.s.click("Podcasts")
    reg.s.click("Playlists")
    topx =  (reg.s.getLastMatch().getX())-10
    topy =  reg.s.getLastMatch().getY()
    width = reg.s.getW()
    PlaylistsRegion = Region(topx,topy, width, 600)
    PlaylistsRegion.setAutoWaitTimeout(20)
    return PlaylistsRegion     
	
    
def delete_site(self,reg,site):
    """Delete the video feed from the sidebar.
    feed = the feed name exact text that is displayed in the sidebar.
    m = Mainview Region, calculate in the testcase on launch.
    s = Sideview Region, calculated in the testcase on launch.

    """
    
    p = get_sources_region(reg)
    while p.exists(site,2):
        p.click(site)
        type(Key.DELETE)
        remove_confirm(self,reg,"remove")
        p = get_sources_region(reg)
        self.assertFalse(p.exists(site,5))     
    else:
        print "feed: " +site+ " not present"

def add_feed(self,reg,url,feed):
    """Add a feed to miro, click on it in the sidebar.
    
    Verify the feed is added by clicking on the feed and verify the feed name is present
    in the main title bar.
    """
    reg.t.click("Sidebar")
    reg.t.click("Add Podcast")
    time.sleep(2)
    type(url + "\n")
    time.sleep(10) #give it 10 seconds to add the feed
    click_podcast(self,reg,feed)
    
def click_podcast(self,reg,feed):
    """Find the podcast in the sidebar within podcast region and click on it.
    """
    p = get_podcasts_region(reg)
    time.sleep(3)
    self.assertTrue(p.exists(feed))
    click(p.getLastMatch())

def click_last_podcast(self,reg):
    """Based on the position of the Playlists tab, click on the last podcast in the list.

    This is useful if the title isn't displayed completely or you have other chars to don't work for text recognition.
    """
    p = get_podcasts_region(reg)
    time.sleep(5)
    p.find("Playlists")
    click(p.getLastMatch().above(35))

def click_misc(reg):
    if not reg.s.exists("Music",1):
        reg.s.click("Videos")
    reg.s.click("Music")
    p = Region(reg.s.getLastMatch().below(200))
    p.click("Misc")
    

def set_podcast_autodownload(self,reg,setting="Off"):
    """Set the feed autodownload setting using the button at the bottom of the mainview.

    """
    """Based on the position of the Playlists tab, click on the last podcast in the list.

    This is useful if the title isn't displayed completely or you have other chars to don't work for text recognition.
    """
    
    b = Region(reg.m.getX(),reg.m.getY()*2,reg.m.getW(), reg.m.getH())
    b.find("button_autodownload.png")
    b1 = Region(b.getLastMatch().right(80))
    for x in range(0,3):
        if not b1.exists(setting,2):
               click(b1.getLastMatch())
               time.sleep(2)

def open_podcast_settings(self,reg):
    b = Region(reg.s.getX(),reg.m.getY()*2,reg.m.getW(), reg.m.getH())
    b.find(Pattern("button_settings.png").exact())
    click(b.getLastMatch())

def change_podcast_settings(self,reg,option,setting):
    find("Expire Items")
    p1 = Region(getLastMatch().nearby(800))
    p1.find(option)
    click(p1.getLastMatch().right(100))
    if not p1.exists(setting):
        type(Key.PAGE_DOWN)
    if not p1.exists(setting):
        type(Key.PAGE_UP)
    if setting == "Keep 0":
        type(Key.DOWN)
        time.sleep(1)
        type(Key.ENTER)
    else:
        p1.click(setting)
    time.sleep(2)
    p1.click("button_done.png")

def click_source(self,reg,website):
        p = get_sources_region(reg)
        self.assertTrue(p.exists(website))
        click(p.getLastMatch())
        

def delete_feed(self,reg,feed):
    """Delete the video feed from the sidebar.
    feed = the feed name exact text that is displayed in the sidebar.
    m = Mainview Region, calculate in the testcase on launch.
    s = Sideview Region, calculated in the testcase on launch.

    """ 
    p = get_podcasts_region(reg)
    
    while p.exists(feed,1):
        p.click(feed)
        type(Key.DELETE)
        remove_confirm(self,reg,"remove")
        p = get_podcasts_region(reg)
        self.assertFalse(p.exists(feed,5))

def delete_items(self,reg,title,item_type):
    """Remove video audio music other items from the library.

    """
    click_sidebar_tab(self,reg,item_type)
    tab_search(self,reg,title)
    while reg.m.exists(title,10):
        click(reg.m.getLastMatch())
        type(Key.DELETE)
        remove_confirm(self,reg,"delete_item")
    self.assertFalse(reg.m.exists(title,10))

def delete_current_selection(self,reg):
    """Wherever you are, remove what is currently selected.

    """
    type(Key.DELETE)
    remove_confirm(self,reg,"remove")


def click_sidebar_tab(self,reg,tab):
    """Click any default tab in the sidebar.

    assumes the tab image file is an os-speicific image, and then verifies
    the tab is selected by verifying the miro large icon in the main view

    """
    if reg.s.exists("Sources",0):
        reg.s.click("Sources")        
    print "going to tab: "+str(tab)
    if "video" in tab.lower():
        reg.s.click("Videos")
    elif "misc" in tab.lower():
        click_misc(reg)
    else:
        reg.s.click(tab.capitalize())

def tab_search(self,reg,title,confirm_present=False):
    """enter text in the search box.

    """
    print "searching within tab"
    time.sleep(3)
    if reg.mtb.exists("tabsearch_inactive.png",5):
        click(reg.mtb.getLastMatch())
    elif reg.mtb.exists("tabsearch_clear.png",5):
        click(reg.mtb.getLastMatch())
        click(reg.mtb.getLastMatch().left(20))
    else:
        print "can not find the search box"
    if config.get_os_name() == "osx":
        wait("tabsearch_active",5)
    else:
        time.sleep(1)
    type(title.upper())
    if confirm_present == True:
        toggle_normal(reg)
        self.assertTrue(reg.m.exists(title))
        present=True
        return present

    
def toggle_normal(reg):
    if reg.mtb.exists(Pattern("list_view_active.png").similar(.98)):
        click(reg.mtb.getLastMatch())

def toggle_list(reg):
    if reg.mtb.exists(Pattern("normal_view_active.png").similar(.98)):
        click(reg.mtb.getLastMatch())

def search_tab_search(self,reg,term,engine=None):
    """perform a search in the search tab.

    Requires: search term (term), search engine(engine) and MainViewTopRegion (mtb)

    """
    print "starting a search tab search"
    # Find the search box and type in the search text
    if reg.mtb.exists("tabsearch_inactive.png",5):
        click(reg.mtb.getLastMatch())
    elif reg.mtb.exists("tabsearch_clear.png",5): # this should always be found on gtk
        print "found the broom"
        click(reg.mtb.getLastMatch())
        click(reg.mtb.getLastMatch().left(10))
    type(term.upper())
    # Use the search text to create a region for specifying the search engine
    if engine != None:
        l = reg.mtb.find(term.upper())
        l1= Region(int(l.getX()-20), l.getY(), 8, 8,)
        click(l1)
        l2 = Region(int(l.getX()-15), l.getY(), 300, 500,)
        
        if engine == "YouTube":
            l3 = Region(l2.find("YouTube User").above())
            l3.click(engine)
        else:
            l2.click(engine)
        type("\n") #enter the search 
        self.assertTrue(reg.mtb.exists("button_save_as_podcast.png",10))
    else:
        type("\n")
 

def download_all_items(self,reg):
    time.sleep(2)
    toggle_normal(reg)
    if reg.m.exists("button_download.png",3):
        badges = reg.m.findAll("down.png")
        for x in badges:
            reg.m.click(x)
    else:
        print "no badges found, maybe autodownloads in progress"


  
def confirm_download_started(self,reg,title):
    """Verifies file download started.

    Handles and already download(ed / ing) messages
    """
    print "in function confirm dl started"
    time.sleep(2)
    if reg.m.exists("message_already_downloaded.png",1):
        downloaded = "downloaded"
        print "item already downloaded"
        type(Key.ENTER)            
    elif reg.m.exists("message_already_external_dl.png",1):
        downloaded = "in_progress"
        print "item already downloaded"
        type(Key.ENTER)
    elif reg.m.exists("Error",1) or reg.m.exists("Error",1):
        downloaded = "failed"
        type(Key.ESC)
    else:
        reg.s.click("Downloading")
        reg.mtb.click("download-pause.png")
        if tab_search(self,reg,title,confirm_present=True) == True:
        	downloaded = "in_progress"
        else:
        	downloaded = "item not located"
        reg.mtb.click("download-resume.png")
    return downloaded


def wait_download_complete(self,reg,title,torrent=False):
    """Wait for a download to complete before continuing test.

    provide title - to verify item present itemtitle_'title'.png

    """
    if not confirm_download_started(self,reg,title) == "downloaded":
        if torrent == False:
            while reg.m.exists(title,5):
                time.sleep(5)
        elif torrent == True:
    #break out if stop seeding button found for torrent
            while not reg.m.exists("item_stop_seeding.png"):
                time.sleep(5)
                
def cancel_all_downloads(self,reg):
    """Cancel all in progress downloads.
    
    If the tab exists, cancel all dls and seeding.
    Click off downloads tab and confirm tab disappears.
    
    """
    if reg.s.exists("Downloading",5):
        click_sidebar_tab(self,reg,"downloading")
        time.sleep(3)
        reg.mtb.click("download-cancel.png")
        if reg.m.exists("Seeding"):
            seedlist = reg.m.findAll("Seeding")
            if len(seedlist > 0):
                for x in seedlist:
                    click(x)
    click_sidebar_tab(self,reg,"Videos")
    time.sleep(2)
    self.assertFalse(reg.s.exists("Downloading"))
    
                
def wait_for_item_in_tab(self,reg,tab,item):
    click_sidebar_tab(self,reg,tab)
    tab_search(self,reg,item)
    for x in range(0,30):
        while not reg.m.exists(item):
            time.sleep(5)
    
def wait_conversions_complete(self,reg,title,conv):
    """Waits for a conversion to complete.

    Catches the status and copies the log to a more identifyable name.
    Then it clears out the finished conversions.

    """
    while reg.m.exists(title):
        if reg.m.exists("Open log"):
            try:
                click(reg.m.getLastMatch())
                #save the error log to a file
                if config.get_os_name() == "osx":
                    time.sleep(10)
                    shortcut("s",shift=True)
                    wait("sys_save_as.png")
                    type(os.getcwd+"\n")
                    type(self.id()+"conv_"+conv+".log"+ "\n")
                else:
                    click("File")
                    click("Save as")
                    type(self.id()+"conv_"+conv+".log"+ "\n")
                    click("Save")
            finally:
                self.verificationErrors.append("error in conversion see log. "+str(title)+": "+str(conv))
            sstatus = "fail"
        else:
            sstatus = "pass"
            
        #fix - it's possible that I am clicking the wrong button
        reg.m.click("Clear Finished")


def add_source(self,reg,site_url,site):
    reg.tl.click("Sidebar")
    reg.tl.click("Add Source")
    time.sleep(2)
    type(site_url+"\n")
    p = get_sources_region(reg)
    website = site[0:10].rstrip()
    self.assertTrue(p.exists(website))

def new_search_feed(self,reg,term,radio,source):
    reg.t.click("Sidebar")
    reg.t.click("New Search")
    type(term)
    # Dialog appears in different locations on os x vs gtk
    if config.get_os_name() == "osx":
        reg.t.find("In this")
        f = Region(reg.t.getLastMatch().right(400).below())
    else:
        reg.m.find("In this")
        f = Region(reg.m.getLastMatch().nearby(500))
    f.click(radio)
    click(f.getLastMatch().right(135))
    time.sleep(2)
    if radio == "url":
        type(source)
    else:     
        if not f.exists(source,2):
            type(Key.PAGE_DOWN)
        if not f.exists(source,2):
            type(Key.PAGE_UP)
        f.click(source)
        
    f.click("Create")


def edit_item_type(self,reg,new_type):
    time.sleep(2)
    shortcut('i')
    time.sleep(2)
    click("Rating")
    f = Region(getLastMatch().nearby(200))
    f.find("Type")
    click(f.getLastMatch().right(50))
    if not f.exists(new_type,2):
        type(Key.PAGE_DOWN)
    f.click(new_type)
    time.sleep(2)
    click("button_ok.png")
        
        
    
def verify_normalview_metadata(self,reg,metadata):
    i = reg.mtb.below(300)
    for k,v in metadata.iteritems():
        self.assertTrue(i.exists(v,3))   

def verify_audio_playback(self,reg,title):
    reg.m.doubleClick(title)
    self.assertTrue(reg.m.exists("item_currently_playing.png"))
    reg.m.click(title)
    shortcut("d")
    reg.m.waitVanish("item_currently_playing.png")

def count_images(self,reg,img,region="screen",num_expected=None):
    """Counts the number of images present on the screen.

    It will either confirms that it is the expected value.
    Returns the number found.

    To narrow the search view - more reliable and efficient, specify the search region
    main: mainview
    sidebar: sidebar
    mainright: right half of mainview extended)

    
    """
    if region == "list":
        ly = reg.mtb.getY()-50
        lh = reg.mtb.getH()+800
        search_reg = Region(reg.mtb.getX(),ly,reg.mtb.getW(),lh)
    elif region == "main":
        search_reg = reg.m
    elif region == "mainright":
        lx = int(reg.m.getX())*2
        ly = int(reg.m.getY())-80
        wx = int(reg.m.getW()/2)+60  
        search_reg = Region(lx,ly,wx,reg.m.getH())
    elif region == "sidebar":
        search_reg = reg.s
    else:
        print "searching default SCREEN"
        search_reg = SCREEN
    mm = []
    f = search_reg.findAll(img) # find all matches
    while f.hasNext(): # loop as long there is a first and more matches
        print "found 1"
        mm.append(f.next())     # access next match and add to mm
        f.destroy() # release the memory used by finder
    if num_expected != None:
        self.assertEqual(len(mm),int(num_expected))
    return len(mm)

   
def handle_crash_dialog(self,db=True,test=False):
    """Look for the crash dialog message and submit report.
    
    """
    crashes = False
    while exists(Pattern("internal_error.png"),5):
        crashes = True
        tmpr = Region(getLastMatch().nearby(500))
        if db == True:
            click("Include")
        try:
            time.sleep(3)
            tmpr.find("Include")
            click(tmpr.getLastMatch().below(120))
            type("Sikuli Automated test crashed:" +str(self.id().split(".")[2]))
        finally:
            if exists("button_submit_crash_report.png") or exists("Submit Crash"):
                click(getLastMatch())
        time.sleep(5)
    	
    if crashes == True and test == False:
        print "miro crashed"
        time.sleep(20) #give it some time to send the report before shutting down.
#        quit_miro(self)
        self.fail("Got a crash report - check bogon")
        

    
