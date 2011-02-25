# All actions on the preferences panel

import config
import testvars
from sikuli.Sikuli import *


def open(self,tl,lang='en'):
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
    self.assertTrue(exists("pref_panel.png"))

def click_pref_tab(self,tab):
    for x in testvars.PREF_PANEL.keys():
        if tab.lower() in x:
            pref_icon = testvars.PREF_PANEL[x]        
    print "going to tab: "+str(tab)
    s.click(pref_icon)    

def set_autodownload_pref(self,tl,m,setting):
    """Set the global autodownload prefernce setting.

    Setting can be "Off, New, or All"
    """
    open_preferences(self,tl)
    click_pref_tab(self,tab)
