from preferences_panel import PreferencesPanel


class PrefGeneralTab(PreferencesPanel):
    """Specify preferences on the Podcasts tab of the Preferences panel.

    """

    _RUN_ON_LOGIN = ["Automatically"]
    _REMEMBER_SCREEN_ON_STARTUP = ["remember"]
    _WARN_ON_QUIT_WITH_DOWNLOADS = ["downloads in"]
    _WARN_ON_QUIT_WITH_CONVERSIONS = ["conversions in"]
    _SHOW_VIDEOS = ["Show videos"]
    _SHOW_AUDIO =  ["Show audio"]
    _DEFAULT_LANG = ["Display in"]
    _TRAY_ICON = ["Enable tray"]

    def automatically_run_on_login(self, setting):
        option = self._RUN_ON_LOGIN
        self.set_preference_checkbox(option, setting)

    def remember_last_screen_on_startup(self, setting):
        option = self._REMEMBER_SCREEN_ON_STARTUP
        self.set_preference_checkbox(option, setting)

    def warn_on_quit_with_downloads(self, setting):
        option = self._WARN_ON_QUIT_WITH_DOWNLOADS
        self.set_preference_checkbox(option, setting)

    def warn_on_quit_with_conversions(self, setting):
        option = self._WARN_ON_QUIT_WITH_CONVERSIONS
        self.set_preference_checkbox(option, setting)
        
    def show_videos_in_videos(self, setting):
        option = self._SHOW_VIDEOS
        self.set_preference_checkbox(option, setting)

    def show_audio_in_music(self, setting):
        option = self._SHOW_AUDIO
        self.set_preference_checkbox(option, setting)
