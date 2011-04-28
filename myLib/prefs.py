# All actions on the preferences panel

import config
import testvars
import mirolib
from sikuli.Sikuli import *


def open_prefs(self,reg,lang='en',menu=None,option=None):
    """OS specific handling for Preferences menu, since it differs on osx and windows.

    """
    #Open the Preferences Menu based on the os
    if lang == 'en':
        if config.get_os_name() == "osx":
            click("Miro_Menu.png")
        elif config.get_os_name() == "win":
            click("File")
        elif config.get_os_name() == "lin":
            click("File")
        else:
            print config.get_os_name()
        #Choose the Preferences menu option
        click("Preferences")
        time.sleep(2)
        #Click the dialog heading name to activate it
        click("Preferences")
        self.assertTrue(exists("pref_heading.png"))
        PrefRegion = Region(getLastMatch().below(600))
        
    else:
        if config.get_os_name() == "osx":
            mirolib.shortcut(',')
        elif config.get_os_name() == "win" or config.get_os_name() == "lin":
            reg.t.click(menu)
            time.sleep(2)
            reg.t.click(option)
        else:
            print config.get_os_name()
        myScreen = Screen(0)
        PrefRegion = myScreen.getBounds()
    
    return PrefRegion


def open_tab(self,reg,p,tab):
    """Open the specified tab by searching with-in the preferences region (p) for the icon.

    """
    for x in testvars.PREF_PANEL.keys():
        if tab.lower() in x:
            pref_icon = testvars.PREF_PANEL[x]        
    print "going to tab: "+str(tab)
    ph = Region(find("pref_heading.png"))
    ph.click(pref_icon)

def set_autodownload(self,reg,setting):
    """Set the global autodownload prefernce setting.

    Setting can be "Off, New, or All"
    """
    open_prefs(self,tl)
    open_tab(self,tab)
