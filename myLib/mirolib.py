#mirolib.py

import os
import time
import glob
import config
import testvars
from sikuli.Sikuli import *

setBundlePath(config.get_img_path())



def open_miro():
    """Returns the launch path for the application.

    launch is an os specific command
    """
    if config.get_os_name() == "osx":
        return "/Applications/Miro.app"
    else:
        print "no clue"

def open_ff():
    """Returns the launch path for the application.

    launch is an os specific command
    """
    if config.get_os_name() == "osx":
        return "/Applications/Firefox.app"
    else:
        print "no clue"


def click_tab(self, tab_image):
    """Looks for the specified tab by image base name.
    Should be able to find the image if it is selected or not selected.
    """
    if exists (imagemap.Tabs[tab_image +"_selected"]):
        print "on the tab " +tab_image
    else:
        click (imagemap.Tabs[(tab_image)])

def toggle_radio(self,button):
    
    """Looks for the specified tab by image base name.
    Should be able to find the image if it is selected or not selected.
    """
    if not exists (imagemap.Buttons[button +"_selected"]):
        click (imagemap.Buttons[(button)])   
 


def cclick(self,img,ddir=getBundlePath()):
    """Look through the image dir and click any image that matches the given name.

    """                                    
    for image in glob.glob(os.path.join(ddir, img+'*.png')):
        print image
        if exists(image,3):
            click(image)
            break

def close_one_click_confirm(self):
    """Close any os confirm dialogs when opening 1-click subscribe feeds."


    """
    if exists("sys_open_alert.png",10):
        click("sys_ok_button.png")

def remove_confirm(self,action):
    """If the remove feed dialog is displayed, remove or cancel.

    action = (remove or cancel)
    """
    time.sleep(5)
    if exists("remove_button_pulse.png",5):
        print "confirm dialog"
        if action == "remove":
            print "clicking remove button"
            click("remove_button_pulse.png")
        else:
            click("cancel_button.png")
        print "verifying dialog closed"
        self.assertFalse(exists("are_you_sure_dialog.png"),4)

def delete_feed(self,feed):
    click(testvars.other_tab)
    if exists(feed,5):
        click(feed)
        type(Key.DELETE)
        remove_confirm(self,"remove")
        self.assertFalse(exists(feed),5)
    else:
        print "feed: " +feed+ " not present"

    
