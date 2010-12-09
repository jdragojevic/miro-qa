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
    elif config.get_os_name() == "win":
        return "C:\Program Files\Participatory Culture Foundation\Miro\Miro.exe"
    else:
        print config.get_os_name()

def shortcut(key):
    if config.get_os_name() == "osx":
        type(key,KEY_CMD)
    elif config.get_os_name() == "win":
        type(key,KEY_CTRL)
    else:
        print config.get_os_name()
        type(key,KEY_CTRL)

    

def quit_miro(self):
    shortcut("q")
    while exists("dialog_confirm_quit.png",10):
        click("dialog_quit.png")
    #giving it 15 seconds to shut down
    self.assertFalse(exists("tab_search.png",15))
    
    
def cmd_ctrl():
    if config.get_os_name() == "osx":
        return "CMD"
    elif config.get_os_name() == "win":
        return "CTRL"
    else:
        print config.get_os_name()
        return "CTRL"


def open_ff():
    """Returns the launch path for the application.

    launch is an os specific command
    """
    if config.get_os_name() == "osx":
        return "/Applications/Firefox.app"
    elif config.get_os_name() == "win":
        return "C:\Program Files\Mozilla Firefox\Firefox.exe"
    else:
        print "no clue"



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
    click_sidebar_tab(self,"other")
    if exists(feed,5):
        click(feed)
        type(Key.DELETE)
        remove_confirm(self,"remove")
        self.assertFalse(exists(feed),5)
    else:
        print "feed: " +feed+ " not present"


def click_sidebar_tab(self,tab):
    """Click any default tab in the sidebar.

    assumes the tab image file is an os-speicific image, and then verifies
    the tab is selected by verifying the miro large icon in the main view

    """
    tab_icon = os.path.join(testvars.side_imgs,"icon-"+tab+"_large.png")
    self.assertTrue(exists("tab_"+tab+".png"))
    click(getLastMatch())
    self.assertTrue(exists(tab_icon))


## Menu related stuff ##

def click_menu(self,menu):
    """Confirms that the specified menu is present, then clicks on it.

    Here are the valid menu images names that exist in the Images_[os] directory
    
    Miro Menu (os x): 'menu_miro'
        'menu_about_miro', 'menu_donate', 'menu_check_version', 'menu_preferences', 'menu_quit'
    File (all os): 'menu_file' = menu_file.png
        menu_open.png, menu_download.png, menu_remove_item.png, menu_edit_item.png,
        menu_save_as.png, menu_copy_item_url.png
    Sidebar (osx, win, linux): menu_sidebar.png
        menu_add_feed.png, menu_add_website.png, menu_new_search_feed.png, menu_new_folder.png,
        menu_rename.png, menu_remove.png, menu_update_feed.png, menu_update_all_feeds.png,
        menu_import_feeds.png, menu_export_feeds.png, menu_share.png, menu_copy_url.png
    Playlists (osx, win, linux): menu_playlists.png
        menu_new_playlist.png, menu_new_playlist_folder.png, menu_rename_playlist.png,
        menu_remove_playlist.png
     ...
     To be continued
    """
    self.assertTrue(exists(menu))
    click(getLastMatch())

def open_preferences(self,lang='en'):
    """OS specific handling for Preferences menu, since it differs on osx and windows.

    """
        
    if config.get_os_name() == "osx":
        click_menu(self,"menu_miro.png")
    elif config.get_os_name() == "win":
        click_menu(self,"menu_file.png")
    else:
        print config.get_os_name()
    self.assertTrue(exists("menu_preferences.png"))
    if lang == 'en':
        click_menu(self,"menu_preferences.png")
    else:
        click_menu(self,lang+"_menu_preferences.png")
    self.assertTrue(exists(testvars.pref_general))
    
    
                    

    

    
