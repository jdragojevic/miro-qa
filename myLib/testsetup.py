import config
from sikuli.Sikuli import *
import os

timeout = 30

def launch_cmd():
    """Returns the launch path for the application.

    launch is an os specific command
    """
    if config.get_os_name() == "osx":
        return "/Applications/Miro.app"
    elif config.get_os_name() == "win":
        return os.path.join(os.getenv("PROGRAMFILES"),"Participatory Culture Foundation","Miro","Miro.exe")
    elif config.get_os_name() == "lin":
        print "trying to run on linux - make sure MIRONIGHTLYDIR is set"
        return "linux"
    else:
        print config.get_os_name()

def launch_miro():
    """Open the Miro Application, the sets the region coords for searching.
    
    Uses the Miro Guides, Home icon, Bottom Corner, and VolumeBar to find coordinates.
    Returns the:
        
    """
    if launch_cmd() == "linux":
        if not exists("Sidebar",3):
            config.start_miro_on_linux()
    else:
        App.open(launch_cmd())
    time.sleep(10)


def get_regions():
        config.set_image_dirs()
        click(Pattern("sidebar_top.png").similar(0.6))
        topx =  int(getLastMatch().getX())-25
        topy = int(getLastMatch().getY())-80
        try:
            sidebar_width = int(config.get_val_from_mirodb("global_state","tabs_width"))
        except:
            sidebar_width = 250
        sidex = sidebar_width+topx    
        find("BottomCorner.png")
        vbarx =  int(getLastMatch().getX())+30
        vbary = int(getLastMatch().getY())+10
        vbarw = getLastMatch().getW()
        app_height = int(vbary-topy)
        mainwidth = int((vbarx-sidex)+vbarw)
        

        AppRegions = {"SidebarRegion": Region(topx,topy,sidebar_width,app_height),
                      "MainViewRegion": Region(sidex, topy+110, mainwidth, app_height),
                      "TopHalfRegion": Region(0,0,mainwidth+sidebar_width,app_height/2),
                      "TopLeftRegion": Region(0,0,mainwidth/2,app_height/2),
                      "MainTitleBarRegion": Region(sidex, topy, mainwidth, 120),
                      "MainAndHeaderRegion": Region(sidex, topy, mainwidth, app_height+50),
                      }
        for regs in AppRegions.itervalues():
            regs.setAutoWaitTimeout(30)
        AppRegions["SidebarRegion"].highlight(3)
        return AppRegions    
   
    
