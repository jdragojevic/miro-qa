import os
import time
import glob
import config
import testvars
from sikuli.Sikuli import *


#setBundlePath(config.get_img_path())

class MiroRegions(object):
    """Base call for setup of Miro App testing. Tabs and dialogs inherit from MiroApp.

    """
    def __init__(self):
        '''
        Constructor
        '''
        import testsetup
        setAutoWaitTimeout(testvars.timeout)
        testsetup.launch_miro()
        reg = testsetup.get_regions()
        config.set_image_dirs()
        self.s = reg["SidebarRegion"]
        self.m = reg["MainViewRegion"]
        self.t = reg["TopHalfRegion"]
        self.tl = reg["TopLeftRegion"]
        self.mtb = reg["MainTitleBarRegion"]
        self.mr = reg["MainAndHeaderRegion"]
        

        myscreen = Screen()
        sr = Region(myscreen.getBounds())
        self.screen_height = sr.getH()
        self.screen_width = sr.getW()
#        Settings.ActionLogs = False
        Settings.InfoLogs = False
        Settings.DebugLogs = False

