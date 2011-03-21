

#mirolib.py

import os
import time
import glob
import config
import testvars
from sikuli.Sikuli import *

setBundlePath(config.get_img_path())


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
    wait("Miro",60)
    click(getLastMatch())

def launch_miro():
    """Open the Miro Application, the sets the region coords for searching.
    
    Uses the Miro Guides, Feedback, Bottom Corner, and VolumeBar to find coordinates.
    Returns the:
        
    SidebarRegion (s) - miro sidebar 
    MainViewRegion(m) - miro mainview
    TopHalfRegion (t) - top 1/2 of whole screen
    TopLeftRegion (tl) - top left of whole screen
    MainTitleBarRegion (mtb) - miro mainview title bar region
    
    """
    regions = []
    if open_miro() == "linux":
        config.start_miro_on_linux()
    else:
        App.open(open_miro())
    wait("Sidebar",45)

    
    if exists("Miro",5):
        click(getLastMatch())
    else:
        if exists("icon-guide_active.png"):
            print "on guide tab"
    if not exists("Feedback.png",5):
        print ("network either off or slow, no feeback icon")
        find("Videos")
        sidex = int(getLastMatch().getX())+200
    else:
        wait("Feedback.png")
        sidex = getLastMatch().getX()

    find("Videos")
    topx =  int(getLastMatch().getX())-55
    topy = int(getLastMatch().getY())-15
    
    find("BottomCorner.png")
    vbarx =  int(getLastMatch().getX())+30
    vbary = int(getLastMatch().getY())+30
    vbarw = getLastMatch().getW()

    sidebar_width = int(sidex-topx)
    app_height = int(vbary-topy)
    
    #Sidebar Region
    SidebarRegion = Region(topx,topy,sidebar_width,app_height)
    SidebarRegion.setAutoWaitTimeout(30)
    regions.append(SidebarRegion)
    #Mainview Region
    mainwidth = int((vbarx-sidex)+vbarw)
    MainViewRegion = Region(sidex,topy,mainwidth,app_height)
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
    MainTitleBarRegion = Region(sidex,topy,mainwidth,150)
    MainTitleBarRegion.setAutoWaitTimeout(30)
    regions.append(MainTitleBarRegion)
    
    return regions

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

    

def quit_miro(self,m,s):
    click_sidebar_tab(self,m,s,"Videos")
    shortcut("q")
    while m.exists("dialog_confirm_quit.png",5):
        m.click("dialog_quit.png")
    self.assertFalse(s.exists("Music",5))
    
    
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
    else:
        print "no clue"



def toggle_radio(self,button):
    
    """Looks for the specified tab by image base name.
    Should be able to find the image if it is selected or not selected.
    """
    if not exists (imagemap.Buttons[button +"_selected"]):
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

def remove_confirm(self,m,action="remove"):
    """If the remove confirmation is displayed, remove or cancel.

    action = (remove_feed, remove_item or cancel)
    m = Mainview region from testcase
    need to add remove_library option
    """
    time.sleep(5)
    if m.exists(Pattern("dialog_are_you_sure.png"),5) or \
       m.exists(Pattern("dialog_one_of_these.png"),5):
        print "confirm dialog"
        time.sleep(3)
        if action == "remove":
            print "clicking remove button"
            type(Key.ENTER)
        elif action == "delete_item":
            print "clicking delete button"
            m.click("button_delete_file.png")
        elif action == "cancel":
            m.click("Cancel")
        elif action == "keep":
            m.click("Keep")
            type(Key.ENTER)
        else:
            print "not sure what to do in this dialog"
    self.assertTrue(m.waitVanish(Pattern("dialog_are_you_sure.png"),10))
    
def get_website_region(m,s):
    """takes the main and sidebar regions to create a region for the websites section.
    
    """
    s.click("Sources")
    topx =  s.getLastMatch().getX()
    topy =  s.getLastMatch().getY()
    width = s.getW()
    s.find("Podcasts")
    boty =  s.getLastMatch().getY()
    height = boty-topy
    WebsitesRegion = Region(topx,topy, width, height)
    WebsitesRegion.setAutoWaitTimeout(20)
    return WebsitesRegion

def get_podcasts_region(s):
    s.find("Podcasts")
    topx =  s.getLastMatch().getX()
    topy =  s.getLastMatch().getY()
    s.find("Playlists")
    boty =  s.getLastMatch().getY()
    height = boty-topy
    width = s.getW()
    PodcastsRegion = Region(topx,topy, width, height)
    PodcastsRegion.setAutoWaitTimeout(20)
    return PodcastsRegion
    
    
    
	
    
def delete_site(self,m,s,site):
    """Delete the video feed from the sidebar.
    feed = the feed name exact text that is displayed in the sidebar.
    m = Mainview Region, calculate in the testcase on launch.
    s = Sideview Region, calculated in the testcase on launch.

    """
    if s.exists("miro_guide_tab.png",1):
        click(s.getLastMatch())
    w = get_website_region(m,s)
    while w.exists(site,10):
        w.click(site)
        type(Key.DELETE)
        remove_confirm(self,m,"remove")
        click_sidebar_tab(self,m,s,"Video")
        self.assertFalse(w.exists(site),5)
    else:
        print "feed: " +site+ " not present"

def add_feed(self,t,s,mtb,url,feed):
    """Add a feed to miro, click on it in the sidebar.
    
    Verify the feed is added by clicking on the feed and verify the feed name is present
    in the main title bar.
    """
    t.click("Sidebar")
    t.click("Add Podcast")
    time.sleep(2)
    type(url + "\n")
    time.sleep(5)
    expand_sidebar_section(self,s,"Podcasts")
    time.sleep(2)
    p = get_podcasts_region(s)
    self.assertTrue(p.exists(feed))
    click(p.getLastMatch())
    


def delete_feed(self,m,s,feed):
    """Delete the video feed from the sidebar.
    feed = the feed name exact text that is displayed in the sidebar.
    m = Mainview Region, calculate in the testcase on launch.
    s = Sideview Region, calculated in the testcase on launch.

    """
    if s.exists("Videos",1):
        click(s.getLastMatch())
    expand_sidebar_section(self,s,"Podcasts")
    time.sleep(2)
    p = get_podcasts_region(s)
    
    while p.exists(feed,1):
        p.click(feed)
        type(Key.DELETE)
        remove_confirm(self,m,"remove")
        click_sidebar_tab(self,m,s,"Videos")
        self.assertFalse(p.exists(feed),5)

def delete_items(self,m,s,title,item_type):
    """Remove video audio music other items from the library.

    """
    click_sidebar_tab(self,m,s,item_type)
    tab_search(self,m,s,title)
    while m.exists(title,10):
        click(m.getLastMatch())
        type(Key.DELETE)
        remove_confirm(self,m,"delete_item")
    self.assertFalse(m.exists(title,10))


def click_sidebar_tab(self,m,s,tab):
    """Click any default tab in the sidebar.

    assumes the tab image file is an os-speicific image, and then verifies
    the tab is selected by verifying the miro large icon in the main view

    """
    if s.exists("Sources",0):
        s.click("Sources")
    for x in testvars.SIDEBAR_ICONS.keys():
        if tab.lower() == "videos":
            tab = "video"
        if tab.lower() in x:
            tab_icon = testvars.SIDEBAR_ICONS[x]        
    print "going to tab: "+str(tab)
    if tab.lower() == "video":
        s.click("Videos")
    else:
        s.click(tab.capitalize())


## Menu related stuff ##
   

def tab_search(self,m,s,title,confirm_present=False):
    """enter text in the search box.

    """
    print "searching within tab"
    if m.exists("tabsearch_inactive.png",5):
        click(m.getLastMatch())
    elif m.exists("tabsearch_clear.png",5):
        click(m.getLastMatch())
    
    type(title.upper())
    if confirm_present == True:
        self.assertTrue(m.exists(title))
        present=True
        return present

def search_tab_search(self,mtb,term,engine):
    """perform a search in the search tab.

    Requires: search term (term), search engine(engine) and MainViewTopRegion (mtb)

    """
    print "starting a search tab search"
    # Find the search box and type in the search text
    if mtb.exists("tabsearch_inactive.png",5):
        click(mtb.getLastMatch())
    elif mtb.exists("tabsearch_clear.png",5): # this should always be found on gtk
        print "found the broom"
        click(mtb.getLastMatch())
        click(mtb.getLastMatch().left(10))
    type(term.upper())
    # Use the search text to create a region for specifying the search engine
    l = mtb.find(term.upper())
    l1= Region(int(l.getX()-20), l.getY(), 8, 8,)
    click(l1)
    l2 = Region(int(l.getX()-15), l.getY(), 200, 300,)
    if engine == "YouTube":
        l3 = Region(l2.find("YouTube User").above())
        l3.click(engine)
    else:
        l2.click(engine)
    type("\n") #enter the search
    self.assertTrue(mtb.exists("button_save_asa_feed.png"))
 

def download_all_items(self,m):
    badges = m.findAll("Download")
    for x in badges:
        m.click(x)


  
def confirm_download_started(self,m,s,title):
    """Verifies file download started.

    Handles and already download(ed / ing) messages
    """
    print "in function confirm dl started"
    time.sleep(2)
    if m.exists("message_already_downloaded.png",1):
        downloaded = "downloaded"
        print "item already downloaded"
        type(Key.ENTER)            
    elif m.exists("message_already_external_dl.png",1):
        downloaded = "in_progress"
        print "item already downloaded"
        type(Key.ENTER)
    else:
        s.click("Downloading")
        m.click("button_pause_all.png")
        if tab_search(self,m,s,title,confirm_present=True) == True:
        	downloaded = "in_progress"
        else:
        	downloaded = "item not located"
        m.click("button_resume_all.png")
    return downloaded


def wait_download_complete(self,m,s,title,torrent=False):
    """Wait for a download to complete before continuing test.

    provide title - to verify item present itemtitle_'title'.png

    """
    if not confirm_download_started(self,title,confirm_present=True) == "downloaded":
        if torrent == False:
            while m.exists(title,5):
                time.sleep(5)
        elif torrent == True:
    #break out if stop seeding button found for torrent
            while not m.exists("item_stop_seeding.png"):
                time.sleep(5)
                
def cancel_all_downloads(self,m,s,mtb):
    """Cancel all in progress downloads.
    
    If the tab exists, cancel all dls and seeding.
    Click off downloads tab and confirm tab disappears.
    
    """
    if s.exists("Downloading",5):
        click_sidebar_tab(self,m,s,"downloading")
        mtb.click("Cancel All")
        seedlist = m.findAll("Seeding")
        if len(seedlist > 0):
            for x in seedlist:
                click(x)
    click_sidebar_tab(self,m,s,"video")
    self.assertFalse(s.exists("Downloading"))
    
                
def wait_for_item_in_tab(self,m,s,tab,item):
    click_sidebar_tab(self,m,s,tab)
    while not m.exists(item):
    	time.sleep(5)
    
    

    
def wait_conversions_complete(self,m,s,title,conv):
    """Waits for a conversion to complete.

    Catches the status and copies the log to a more identifyable name.
    Then it clears out the finished conversions.

    """
    while m.exists(title):
        if m.exists("Open log"):
            try:
                click(m.getLastMatch())
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
        m.click("Clear Finished")


def expand_sidebar_section(self,s,section):
    s.find(section)
    a = Region(s.getLastMatch().left(35))
    a1 = Region(a.nearby(25))
    if a1.exists(Pattern("arrow_opened.png").similar(0.95)):
        print("section expanded")
    elif a1.exists(Pattern("arrow_closed.png").similar(0.95)):
        click(a1.getLastMatch())
    else:
        print "expander not found"


def add_website(self,s,tl,site_url,site):
    expand_sidebar_section(self,s,"Sources")
    tl.click("Sidebar")
    tl.click("Website")
    time.sleep(4)
    type(site_url+"\n")
    s.find(site)
    self.assertTrue(s.exists(site))

def new_search_feed(self,m,t,term,radio,source):
    t.click("Sidebar")
    t.click("New Search")
    type(term)
    m.find(radio)
    f = Region(m.getLastMatch().left(300))
    click(m.getLastMatch())
    click(f)
    if radio == url:
        type(source)
    else:     
        f1 = f.below()
        f1.click(source)
    m.click("Create Feed")

def verify_normalview_metadata(self,mtb,metadata):
    i = mtb.below(300)
    for k,v in metadata.iteritems():
        self.assertTrue(i.exists(v,3))   

def verify_audio_playback(self,m,s):
    self.assertTrue(exists("playback_bar_audio.png"))
    self.assertTrue(m.exists("item_currently_playing.png"))
    mirolib.shortcut("d")
    waitVanish("playback_bar_audio.png")
    
def handle_crash_dialog(self,db=True):
    """Look for the crash dialog message and submit report.
    
    """
    crashes = False
    while exists(Pattern("internal_error.png"),15):
        crashes = True
#        tmpr = Region(getLastMatch().around(500))
        if db == True:
            click("Include")
        type("Auto test crashed:" +str(self.id().split(".")[2]))
        click("button_submit_crash_report.png")
        time.sleep(5)
    	
    if crashes == True:
        print "miro crashed"
        shortcut("q")
        time.sleep(10)
    
    
        

    
