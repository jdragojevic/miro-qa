# All actions on the preferences panel

from sikuli.Sikuli import *
from miro_app import MiroApp



class PreferencesPanel(MiroApp):

    _PREF_HEADING = Pattern("pref_heading.png")

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


    _CLOSE_BUTTON = Pattern("button_close.png")
    _PREFS_CHECKBOX = Pattern("prefs_checkbox.png")
    _OPTION_EXPAND = Pattern("prefs_expand_option.png")
    _OPTION_LEFT_SIDE = Pattern("prefs_option_left_side.png")



    def preference_panel_regions(self):
        find(self._PREF_HEADING)
        heading = Region(getLastMatch())
        tr = Region(getLastMatch().left(200))
        tr.find(self._GENERAL_TAB)
        trr = Region(tr.getLastMatch())
        heading.setX(heading.getX() - trr.getW())
        settings = heading.below()
        return (heading, settings)
            

            
    def open_tab(self,tab):
        """Open of of the preferences panel tabs.

        Valid values are ['General', 'Podcasts', 'Downloads', 'Folders', 'Diskspace',
                          'Playback', 'Sharing', 'Conversions', 'Stores' 'Extensions']
        """
        print "opening tab"
        pref_tabs = {"General":             self._GENERAL_TAB, \
                     "Podcasts":            self._PODCASTS_TAB, \
                     "Downloads":           self._DOWNLOADS_TAB, \
                     "Folders":             self._FOLDERS_TAB, \
                     "DiskSpace":           self._DISK_SPACE_TAB, \
                     "Playback":            self._PLAYBACK_TAB, \
                     "Sharing":             self._SHARING_TAB , \
                     "Conversions":         self._CONVERSION_TAB, \
                     "Stores":              self._STORES_TAB, \
                     "Extensions":          self._EXTENSTIONS_TAB, \
                     }
        
        if tab not in pref_tabs.keys():
            raise Exception("A valid pref tab must be provided. Valid values are ['General', \
                            'Podcasts', 'Downloads', 'Folders', ...]")
                                    
        #Open the specified tab by searching within the preferences region (p) for the icon.
        print "going to the %s tab" % tab

        heading, settings = self.preference_panel_regions()
        heading.click(pref_tabs[tab])
        return settings

        

    def close_prefs(self):
        _, sr = self.preference_panel_regions()
        
        if self.os_name == "osx":
            type(Key.ESC)
        else:
            if sr.exists(self._CLOSE_BUTTON,3) or \
               sr.exists("Close",3):
                click(sr.getLastMatch())
        #restore focus back to Miro
        if self.os_name == "lin":
            click("Miro")
        else:
            self.miro_focus()

    def set_preference_checkbox(self, option, setting):
        """Check or uncheck the box for a preference setting.
        Assumes you are on the correct tab

        Valid values are ['on' and 'off']

        """
        valid_settings = ['on', 'off']
        if setting not in valid_settings:
            raise Exception("valid setting value not proviced, must be 'on' or 'off'")
        
        _, settings_region = self.preference_panel_regions()
        self.check_the_box(option, setting)
        

    def check_the_box(self, phrase, setting):
        _, sr = self.preference_panel_regions()


        found = False
        for x in phrase:
            if not found and sr.exists(x, 1):
                sr_loc = Region(sr.getLastMatch())
                found = True
            else:
                raise Exception("Can't find the preference field %s" % phrase)

        print sr_loc
        sr1 = Region(sr.getX(), sr_loc.getY()-15, 400, 30) #location of associated checkbox
#        sr1 = Region(sr.getX(), sr_loc.getY()-15, sr_loc.getX()-sr.getX(), 30) #location of associated checkbox
        print sr1
        sr1.click(Pattern(self._PREFS_CHECKBOX))
        
##        if setting == "off":
##            if sr1.exists(Pattern(self._PREFS_CHECKBOX)):
##                click(sr1.getLastMatch())
##        if setting == "on":
##            if not sr1.exists(Pattern(self._PREFS_CHECKBOX)):
##                click(sr1.getLastMatch())
        


    def select_menu_value(self, option, setting, width=120, yoffset=200, multipage = False):
        """For preference settings that have a pull-down menu.

        To account for variations in finding text in various os - option
        is a list of strings to search.
        
        """

        _, sr = self.preference_panel_regions()

        #Locate the preference setting in the panel or fail.
        for x in options:
            if sr.exists(x, 3): break 
            else:
                raise Exception("Can't find the preference field")

        #Set the pull-down menu region
        if multipage == True: #will need to page up and down to locate option.
            pgs = 3
        else:
            pgs = 1
        
        sr1 = Region(sr.getLastMatch().right(200))
        menu_pos = Location(sr1.find(self._OPTION_EXPAND))
        rmx = menu_pos.getX()
        rmy = menu_pos.getY()
        mr = Region(rmx-width,rmy-yoffset,width,yoffset*2)
        mr.highlight(1)
        if mr.exists(new_setting):
            print "pref already set"
        else: #Locate the setting value in the menu.
            click(menu_pos)
            value_found = False
            for x in range(0,pgs):
                if not mr.exists(setting,1):
                    type(Key.PAGE_DOWN)
                else:
                    value_found = True
                   
            if pgs > 1 and value_found == False:
                    for x in range(0,pgs*2):
                        if not exists(setting,1):
                            type(Key.PAGE_UP)
                        else:
                            value_found = True
            #Click the found value or fail if value wasn't found.
            if value_found == True:
                click(mr.getLastMatch())
            else:
                raise Exception("Can't find the preference value")


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
                                     
                                       


##def set_default_view(self,reg,setting="Standard"):
##        """Set the global podcast default view prefernce.
##
##        Setting can be "Standard" or "List"
##        """
##        allset = False
##        p = open_prefs(self,reg)
##        r = Region(open_tab(self,p,tab="Podcasts")).right(400).below(300)
##        ry = r.getY()+100
##        r.setY(ry)
##        r.highlight(3)
##        new_setting = setting.capitalize()
##
##        if r.exists("Defau",2):
##            print "found Default"
##        elif r.exists("Default view",2):
##            print "found Default view"
##
##
##        r1 = Region(r.getLastMatch().right(200))
##        r2 = Region(r1.nearby(150))
##        r2.highlight(1)
##
##        
##        if r2.exists(new_setting):
##            allset = True
##        else:
##            if new_setting == "Standard":
##                r2.click("List")
##                r2.click("Standard")
##            elif new_setting == "List":
##                r2.click("Standard")
##                r2.click("List")
##        save_prefs(self,reg,p=p,allset=allset)
##
##
##def set_autodownload(self,reg,setting="Off"):
##        """Set the global autodownload prefernce setting.
##
##        Setting can be "Off, New, or All"
##        """
##        allset = False
##        p = open_prefs(self,reg)
##        r = Region(open_tab(self,p,tab="Podcasts")).right(400).below(300)
##    #    r.setY(r.getY()+100)
##
##        if r.exists("download setting",2):
##            print "found download setting"
##        elif r.exists("Auto-download",2):
##            print "found auto-download"
##        else:
##            self.fail("Autodownload setting not found, can not set preference")
##        click(r.getLastMatch())
##        r1 = Region(r.getLastMatch().right(200))
##        r1a = Location(r1.getCenter())
##        r2 = Region(int(r1a.getX()-100),int(r1a.getY())-130,150,180)
##        r2.highlight(5)
##
##        if r1.exists(setting):
##            allset = True
##        else:
##            click(r1a)
##            r2.click(setting)
##        save_prefs(self,reg,p=p,allset=allset)
##
##    def set_item_display(self,reg,option,setting):
##        """Sets the podcast display preference for video or music sections of the library.
##
##        """
##        p = open_prefs(self,reg)
##        allset = False
##        
##    ##    p1.setX(p1.getX()-250)
##    ##    p1.highlight(3)
##        
##        if option == "audio":
##           allset = check_the_box(search_reg=p, phrase="Show audio", setting=setting)
##            
##        if option == "video" :
##            allset = check_the_box(search_reg=p, phrase="Show videos", setting=setting)  
##        save_prefs(self,reg,p,allset=allset)
##
##    def remove_watched_folder(self,reg,folder):
##        """Sets the podcast display preference for video or music sections of the library.
##
##        """
##        p = open_prefs(self,reg)
##        allset = True
##        p1 = Region(open_tab(self,p,tab="Folders").below())
##        p1.setX(p1.getX()-250)
##        p1.setW(p1.getW()+800)
##        p1.highlight(3)
##        p1.find("Watch")
##        p2 = Region(p1.getLastMatch().below())
##        p2.setW(p1.getW())
##        
##
##        watched = folder.split('/')
##        while watched:
##            curr = watched.pop()
##            if p2.exists(curr):
##                print "found",curr
##                click(p2.getLastMatch())
##                p2.click("Remove")
##        save_prefs(self,reg,p,allset=allset)
##
##
##


        
