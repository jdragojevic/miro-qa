#testvars.py
"""Specify the test variables and image locations.

"""

import os
import config

timeout = 30

##Sidebar
side_imgs = os.path.join(config.miro_images(),"Sidebar")
SIDEBAR_ICONS = {"guide_icon": os.path.join(side_imgs,"icon-guide.png"),
                 "guide_icon_active": os.path.join(side_imgs,"icon-guide_active.png"),
                 "search_icon": os.path.join(side_imgs,"icon-search.png"),
                 "video_icon": os.path.join(side_imgs,"icon-video.png"),
                 "music_icon": os.path.join(side_imgs,"icon-music.png"),
                 "other_icon": os.path.join(side_imgs,"icon-other.png"),
                 "conversions_icon": os.path.join(side_imgs,"icon-converting.png"),
                 "downloading_icon": os.path.join(side_imgs,"icon-downloading.png"),
                 "playlist_icon": os.path.join(side_imgs,"icon-playlist.png"),
                 }

##Preferences panel
pref_imgs = os.path.join(config.miro_images(),"Prefs")
PREF_PANEL = {
    "error": os.path.join(pref_imgs,"pref_panel_error.png"),
    "conversions" : os.path.join(pref_imgs,"pref_tab_conversions.png"),
    "diskspace" : os.path.join(pref_imgs,"pref_tab_disk_space.png"),
    "downloads" : os.path.join(pref_imgs,"pref_tab_downloads.png"),
    "extensions" : os.path.join(pref_imgs,"pref_tab_extensions.png"),
    "podcasts" : "pref_tab_feeds.png",
    "folders" : os.path.join(pref_imgs,"pref_tab_folders.png"),
    "general" : os.path.join(pref_imgs,"pref_tab_general.png"),
    "playback" : os.path.join(pref_imgs,"pref_tab_playback.png"),
    "sharing" : os.path.join(pref_imgs,"pref_tab_sharing.png"),
    "stores" : os.path.join(pref_imgs,"pref_tab_stores.png"),      
              }

#MiroGuide

mg = os.path.join(config.miro_images(),"MiroGuide")
guide_add_feed = os.path.join(mg,"add_feed.png")
guide_search = os.path.join(mg,"guide_search.png")
guide_home = os.path.join(mg,"navhome.png")
feedback = os.path.join(mg,"feedback.png")

#Search
search_imgs = os.path.join(config.miro_images(),"Search")
blip_icon = os.path.join(search_imgs,"search_icon_bliptv.png")
youtube_icon = os.path.join(search_imgs,"search_icon_youtube.png")
youtube_user_icon = os.path.join(search_imgs,"search_icon_youtubeuser.png")
all_icon = os.path.join(search_imgs,"search_icon_all.png")


#Items

item_context_button = os.path.join(config.miro_images(),"Items")

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
tv_icon = os.path.join(misc_imgs,"mike_tv.png")


        
