from preferences import Preferences
from sikuli.Sikuli import *



class PrefFoldersTab(Preferences):
    """Specify preferences on the Podcasts tab of the Preferences panel.

    """
    _ADD_BUTTON = ["Add", Pattern('button_add.png')]
    _REMOVE_BUTTON = ["Add", Pattern('button_add.png')]
    _CHANGE_BUTTON = ["Change"]
    
        
    
    def video_storage_setting(self, directory):
        self.click_element(self._CHANGE_BUTTON)
        self.type_a_path(self, folder)

    def add_watched_folder(self, folder, setting):
        self.click_element(self._ADD_BUTTON)
        self.type_a_path(self, folder)
        
        
    def remove_watched_folder(self, folder):
        wf_reg = self.find_element([folder])
        click(wf_reg.getLastMatch())
        self.click_element(self._REMOVE_BUTTON)

    def toggle_watched_folder(self, folder, setting):
        set_preference_checkbox(self, [folder], setting)
        
