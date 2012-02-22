# All actions on the preferences panel

import time
from sikuli.Sikuli import *
import config
from preferences import Preferences
from pref_general_tab import PrefGeneralTab
from pref_folders_tab import PrefFoldersTab
from pref_podcasts_tab import PrefPodcastsTab
from pref_playback_tab import PrefPlaybackTab

class PreferencesPanel(Preferences):

    _GENERAL_TAB = ["General", "pref_tab_general.png"]
    _PODCASTS_TAB = ["Podcasts", "pref_tab_feeds.png"]
    _DOWNLOADS_TAB = ["Downloads", "pref_tab_downloads.png"]
    _FOLDERS_TAB = ["Folders", "pref_tab_folders.png"]
    _DISK_SPACE_TAB = ["Disk", "pref_tab_disk_space.png"]
    _PLAYBACK_TAB = ["Playback", "pref_tab_playback.png"]
    _SHARING_TAB = ["Sharing", "pref_tab_sharing.png"]
    _CONVERSION_TAB = ["Conversions", "pref_tab_conversions.png"]
    _STORES_TAB = ["Stores", "pref_tab_stores.png"]
    _EXTENSTIONS_TAB = ["Extensions", "pref_tab_extensions.png"]
    
    _PANEL_ERROR = Pattern("pref_panel_error.png")


    _CLOSE_BUTTON = Pattern("button_close.png")
    _PREFS_CHECKBOX_CHECKED = Pattern("prefs_checkbox.png")
    _PREFS_CHECKBOX_NOT_CHECKED = Pattern("prefs_checkbox_unchecked.png")

    _OPTION_EXPAND = Pattern("prefs_expand_option.png")
    _OPTION_LEFT_SIDE = Pattern("prefs_option_left_side.png")
    
           
    def open_tab(self, tab):
        """Open of of the preferences panel tabs.

        Valid values are ['General', 'Podcasts', 'Downloads', 'Folders', 'Diskspace',
                          'Playback', 'Sharing', 'Conversions', 'Stores' 'Extensions']
        """
        pref_tabs = {"General":             [self._GENERAL_TAB, PrefGeneralTab() ], \
                     "Podcasts":            [self._PODCASTS_TAB, PrefPodcastsTab() ], \
                     "Downloads":           [self._DOWNLOADS_TAB, ], \
                     "Folders":             [self._FOLDERS_TAB, PrefFoldersTab() ], \
                     "DiskSpace":           [self._DISK_SPACE_TAB, ], \
                     "Playback":            [self._PLAYBACK_TAB, PrefPlaybackTab() ], \
                     "Sharing":             [self._SHARING_TAB , ], \
                     "Conversions":         [self._CONVERSION_TAB, ], \
                     "Stores":              [self._STORES_TAB, ], \
                     "Extensions":          [self._EXTENSTIONS_TAB, ], \
                     }
        
        if tab not in pref_tabs.keys():
            print("A valid pref tab must be provided. Valid values are ['General', \
                            'Podcasts', 'Downloads', 'Folders', ...]")
                                    
        #Open the specified tab by searching within the preferences region (p) for the icon.
        print "going to the %s tab" % tab

        for x in pref_tabs[tab][0]:
                if self.hr.exists(x, 2): break
        else:
            print("Can't find the preferenes %s tab" % tab)
        click(self.hr.getLastMatch())
        time.sleep(3)
        return pref_tabs[tab][1]

                                     
                                    
