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
other_tab = os.path.join(side_imgs,"icon-other.png")
##miro_guide_tab = miro_guide_tab.png"
##        "miro_guide_tab_selected":"miro_guide_tab_selected.png" , \
##        "new_video_folder":"new_video_folder.png" ,\
##        "new_video_folder_selected":"new_video_folder_selected.png" ,\
##         }
##
##Sites = {"miro_guide_search":"miro_guide_search.png" ,\
##         "miro_guide_home":"mg_home.png", \
##        }


#Misc

misc_imgs = os.path.join(config.miro_images(),"Misc")
one_click_badge = os.path.join(misc_imgs,"patrace1.png")
