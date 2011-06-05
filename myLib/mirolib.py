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


    def launch_miro():
        """Open the Miro Application, the sets the region coords for searching.
        
        Uses the Miro Guides, Home icon, Bottom Corner, and VolumeBar to find coordinates.
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
        if exists("Music",120) or \
           exists("icon-music.png",120) :
            print "miro launched"
            
    
    def get_regions():
        regions = []
        myscreen = Screen()
        pr = Region(myscreen.getBounds())
        hw = pr.getW()/3
        hh = pr.getH()/3
        pr.setW(hw)
        pr.setH(hh)
        pr.setY(10)
        if pr.exists("Music") or \
           pr.exists(Pattern("icon-audio_active.png")):
            click(pr.getLastMatch())
        elif pr.exists("Videos",3):
            click(pr.getLastMatch())
        libr = Region(pr.getLastMatch().above(80).left(120).right(200))
        libr.click("Miro")
        mg = Region(libr.getLastMatch())
        pr.find(Pattern("miroguide_home.png").similar(.95))
        click(pr.getLastMatch())
        click(mg)
        sidex = pr.getLastMatch().getX()-15            

        pr.find("Music")
        topx =  int(pr.getLastMatch().getX())-55
        topy = int(pr.getLastMatch().getY())-80
         
        
        find("BottomCorner.png")
        vbarx =  int(getLastMatch().getX())+30
        vbary = int(getLastMatch().getY())+10
        vbarw = getLastMatch().getW()

        sidebar_width = int(sidex-topx)
        app_height = int(vbary-topy)
#        tbar_height = 100
        
        #Sidebar Region
        SidebarRegion = Region(topx,topy,sidebar_width,app_height)
        SidebarRegion.setAutoWaitTimeout(30)
        regions.append(SidebarRegion)                
        #Mainview Region
        mainwidth = int((vbarx-sidex)+vbarw)
        #MainViewRegion = Region(sidex,topy+tbar_height,mainwidth,app_height-155) - old m
        MainViewRegion = Region(sidex,topy+80,mainwidth,app_height)
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
        MainTitleBarRegion = Region(sidex,topy,mainwidth,120)
        MainTitleBarRegion.setAutoWaitTimeout(30)
        regions.append(MainTitleBarRegion)
        return regions

    
    config.set_image_dirs()
    launch_miro()
    setAutoWaitTimeout(testvars.timeout) 
    miroRegions = get_regions()
    s = miroRegions[0] #Sidebar Region
    s.highlight(1)
    m = miroRegions[1] #Mainview Region
    m.highlight(1)
    t= miroRegions[2] #top half screen
#    t.highlight(5)
    tl = miroRegions[3] #top left quarter
#    tl.highlight(5)
    mtb = miroRegions[4] #main title bar
#    mtb.highlight(5)
    mr = Region(mtb.above(50).below())
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
        App.open(open_miro())
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
        return "C:\\Program Files\\Mozilla Firefox\\firefox.exe"
    elif config.get_os_name() == "lin":
        config.start_ff_on_linux()
        return "firefox"
    else:
        print "no clue"

def browser_to_miro(self,reg,url):
    """Opens the browser and copies in a url. Waits then closes the browser.

    This has the expectation that the browser is configured to open the url with miro, .torrent or feed item.
    """
    App.open(open_ff())
    if reg.t.exists("Firefox",45):
        click(reg.t.getLastMatch())
    shortcut("l")
    time.sleep(2)
    type(url + "\n")
    time.sleep(20)
    close_ff()


def close_ff():
    App.close("Firefox")
    time.sleep(3)
    if exists("Firefox",3):
        print "ff still here"
        click(getLastMatch())
        if config.get_os_name() == "osx":
            shortcut('w')
        elif config.get_os_name() == "win":
            shortcut('w')
        else:
            shortcut('q')
    time.sleep(2)
        
def close_window():
    if config.get_os_name() == "osx":
        shortcut('w')
    else:
        shortcut('q')

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
    if reg.m.exists("Remove",3) or \
       reg.t.exists("Are you",3) or \
       reg.t.exists("One of",3) or \
       reg.m.exists(Pattern("dialog_are_you_sure.png"),3) or \
       reg.m.exists(Pattern("dialog_one_of_these.png"),3) or \
       reg.t.exists("Cancel",3)or \
       reg.t.exists(Pattern("dialog_are_you_sure.png"),3) or \
       reg.t.exists(Pattern("dialog_one_of_these.png"),3):
        
        print "got confirmation dialog"
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
        time.sleep(1)
    reg.s.click("Sources")
    time.sleep(2)
    topx =  reg.s.getX()-10
    topy =  reg.s.getLastMatch().getY()
    reg.s.find("Stores")
    boty =  reg.s.getLastMatch().getY()
    height = (boty-topy)+20
    width = reg.s.getW()
    SourcesRegion = Region(topx,topy, width, height)
    SourcesRegion.setAutoWaitTimeout(20)
    return SourcesRegion

def get_podcasts_region(reg):
    if not reg.s.exists("Podcasts",1):
        reg.s.click("Music")
    reg.s.click("Podcasts")
    time.sleep(2)
    topx =  (reg.s.getLastMatch().getX())-10
    topy =  reg.s.getLastMatch().getY()
    tmpr = Region(reg.s)
    tmpr.setY(tmpr.y+200)
    tmpr.find("Playlists")
    boty =  tmpr.getLastMatch().getY()
    height = (boty-topy)+50
    width = reg.s.getW()
    PodcastsRegion = Region(topx,topy, width, height)
    PodcastsRegion.setAutoWaitTimeout(20)
    return PodcastsRegion
    
def get_playlists_region(reg):
    if not reg.s.exists("Playlists",1):
        reg.s.click("Podcasts")
    reg.s.click("Playlists")
    PlaylistsRegion = Region(reg.s.getLastMatch().left(150).right(200).below())
    PlaylistsRegion.setAutoWaitTimeout(20)
    return PlaylistsRegion     
	
    
def delete_site(self,reg,site):
    """Delete the video feed from the sidebar.
    feed = the feed name exact text that is displayed in the sidebar.
    m = Mainview Region, calculate in the testcase on launch.
    s = Sideview Region, calculated in the testcase on launch.

    """
    
    p = get_sources_region(reg)
    if p.exists(site,15):
        click(p.getLastMatch())
        time.sleep(2)
        type(Key.DELETE)
        remove_confirm(self,reg,"remove")
    else:
        print "site not present: ",site

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
    p.find(feed)
    click(p.getLastMatch())

def add_watched_folder(self,reg,folder_path,show=True):
    """Add a feed to miro, click on it in the sidebar.
    
    Verify the feed is added by clicking on the feed and verify the feed name is present
    in the main title bar.
    """
    reg.t.click("File")
    reg.t.click("Import")
    reg.t.click("Watch")
    time.sleep(4)
    if show == True:
        type(folder_path+"\n")
        time.sleep(10) #give it 10 seconds to add the feed
        click_last_podcast(self,reg)
    else:
        type(folder_path)
        reg.m.click("Show in")
        type(Key.TAB)
        type(Key.TAB)
        type(Key.ENTER)
    
def click_last_source(self,reg):
    """Based on the position of the Playlists tab, click on the last podcast in the list.

    This is useful if the title isn't displayed completely or you have other chars to don't work for text recognition.
    """
    p = get_sources_region(reg)
    time.sleep(5)
    p.find("Stores")
    click(p.getLastMatch().above(38))


def click_last_podcast(self,reg):
    """Based on the position of the Playlists tab, click on the last podcast in the list.

    This is useful if the title isn't displayed completely or you have other chars to don't work for text recognition.
    """
    p = get_podcasts_region(reg)
    time.sleep(5)
    reg.s.find("Playlists")
    click(reg.s.getLastMatch().above(35))

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
    
    b = Region(reg.m.getX(),reg.m.getY()+500,reg.m.getW(), reg.m.getH())
    b.highlight(2)
    b.find("button_autodownload.png")
    b1 = Region(b.getLastMatch().right(80))
    b1.highlight(2)
    for x in range(0,3):
        if not b1.exists(setting,2):
               b.click("button_autodownload.png")
               time.sleep(2)

def open_podcast_settings(self,reg):
    b = Region(reg.s.getX(),reg.m.getY()*2,reg.m.getW(), reg.m.getH())
    b.find(Pattern("button_settings.png").exact())
    click(b.getLastMatch())

def click_remove_podcast(self,reg):
    click("button_remove_podcast.png")

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
        p.find(website)
        click(p.getLastMatch())
        

def delete_feed(self,reg,feed):
    """Delete the video feed from the sidebar.
    feed = the feed name exact text that is displayed in the sidebar.
    m = Mainview Region, calculate in the testcase on launch.
    s = Sideview Region, calculated in the testcase on launch.

    """ 
    p = get_podcasts_region(reg)
    
    if p.exists(feed,4):
        click(p.getLastMatch())
        type(Key.DELETE)
        remove_confirm(self,reg,"remove")
##        p = get_podcasts_region(reg)
##        self.assertFalse(p.exists(feed,5))

def delete_items(self,reg,title,item_type):
    """Remove video audio music other items from the library.

    """
    click_sidebar_tab(self,reg,item_type)
    tab_search(self,reg,title)
    if reg.m.exists(title,10):
        click(reg.m.getLastMatch())
        type(Key.DELETE)
        remove_confirm(self,reg,"delete_item")

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
        reg.s.find("Music")
        tr = Region(reg.s.getLastMatch().left(30).right(100).above(100))
        tr.click("Videos")
    elif "misc" in tab.lower():
        click_misc(reg)
    elif "miro" in tab.lower():
        reg.s.find("Music")
        tr = Region(reg.s.getLastMatch().above(100))
        tr.click("Miro")
    else:
        reg.s.click(tab.capitalize())

def tab_search(self,reg,title,confirm_present=False):
    """enter text in the search box.

    """
    
    print "searching within tab"
    time.sleep(3)
    if reg.mtb.exists("tabsearch_clear.png",5):
        print "found tabsearch_clear"
        click(reg.mtb.getLastMatch())
        click(reg.mtb.getLastMatch().left(10))
    elif reg.mtb.exists("tabsearch_inactive.png",5):
        print "found tabsearch_inactive"
        click(reg.mtb.getLastMatch())
    else:
        print "can not find the search box"
    time.sleep(2)
    type(title.upper())
    if confirm_present == True:
        toggle_normal(reg)
        if reg.m.exists(title,5):
            present=True
        else:
            self.fail("Item not found in downloading tab",title)
        return present

    
def toggle_normal(reg):
    if reg.mtb.exists(Pattern("list_view_active.png").similar(.98),1):
        click(reg.mtb.getLastMatch())
        time.sleep(2)

def toggle_list(reg):
    if reg.mtb.exists(Pattern("normal_view_active.png").similar(.98),1):
        click(reg.mtb.getLastMatch())
        time.sleep(2)

def search_tab_search(self,reg,term,engine=None):
    """perform a search in the search tab.

    Requires: search term (term), search engine(engine) and MainViewTopRegion (mtb)

    """
    print "starting a search tab search"
    # Find the search box and type in the search text
    
    if reg.mtb.exists("tabsearch_clear.png",5): # this should always be found on gtk
        print "found the broom"
        click(reg.mtb.getLastMatch())
        click(reg.mtb.getLastMatch().left(10))
    elif reg.mtb.exists("tabsearch_inactive.png",5):
        click(reg.mtb.getLastMatch())
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
        self.assertTrue(reg.mtb.exists(Pattern("button_save_as_podcast.png")),10)
    else:
        type("\n")
 

def download_all_items(self,reg):
    time.sleep(2)
    toggle_normal(reg)
    if reg.m.exists(Pattern("button_download.png"),3):       
        mm = []
        f = reg.m.findAll("button_download.png") # find all matches
        while f.hasNext(): # loop as long there is a first and more matches
            print "found 1"
            mm.append(f.next())     # access next match and add to mm
        for x in mm:
            click(x)
    else:
        print "no badges found, maybe autodownloads in progress"


  
def confirm_download_started(self,reg,title):
    """Verifies file download started.

    Handles and already download(ed / ing) messages
    """
    print "in function confirm dl started"
    time.sleep(2)
    mr = Region(reg.mtb.above(50).below())
    if mr.exists("been downloaded",3) or \
       mr.exists("message_already_downloaded.png",1):
        downloaded = "downloaded"
        print "item already downloaded"
        type(Key.ESC)            
    elif mr.exists("downloading now",5) or \
         mr.exists("message_already_external_dl.png",1):
        downloaded = "in_progress"
        print "item downloading"
        type(Key.ESC)
    elif mr.exists("Error",3) or \
         mr.exists(Pattern("badge_dl_error.png"),1):
        downloaded = "failed"
        type(Key.ESC)
    else:
        click_sidebar_tab(self,reg,"Downloading")
        reg.mtb.click("download-pause.png")
        if mr.exists(Pattern("badge_dl_error.png"),2):
            downlaoded = "errors"
        elif tab_search(self,reg,title,confirm_present=True) == True:
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
    click_sidebar_tab(self,reg,"Music")
    time.sleep(2)
    if reg.s.exists("Downloading",5):
        click(reg.s.getLastMatch())
        time.sleep(3)
        reg.mtb.click("download-cancel.png")
        if reg.m.exists("Seeding"):
            mm = []
            f = reg.m.findAll("button_download.png") # find all matches
            while f.hasNext(): # loop as long there is a first and more matches
                print "found 1"
                mm.append(f.next())     # access next match and add to mm
            for x in mm:
                click(x)    
                
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
        if reg.m.exists("Open log",5):
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
        if reg.mtb.exists("button_clear_finished.png",2) or \
           reg.mtb.exists("Clear Finished",5):
            click(reg.mtb.getLastMatch())
        return sstatus


def add_source(self,reg,site_url,site,alt_site=None):
    reg.tl.click("Sidebar")
    reg.tl.click("Add Source")
    time.sleep(2)
    type(site_url+"\n")
    time.sleep(3)
    p = get_sources_region(reg)
    website = site[0:10].rstrip()
    if alt_site == None:
        p.find(website)
    else:
        if not exists(website,5):
            p.find(alt_site)
    click(p.getLastMatch())


def add_source_from_tab(self,reg,site_url):
    p = get_sources_region(reg)
    reg.m.find("URL")
    click(reg.m.getLastMatch().right(150))
    type(site_url+"\n")
    
def new_search_feed(self,reg,term,radio,source,defaults=False,watched=False):
    reg.t.click("Sidebar")
    reg.t.click("New Search")
    if defaults == True:
        time.sleep(2)
        type(Key.ENTER)
    elif watched == True:
        if reg.m.exists(source):
            self.fail
        handle_crash_dialog(self,db=True,test=False)   
        type(Key.ESC)   
    else:
        type(term)
        # Dialog appears in different locations on os x vs gtk
##        if config.get_os_name() == "osx":
##            reg.t.find("In this")
##            f = Region(reg.t.getLastMatch().right(600).below())
##        else:
##            reg.m.find("In this")
##            f = Region(reg.m.getLastMatch().right(600).above().below())
        reg.mr.find("In this")
        f = Region(reg.mr.getLastMatch().right(600).below())
        f.setY(f.getY()-120)
        f.highlight(3)         
        f.click(radio)
        click(f.getLastMatch().right(150))
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
    self.assertTrue(reg.m.exists("item_currently_playing.png"))
    reg.m.click(title)
    shortcut("d")
    reg.m.waitVanish("item_currently_playing.png",20)
    log_result("102","stop audio playback shortcut verified.")

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
        lx = int(reg.m.getX())*4
        ly = int(reg.m.getY())
        wx = int(reg.m.getW()/2)  
        search_reg = Region(lx,ly,wx,reg.m.getH())
    elif region == "sidebar":
        search_reg = reg.s
    else:
        print "searching default SCREEN"
        search_reg = SCREEN
    search_reg.highlight(3)
    mm = []
    f = search_reg.findAll(img) # find all matches
    while f.hasNext(): # loop as long there is a first and more matches
        print "found 1"
        mm.append(f.next())     # access next match and add to mm
        f.destroy() # release the memory used by finder
    if num_expected != None:
        self.assertEqual(len(mm),int(num_expected))
    return len(mm)


def convert_file(self,reg,out_format):
    if config.get_os_name() == "osx":
        reg.t.click("Convert")
    else:
       type('c',KEY_ALT)
    find("Conversion Folder")
    tmpr = Region(getLastMatch().left(300).right(200).above(900))
    if out_format == "MP3":
        tmpr.find("Theora")
        click(tmpr.getLastMatch().above(80))
    else:
        tmpr.find(out_format)
        click(tmpr.getLastMatch())
    

def import_opml(self,reg,opml_path):
    reg.tl.click("Sidebar")
    reg.tl.click("Import")
    time.sleep(2)
    type_a_path(self,reg,opml_path)
    wait("imported",15)
    type(Key.ENTER)

def type_a_path(self,reg,file_path):
    if config.get_os_name() == "osx":
        type(opml_path +"\n")     
    else:
        if not exists("Location",5):
            click(Pattern("type_a_filename.png"))
            time.sleep(2)
        type(file_path +"\n")
    

def log_result(result_id,runner_id):
    LOG_RESULT = """
    <result testid="%(testid)s"
    is_automated_result="0"
    resultstatus="%(status)s"
    exitstatus="0"
    timestamp="%(timestamp)s"
    >
    
        <comment><![CDATA[ %(msg)s]]>
        </comment>
    </result>
"""
    
    log = "Log_current.xml"
    logfile = os.path.join(os.getcwd(),log)
    f = open(logfile, 'a')
    f.write(LOG_RESULT % {"testid": result_id,
                     "status": "pass",
                     "timestamp": time.strftime("%Y%m%d%H%M%S", time.gmtime()),
                     "msg": "executed as part of "+runner_id
                         })
    f.close
   
def handle_crash_dialog(self,db=True,test=False):
    """Look for the crash dialog message and submit report.
    
    """
    crashes = False
    while exists(Pattern("internal_error.png"),5):
        crashes = True
        tmpr = Region(getLastMatch().nearby(800))
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
        type(Key.ESC) # close any leftover dialogs
        time.sleep(20) #give it some time to send the report before shutting down.
#        quit_miro(self)

        self.fail("Got a crash report - check bogon")
        

    
