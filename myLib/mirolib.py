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
        return "C:\Program Files\Participatory Culture Foundation\Miro\Miro.exe"
    elif config.get_os_name() == "lin":
        return "~/builds/miro*/linux/run.sh"
    else:
        print config.get_os_name()

def launch_miro():
    regions = []
    App.open(open_miro())
    if exists("miro_guide_tab.png",10):
        click(getLastMatch())
    wait("Feedback.png")
    sidex = getLastMatch().getX()
    find("MiroGuide_selected.png")
    topx =  getLastMatch().getX()
    topy = getLastMatch().getY()

    find("BottomCorner.png")
    botx =  getLastMatch().getX()
    boty = getLastMatch().getY()

    find("VolumeBar.png")
    vbarx =  getLastMatch().getX()
    vbary = getLastMatch().getY()
    vbarw = getLastMatch().getW()

    sidebar_width = int(sidex-topx)
    app_height = int(vbary-topy)

    SidebarRegion = Region(topx,topy,sidebar_width,app_height)
    SidebarRegion.setAutoWaitTimeout(60)
    regions.append(SidebarRegion)
    mainwidth = int((vbarx-sidex)+vbarw)
    MainViewRegion = Region(sidex,topy,mainwidth,app_height)
    MainViewRegion.setAutoWaitTimeout(60)
    regions.append(MainViewRegion)
    TopHalfRegion = Region(0,0,mainwidth+sidebar_width,app_height/2)
    TopHalfRegion.setAutoWaitTimeout(60)
    regions.append(TopHalfRegion)
    TopLeftRegion = Region(0,0,mainwidth/2,app_height/2)
    TopLeftRegion.setAutoWaitTimeout(60)
    regions.append(TopLeftRegion)
    

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

    

def quit_miro(self):
    shortcut("q")
    while exists("dialog_confirm_quit.png",10):
        click("dialog_quit.png")
    #giving it 15 seconds to shut down
    self.assertFalse(exists("tab_search.png",15))
    
    
def cmd_ctrl():
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
        return "C:\Program Files\Mozilla Firefox\Firefox.exe"
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
    """If the remove feed dialog is displayed, remove or cancel.

    action = (remove_feed, remove_item or cancel)
    m = Mainview region from testcase
    need to add remove_library option
    """
    time.sleep(5)
    if m.exists(Pattern("button_remove_pulse.png"),5):
        print "confirm dialog"
        if action == "remove":
            print "clicking remove button"
            type("\n")
        elif action == "delete_item":
            print "clicking delete button"
            m.click("Delete File")
        elif action == "cancel":
            m.click("Cancel")
        print "verifying dialog closed"
    self.assertFalse(exists("are_you_sure_dialog.png"),4)
    
def get_website_region(m,s):
    "takes the main and sidebar regions to create a region for the websites section"
    s.find("WEBSITES")
    topx =  s.getLastMatch().getX()
    topy =  s.getLastMatch().getY()
    width = s.getW()
    s.find("VIDEO FEEDS")
    boty =  s.getLastMatch().getY()
    height = boty-topy
    print height
    WebsitesRegion = Region(topx,topy, width, height)
    WebsitesRegion.setAutoWaitTimeout(20)
    return WebsitesRegion
    
	
    
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

def delete_feed(self,m,s,feed):
    """Delete the video feed from the sidebar.
    feed = the feed name exact text that is displayed in the sidebar.
    m = Mainview Region, calculate in the testcase on launch.
    s = Sideview Region, calculated in the testcase on launch.

    """
    if s.exists("miro_guide_tab.png",1):
        click(s.getLastMatch())
    while s.exists(feed,10):
        s.click(feed)
        type(Key.DELETE)
        remove_confirm(self,m,"remove")
        click_sidebar_tab(self,m,s,"Video")
        self.assertFalse(s.exists(feed),5)
    else:
        print "feed: " +feed+ " not present"

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
    if s.exists("miro_guide_tab.png",4):
        s.click("miro_guide_tab.png")
    for x in testvars.TAB_LARGE_ICONS.keys():
        if tab.lower() in x:
            tab_icon = testvars.TAB_LARGE_ICONS[x]        
    print "going to tab: "+str(tab)
    print tab_icon
    if m.exists(Pattern(tab_icon).similar(0.91),5):
        print "on tab: "+ str(tab)
    else:
        s.click(tab)
        self.assertTrue(m.exists(tab_icon))


## Menu related stuff ##


def open_preferences(self,tl,lang='en'):
    """OS specific handling for Preferences menu, since it differs on osx and windows.

    """
        
    if config.get_os_name() == "osx":
        tl.click("Miro")
    elif config.get_os_name() == "win":
        tl.click("File")
    else:
        print config.get_os_name()
    self.assertTrue(exists("menu_preferences.png"))
    if lang == 'en':
        tl.click("Preferences")
    else:
        tl.click(lang)
    self.assertTrue(exists(testvars.pref_general))

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
        self.assertTrue(m.exists(title),15)
    	present=True
    	return present
    
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
            while not exists("item_stop_seeding.png"):
                time.sleep(5)
    
    click_sidebar_tab(self,"other")
    

    
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


            
    

    

    
