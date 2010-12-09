#testvars.py
"""Specify the test variables and image locations.

"""

import os
import config





#Defines the image locations

#Menus

##= {"sidebar":"sidebar_menu.png" , \
##         "new_folder":"sidebar_new_folder.png", \
##        }
##
##Buttons = {"create_folder":"create_folder.png", \
##           "video_radio":"video_radio.png", \
##           "video_radio_selected":"video_radio_selected.png", \
##           "audio_radio":"audio_radio.png", \
##           "audio_radio_selected":"audio_radio_selected.png", \
##        }
##
##
##Icons = {"miro_tray":"miro_tray.png", \
##         "miro_tray_active":"miro_active_tray.png", \
##        }
##


##Sidebar
side_imgs = os.path.join(config.miro_images(),"Sidebar")
guide_icon = os.path.join(side_imgs,"icon-guide_large.png")
search_icon = os.path.join(side_imgs,"icon-search_large.png")
video_icon = os.path.join(side_imgs,"icon-video_large.png")
audio_icon = os.path.join(side_imgs,"icon-audio_large.png")
other_icon = os.path.join(side_imgs,"icon-other_large.png")
conversions_icon = os.path.join(side_imgs,"icon-conversions_large.png")
downloading_icon = os.path.join(side_imgs,"icon-downloading.png")
playlist_icon = os.path.join(side_imgs,"icon-playlist_large.png")

##Preferences panel
pref_imgs = os.path.join(config.miro_images(),"Prefs")
pref_general = os.path.join(pref_imgs,"pref-tab-general.png")
pref_feeds = os.path.join(pref_imgs,"pref-tab-feeds.png")
pref_downloads = os.path.join(pref_imgs,"pref-tab-downloads.png")
pref_folders = os.path.join(pref_imgs,"pref-tab-folders.png")
pref_diskspace = os.path.join(pref_imgs,"pref-tab-disk-space.png")
pref_playback = os.path.join(pref_imgs,"pref-tab-playback.png")
pref_convesions = os.path.join(pref_imgs,"pref-tab-conversions.png")




#Misc

misc_imgs = os.path.join(config.miro_images(),"Misc")
one_click_badge = os.path.join(misc_imgs,"patrace1.png")
