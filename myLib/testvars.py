#testvars.py
"""Specify the test variables and image locations.

"""

import os
import config





timeout = 30

##Sidebar
side_imgs = os.path.join(config.miro_images(),"Sidebar")
TAB_LARGE_ICONS = {"guide_icon": os.path.join(side_imgs,"icon-guide_large.png"),
                 "search_icon": os.path.join(side_imgs,"icon-search_large.png"),
                 "video_icon": os.path.join(side_imgs,"icon-video_large.png"),
                 "music_icon": os.path.join(side_imgs,"icon-audio_large.png"),
                 "other_icon": os.path.join(side_imgs,"icon-other_large.png"),
                 "conversions_icon": os.path.join(side_imgs,"icon-conversions_large.png"),
                 "downloading_icon": os.path.join(side_imgs,"icon-downloading_large.png"),
                 "playlist_icon": os.path.join(side_imgs,"icon-playlist_large.png"),
                 }

##Preferences panel
pref_imgs = os.path.join(config.miro_images(),"Prefs")
pref_general = os.path.join(pref_imgs,"pref-tab-general.png")
pref_feeds = os.path.join(pref_imgs,"pref-tab-feeds.png")
pref_downloads = os.path.join(pref_imgs,"pref-tab-downloads.png")
pref_folders = os.path.join(pref_imgs,"pref-tab-folders.png")
pref_diskspace = os.path.join(pref_imgs,"pref-tab-disk-space.png")
pref_playback = os.path.join(pref_imgs,"pref-tab-playback.png")
pref_conversions = os.path.join(pref_imgs,"pref-tab-conversions.png")

#MiroGuide

mg = os.path.join(config.miro_images(),"MiroGuide")
guide_add_feed = os.path.join(mg,"add_feed.png")
guide_search = os.path.join(mg,"guide_search.png")

#Search
search_imgs = os.path.join(config.miro_images(),"Search")
blip_icon = os.path.join(search_imgs,"search_icon_bliptv.png")
youtube_icon = os.path.join(search_imgs,"search_icon_youtube.png")
youtube_user_icon = os.path.join(search_imgs,"search_icon_youtubeuser.png")
all_icon = os.path.join(search_imgs,"search_icon_all.png")


#Misc

misc_imgs = os.path.join(config.miro_images(),"Misc")
one_click_badge = os.path.join(misc_imgs,"patrace1.png")
revver_logo = os.path.join(misc_imgs,"revver_logo.png")
ffhome = os.path.join(misc_imgs,"ff_home.png")
revver_logo = os.path.join(misc_imgs,"revver_logo.png")
clearbits_rss = os.path.join(misc_imgs,"clearbits_feedicon.png")
dizizle_logo = os.path.join(misc_imgs,"dizizle.png")
blip_browse = os.path.join(misc_imgs,"blip_browse.png")
blip_recent = os.path.join(misc_imgs,"blip_recent.png")
blip_popular = os.path.join(misc_imgs,"blip_popular.png")
