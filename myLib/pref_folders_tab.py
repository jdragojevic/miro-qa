from preferences_panel import PreferencesPanel


class PrefFoldersTab(PreferencesPanel):
    """Specify preferences on the Podcasts tab of the Preferences panel.

    """

    _CHECK_FOR_NEW_CONTENT =  ["content"]
    _AUTO-DOWNLOAD = ["Auto-download", "download"]
    _DEFAULT_VIEW = ["view", "Default view"]
    _REMEMBER_OLD_ITEMS = ["Remember", "old items"]

    _ADD_BUTTON = ["Add", Pattern('button_add.png')]
    _REMOVE_BUTTON = ["Add", Pattern('button_add.png')]
    _CHANGE_BUTTON = ["Change"]
    
        
    
    def video_storage_setting(self, directory):
        _, sr = self.preference_panel_regions()
        self.click_element(self._CHANGE_BUTTON, sr)
        self.type_a_path(self, folder)

    def add_watched_folder(self, folder, setting):
        _, sr = self.preference_panel_regions()
        self.click_element(self._ADD_BUTTON, sr)
        self.type_a_path(self, folder)
        
        
    def remove_watched_folder(self, folder, setting):
        _, sr = self.preference_panel_regions()
        wf_reg = self.find_element([folder], sr)
        click(wf_reg.getLastMatch())
        self.click_element(self._REMOVE_BUTTON, sr)

    def toggle_watched_folder(self, folder, setting):
        set_preference_checkbox(self, [folder], setting)
        
