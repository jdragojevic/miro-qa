#config.py

import os
import time
from sikuli.Sikuli import *


testlitmus = False


def get_img_path():
    """Set up the path to the os specific image directory and for setBundlePath().

    """
    proj_dir = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro")
    img_dir = "Images_"+get_os_name()
    img_path = os.path.join(proj_dir,img_dir)
    return img_path


def miro_images():
    """Set up the path to the generic miro images.


    """
    proj_dir = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro")
    img_path = os.path.join(proj_dir,"Images")
    return img_path

def get_os_name():
    """Returns the os string for the SUT
    """
    if "MAC" in str(Env.getOS()):
        return "osx"
    elif "WINDOWS" in str(Env.getOS()):
        return "win"
    elif "LINUX" in str(Env.getOS()):
        return "lin"
    else:
        print ("I don't know how to handle platform '%s'", Env.getOS())

   
