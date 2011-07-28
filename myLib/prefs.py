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
    if exists("Preferences") and config.get_os_name() == "osx":
        pr = Region(getLastMatch().below(150))
        pr.setX(pr.getX()-250)
        pr.setW(pr.getW()+500)
    else:
        pr = Region(p)
    pr.highlight(5)
    for x in testvars.PREF_PANEL.keys():
        if tab.lower() in x:
            pref_icon = testvars.PREF_PANEL[x]        
    print "going to tab: "+str(tab)
    if pr.exists(Pattern(pref_icon),5) or pr.exists(tab.capitalize(),5):
        tab_loc = Region(pr.getLastMatch())
        click(tab_loc)
        return tab_loc
    else:
        self.fail(tab+" tab not found")

def set_default_view(self,reg,setting="Standard"):
    """Set the global podcast default view prefernce.

    Setting can be "Standard" or "List"
    """
    allset = False
    p = open_prefs(self,reg)
    r = Region(open_tab(self,p,tab="Podcasts")).right(400).below(300)
    ry = r.getY()+100
    r.setY(ry)
    r.highlight(3)
    new_setting = setting.capitalize()

    if r.exists("Defau",2):
        print "found Default"
    elif r.exists("Default view",2):
        print "found Default view"


    r1 = Region(r.getLastMatch().right(200))
    r2 = Region(r1.nearby(150))
    r2.highlight(1)

    
    if r2.exists(new_setting):
        allset = True
    else:
        if new_setting == "Standard":
            r2.click("List")
            r2.click("Standard")
        elif new_setting == "List":
            r2.click("Standard")
            r2.click("List")
    save_prefs(self,reg,p=p,allset=allset)


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
    p1.highlight(3)
    
    if option == "audio":
       allset = check_the_box(search_reg=p1,phrase="Show audio",setting=setting)
        
    if option == "video" :
        allset = check_the_box(search_reg=p1,phrase="Show videos",setting=setting)  
    save_prefs(self,reg,p,allset=allset)

def remove_watched_folder(self,reg,folder):
    """Sets the podcast display preference for video or music sections of the library.

    """
    p = open_prefs(self,reg)
    allset = True
    p1 = Region(open_tab(self,p,tab="Folders").below())
    p1.setX(p1.getX()-250)
    p1.setW(p1.getW()+800)
    p1.highlight(3)
    p1.find("Watch")
    p2 = Region(p1.getLastMatch().below())
    p2.setW(p1.getW())
    

    watched = folder.split('/')
    while watched:
        curr = watched.pop()
        if p2.exists(curr):
            print "found",curr
            click(p2.getLastMatch())
            p2.click("Remove")
    save_prefs(self,reg,p,allset=allset)



def set_preference_checkbox(self,reg,tab,option,setting):
    """Check or uncheck the box for a preference setting.

    Setting can be either 'on' or 'off'

    """
    p = open_prefs(self,reg)
    allset = False

    if tab=="General":
        print "already on tab"
    else:
        open_tab(self,p,tab)

    allset = check_the_box(search_reg=p,phrase=option,setting=setting)
    save_prefs(self,reg,p,allset=allset)

def check_the_box(search_reg,phrase,setting):
    if search_reg == "screen":
        myscreen = Screen()
        search_reg = Region(myscreen.getBounds())
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
    
