# All actions on the preferences panel

import config
import testvars
import mirolib
from sikuli.Sikuli import *


def open_prefs(self,reg,lang='en',menu=None,option=None):
    """OS specific handling for Preferences menu, since it differs on osx and windows.

    """
    #Open the Preferences Menu based on the os with keyboard navigation
    if config.get_os_name() == "osx":
        mirolib.shortcut(',')
    else:
        type('f',KEY_ALT)
        if lang == 'en':
            click("Preferences")
            reg.t.click(option)
    myScreen = Screen(0)
    PrefRegion = myScreen.getBounds()
    PrefRegion.highlight(4)
    return PrefRegion


def open_tab(self,p,tab):
    """Open the specified tab by searching with-in the preferences region (p) for the icon.

    """
    for x in testvars.PREF_PANEL.keys():
        if tab.lower() in x:
            pref_icon = testvars.PREF_PANEL[x]        
    print "going to tab: "+str(tab)
    p.click(pref_icon)

def set_autodownload(self,reg,setting="Off"):
    """Set the global autodownload prefernce setting.

    Setting can be "Off, New, or All"
    """
    p = open_prefs(self,reg)
    open_tab(self,p,tab="Podcasts")
    p.find("Auto-download setting")
    p1 = Region(p.getLastMatch().left(200))
    p2 = p1.nearby(200)
    if p1.exists(setting):
        print "pref already set"
    else:
        click(p1.getCenter())
    if not p2.exists(setting):
        type(Key.PAGE_DOWN)
    f.click(setting)
        
    f.click("Close")
    


def set_item_display(self,reg,option="audio",setting="on"):
    """Sets the podcast display preference for video or music sections of the library.

    """
    p = open_prefs(self,reg)        
    open_tab(self,p,tab="Podcasts")
    if option == "audio" and setting == "on":
        if not p.exists("checked_Show_audio"):
            p.click("Show audio")
    elif option == "audio" and setting == "off":
        if p.exists("checked_Show_audio"):
            p.click("Show audio")
    elif option == "video" and setting == "on":
        if not p.exists("checked_Show_videos"):
            p.click("Show videos")
    elif option == "videos" and setting == "off":
        if p.exists("checked_Show_videos"):
            p.click("Show videos")
            
        
    
