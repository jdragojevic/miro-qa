# All actions on the preferences panel
import miro_app
from sikuli.Sikuli import *


class SidebarTab(MiroApp):
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
    


    def click_sidebar_tab(self,reg,tab):
        """Click any default tab in the sidebar.

        assumes the tab image file is an os-speicific image, and then verifies
        the tab is selected by verifying the miro large icon in the main view

        """
        similar_tabs = ["Music","Misc","Miro","Videos"]
                         #including Videos so it's not mixed with the video search
        if reg.s.exists("Search",0):
            print "found Search"
            reg.s.click("Search")
            active_tab = "search"
        elif reg.s.exists("Connect"):     
            print "found connect"
            reg.s.click("Connect")
            active_tab = "connect"
        time.sleep(2)
        tab = tab.capitalize()
        if tab.capitalize() in similar_tabs:
            print "going to tab: ",tab
            boty = reg.s.getLastMatch().getY()
            myr = Region(reg.s)
            myr.setH(boty - reg.s.getY()) #height is top of sidebar to y position of video search
            if tab == "Misc": #drop the height to avoid Miro tab
                myr.find("Videos")
                mry1 = Region(myr.getLastMatch().below(250))
                mry1.click("Misc")
            elif tab == "Miro":
                myr.find("Music")
                mry1 = Region(myr.getLastMatch().above(100))
                mry1.click("Miro")
            else:
                myr.click(tab)
                    
        elif tab.lower() == "search" and active_tab == "search":
            print "should be on search already"
        else:
            reg.s.click(tab)
