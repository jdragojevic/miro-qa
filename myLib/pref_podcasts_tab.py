from preferences import Preferences
from sikuli.Sikuli import *

class PrefPodcastsTab(Preferences):
    """Specify preferences on the Podcasts tab of the Preferences panel.

    """

    _CHECK_FOR_NEW_CONTENT =  ["content"]
    _AUTODOWNLOAD = ["Auto-download", "download", "setting:"]
    _DEFAULT_VIEW = ["view", "Default view", "Default"]
    _REMEMBER_OLD_ITEMS = ["Remember", "old items"]
        
    
    def check_for_new_content_setting(self, setting):
        option = self._CHECK_FOR_NEW_CONTENT
        self.select_menu_value(option, setting, menu_width=500, yoffset="120")

    def autodownload_setting(self, setting):
        option = self._AUTODOWNLOAD
        self.select_menu_value(option=option, setting=setting, menu_width=500, yoffset=180)
        
    def default_view_setting(self, setting):
        option = self._DEFAULT_VIEW
        self.select_menu_value(option, setting, menu_width=500, yoffset="180")

    def remember_old_items_setting(self, setting):
        option = self._REMEMBER_OLD_ITEMS
        self.select_menu_value(option, setting, menu_width=500, yoffset="120")
        
