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
            raise Exception("A valid pref tab must be provided. Valid values are ['General', \
                            'Podcasts', 'Downloads', 'Folders', ...]")
                                    
        #Open the specified tab by searching within the preferences region (p) for the icon.
        print "going to the %s tab" % tab
        self.hr.click(pref_tabs[tab][0])
        time.sleep(5)
        return pref_tabs[tab][1]

                                     
                                    
