# All actions on the preferences panel

import config
import testvars
import mirolib
from sikuli.Sikuli import *


def open_prefs(self,reg,lang='en',menu=None,option=None):
    """OS specific handling for Preferences menu, since it differs on osx and windows.

    """
    if lang == 'en':
        option = 'Preferences'
    #Open the Preferences Menu based on the os with keyboard navigation
    if config.get_os_name() == "osx":
        mirolib.shortcut(',')
        pr = Region(reg.m)
    else:
        myscreen = Screen()
        pr = Region(myscreen.getBounds())
        type('f',KEY_ALT)
        reg.t.click(option)
        time.sleep(2)             
    pr.highlight(2)
    return pr


def open_tab(self,p,tab):
    """Open the specified tab by searching with-in the preferences region (p) for the icon.

    """
    for x in testvars.PREF_PANEL.keys():
        if tab.lower() in x:
            pref_icon = testvars.PREF_PANEL[x]        
    print "going to tab: "+str(tab)
    p.click(pref_icon)
    tab_loc = Region(p.getLastMatch())
    return tab_loc

def set_autodownload(self,reg,setting="Off"):
    """Set the global autodownload prefernce setting.

    Setting can be "Off, New, or All"
    """
    allset = False
    p = open_prefs(self,reg)
    open_tab(self,p,tab="Podcasts")
    p.find("download setting")
    p1 = Region(p.getLastMatch().right(200))
    p2 = Region(p1.nearby(200))
    if p1.exists(setting):
        allset = True
    else:
        click(p1.getCenter())
        if not p2.exists(setting):
            type(Key.PAGE_DOWN)
        if not p2.exists(setting):
            type(Key.PAGE_UP)
        p2.click(setting)
    save_prefs(self,reg,p,allset)


def set_item_display(self,reg,option,setting):
    """Sets the podcast display preference for video or music sections of the library.

    """
    p = open_prefs(self,reg)
    allset = False
    tab_loc = open_tab(self,p,tab="Podcasts")
    p1 = Region(tab_loc.nearby(500))
    print p1
    print option,setting
    if option == "audio":
        if setting == "on":
            if not p1.exists(Pattern("checked_Show_audio.png").exact()):
                print "audio not checked"
                p1.click("Show audio")
            else:
                allset = True

        if setting == "off":
            if p1.exists(Pattern("checked_Show_audio.png").exact()):
                p1.click("Show audio")
            else:
                allset = True
        
    if option == "video" :
        if setting == "on":
            if not p1.exists(Pattern("checked_Show_vidoes.png").exact()):
                p1.click("Show videos")
            else:
                allset = True

        if setting == "off":
            if p1.exists(Pattern("checked_Show_videos.png").exact()):
                p1.click("Show videos")
            else:
                allset = True     
    save_prefs(self,reg,p,allset)
   
       
def save_prefs(self,reg,p,allset):
    if allset == True or config.get_os_name() == "osx":
        type(Key.ESC)
    else:
        p.click("button_close.png")
        if reg.t.exists("Miro",2):
            click(reg.t.getLastMatch())
    time.sleep(5)
    
