from preferences import Preferences
from sikuli.Sikuli import *

class PrefPlaybackTab(Preferences):
    """Specify preferences on the Podcasts tab of the Preferences panel.

    """

    _VIDEO_SECTION = [Pattern("playback_pref_video.png"), "Video Playback"]
    _MUSIC_SECTION = [Pattern("playback__pref_music.png"), "Music Playback"]
    _PODCAST_SECTION = [Pattern("playback_pref_podcast.png"), "Podcast Playback"]
    _RESUME_PLAYBACK = [Pattern("resume_playback.png"), "Resume play"]
    _PLAY_CONINUOUSLY = [Pattern("play_continuously.png"), "Play cont"]
    _PLAY_IN_MIRO = "Play media"
    _POP_OUT_WINDOW = "separate window"
    _SUBTITLES = "movie subtitles"



    def section_sub_region(self, section):
        for x in section:
             if self.sr.exists(x, 2): break
        else:
            print("Can't find the preference field %s" % option)
 
        sect_reg = Region(self.sr.getLastMatch())
        sect_reg.setX(self.sr.getX())
        sect_reg.setW(self.sr.getW())
        print sect_reg.getH()
        sect_reg.setH(sect_reg.getH()*6)
        return sect_reg


    def play_media_in_miro(self, setting):
        option = self._PLAY_IN_MIRO
        self.set_preference_checkbox(option, setting)

    def play_in_popout_window(self, setting):
        option = self._POP_OUT_WINDOW
        self.set_preference_checkbox(option, setting)

    def enable_subtitles_when_available(self, setting):
        option = self._SUBTITLES
        self.set_preference_checkbox(option, setting)

    def play_continuous(self, setting, section):
        """Checks the Play Continuous setting for the specifed file kind.

        Must be: 'Video', 'Music' or 'Podcast'
        """
        sections = {"Video": self._VIDEO_SECTION, 
                    "Music": self._MUSIC_SECTION,
                    "Podcast": self._PODCAST_SECTION
                    }
        if section not in sections.keys():
            print("section must be one of %s" %sections.keys())
        option = self._PLAY_CONINUOUSLY
        section_region = self.section_sub_region(sections[section])
        self.set_preference_checkbox(option, setting, subsection_region=section_region)


    def resume_playback(self, setting, section):
        """Checks the Resume Playback setting for the specifed file kind.

        Must be: 'Video', 'Music' or 'Podcast'
        """


        sections = {"Video": self.VIDEO_SECTION, 
                    "Music": self._MUSIC_SECTION,
                    "Podcast": self_PODCAST_SECTION,
                    }

        if section not in sections.keys():
           print("section must be one of %s" %sections.keys())
        option = self._RESUME_PLAYBACK
        section_region = self.section_sub_region(section)
        self.set_preference_checkbox(option, setting, subsection_region=section_region)
