# All actions on the preferences panel

import config
import testvars
import mirolib
from sikuli.Sikuli import *


def open_prefs(self,reg,lang='en',menu=None,option=None):
    """OS specific handling for Preferences menu, since it differs on osx and windows.

    """
    if reg.s.exists("icon-search.png",3) or \
       reg.s.exists("icon-video.png",3):
        click(reg.s.getLastMatch())
    time.sleep(3)
    if lang == 'en':
        option = 'Preferences'
        sc = 'f'
    else:
        sc = menu[0].lower()
    #Open the Preferences Menu based on the os with keyboard navigation
    if config.get_os_name() == "osx":
        mirolib.shortcut(',')
        pr = Region(reg.m)
    else:
        myscreen = Screen()
        pr = Region(myscreen.getBounds())
        type(sc,KEY_ALT)
        reg.t.click(option)
        time.sleep(2)             
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

def set_default_view(self,reg,setting="Standard view"):
    """Set the global podcast default view prefernce.

    Setting can be "Standard" or "List"
    """
    allset = False
    p = open_prefs(self,reg)
    r = Region(open_tab(self,p,tab="Podcasts").below())
    r.setW(800)
    r.highlight(1)
    new_setting = setting.capitalize() +" view"

    if r.exists(new_setting):
        allset = True
    else:
        if new_setting == "Standard":
            r.click("List view")
            r.click("Standard view")
        elif new_setting == "List view":
            r.click("Standard view")
            r.click("List view")
    save_prefs(self,reg,p=r,allset=allset)


def set_autodownload(self,reg,setting="Off"):
    """Set the global autodownload prefernce setting.

    Setting can be "Off, New, or All"
    """
    allset = False
    p = open_prefs(self,reg)
    r = Region(open_tab(self,p,tab="Podcasts")).right(400).below(300)
    ry = r.getY()+100
    r.setY(ry)
    r.highlight(1)

    if r.exists("download setting",2):
        print "found download setting"
    elif r.exists("Auto-download",2):
        print "found auto-download"
    r1 = Region(r.getLastMatch().right(200))
    r2 = Region(r1.nearby(150))
    r2.highlight(1)

    if r1.exists(setting):
        allset = True
    else:
        click(r1.getCenter())
        if not r2.exists(setting):
            type(Key.PAGE_DOWN)
        if not p.exists(setting):
            type(Key.PAGE_UP)
        r2.click(setting)
    save_prefs(self,reg,p=p,allset=allset)

def set_item_display(self,reg,option,setting):
    """Sets the podcast display preference for video or music sections of the library.

    """
    p = open_prefs(self,reg)
    allset = False
    p1 = Region(open_tab(self,p,tab="Podcasts").right(600).below(300))
    p1.setX(p1.getX()-250)
    
    if option == "audio":
       allset = check_the_box(search_reg=p1,phrase="Show audio",setting=setting)
        
    if option == "video" :
        allset = check_the_box(search_reg=p1,phrase="Show videos",setting=setting)  
    save_prefs(self,reg,p,allset=allset)

def check_the_box(search_reg,phrase,setting):
    print phrase,setting
    allset = False
    search_reg.find(phrase)
    r1 = Region(search_reg.getLastMatch().left(80)).nearby(10)
    if setting == "off":
        if r1.exists(Pattern("prefs_checkbox.png")):
            click(search_reg.getLastMatch())
        else:
            allset=True
    if setting == "on":
        if not r1.exists(Pattern("prefs_checkbox.png")):
            click(search_reg.getLastMatch())
        else:
            allset="True"
        print allset
        return allset
       
def save_prefs(self,reg,p,allset):
    if allset == True or \
       config.get_os_name() == "osx":
        type(Key.ESC)
    else:
        if p.exists(Pattern("button_close.png"),5) or \
           p.exists("Close",5):
            click(p.getLastMatch())
        if reg.t.exists("Miro",2):
            click(reg.t.getLastMatch())
    time.sleep(2)
    
