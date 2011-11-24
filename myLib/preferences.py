# All actions on the preferences panel

import time
from sikuli.Sikuli import *
import config
from miro_app import MiroApp


class Preferences(MiroApp):

    _GENERAL_TAB = "General"
    _PODCASTS_TAB = "Podcasts"
    _DOWNLOADS_TAB = "Downloads"
    _FOLDERS_TAB = "Folders"
    _DISK_SPACE_TAB = "Disk"
    _PLAYBACK_TAB = "Playback"
    _SHARING_TAB = "Sharing"
    _CONVERSION_TAB = "Conversions"
    _STORES_TAB = "Stores"
    _EXTENSTIONS_TAB = "Extensions"
    _PANEL_ERROR = Pattern("pref_panel_error.png")


    _CLOSE_BUTTON = [Pattern("button_close.png"), "Close"]
    _PREFS_CHECKBOX_CHECKED = Pattern("prefs_checkbox.png")
    _PREFS_CHECKBOX_NOT_CHECKED = Pattern("prefs_checkbox_unchecked.png")

    _OPTION_EXPAND = Pattern("prefs_expand_option.png")
    _OPTION_LEFT_SIDE = Pattern("prefs_option_left_side.png")
    
    def __init__(self):
        self.os_name = config.get_os_name()
        PREF_HEADING = Pattern("pref_heading.png")
        
        def preference_panel_regions():
            find(PREF_HEADING)
            heading = Region(getLastMatch())
            gtw = heading.getW()/10
            heading.setX(heading.getX() - gtw)
            heading.setW(heading.getW() + gtw*2)
            heading.setH(heading.getH() + 30)
            heading.setAutoWaitTimeout(10)
            settings = Region(heading.below())
            settings.setAutoWaitTimeout(10)
            return (heading, settings)
        

        def screen_region():
            myscreen = Screen()
            screen = Region(myscreen.getBounds())
            return screen
        
        self.hr, self.sr = preference_panel_regions()
        self.screen = screen_region()        

    def close_prefs(self):
               
        if self.os_name == "osx":
            type(Key.ESC)
        else:
            for x in self._CLOSE_BUTTON:
                if self.sr.exists(x, 2): break
            else:
                print("Can't find the close button")
        click(self.sr.getLastMatch())
        #restore focus back to Miro
        if self.os_name == "lin":
            click("Miro")
        else:
            self.miro_focus()

    def set_preference_checkbox(self, option, setting, subsection_region=None):
        """Check or uncheck the box for a preference setting.
        Assumes you are on the correct tab

        Valid values are ['on' and 'off']

        """
        if not subsection_region == None:
            pref_reg = subsection_region
        else:
            pref_reg = self.sr
        valid_settings = ['on', 'off']
        if setting not in valid_settings:
            print("valid setting value not proviced, must be 'on' or 'off'")
        #CHECK THE BOX
        for x in option:
             if pref_reg.exists(x, 2): break
        else:
            print("Can't find the preference field %s" % option)
        sr_loc = Region(pref_reg.getLastMatch())
        sr1 = Region(pref_reg.getX(), sr_loc.getY()-10, pref_reg.getW(), 30) #location of associated checkbox
                   
        if setting == "off":
            if sr1.exists(self._PREFS_CHECKBOX_CHECKED):
               click(sr1.getLastMatch())
        if setting == "on":
            if sr1.exists(self._PREFS_CHECKBOX_NOT_CHECKED):
                sr1.click(sr1.getLastMatch())
        


    def select_menu_value(self, option, setting, menu_width, yoffset=200, multipage = False):
        """For preference settings that have a pull-down menu.

        To account for variations in finding text in various os - option
        is a list of strings to search.
        
        """
    
        #Locate the preference setting in the panel or fail.
        for x in option:
            if self.sr.exists(x, 3): break
        else:
            print("Can't find the preference field %s" % x)
        sr_loc = Region(self.sr.getLastMatch())
        sr1 = Region(self.sr.getX(), sr_loc.getY()-10, self.sr.getW(), 30)

        #Set the pull-down menu region
        if multipage == True: #will need to page up and down to locate option.
            pgs = 3
        else:
            pgs = 1
        sr1.highlight(1)      
        menu_pos = Region(sr1.find(self._OPTION_EXPAND))
        print menu_pos
        rmx = menu_pos.getX() - menu_width
        sr = self.sr
        if yoffset == "top":
            sr = self.screen
            rmy = 0
            rmh = sr.getH()
        else:
            rmy = menu_pos.getY() - int(yoffset)
            rmh = int(yoffset)*2+10
            
        mr = Region(rmx, rmy, menu_width, rmh)
        mr.setAutoWaitTimeout(5)
        mr.highlight(1)
        if mr.exists(setting):
            print "pref already set"
        else: #Locate the setting value in the menu.
            click(menu_pos)
            value_found = False
            for x in range(0,pgs):
                print mr
                if mr.exists(setting):
                    value_found = True        
                else:
                     type(Key.PAGE_DOWN)              
            if pgs > 1 and value_found == False:
                    for x in range(0,pgs*2):
                        if mr.exists(setting,1):
                            value_found = True
                        else:
                            type(Key.PAGE_UP)
                            
            #Click the found value or fail if value wasn't found.
            if value_found == True:
                mr.click(setting)
            else:
                print("Can't find the preference value")


    def check_type_text(self, option, setting):
        """For preference settings that have a checkbox and text entry.

        """
        pass
    def pref_text_entry(self, option, setting):
        """For preference settings that require text entry.

        """
        pass
    
    def pref_tables(self, option, settign):
        """preference tables.

        """
        pass
                                     
                                    
