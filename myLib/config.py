#config.py

import os
import time
from sikuli.Sikuli import *


testlitmus = False


def get_img_path():
    """Set up the path to the os specific image directory and for setBundlePath().

    """
    mycwd = os.path.join(os.getcwd(),"Miro")
    img_path = os.path.join(mycwd,"Images_"+get_os_name())
    return img_path


def miro_images():
    """Set up the path to the generic miro images.


    """
    mycwd = os.path.join(os.getcwd(),"Miro")
    img_path = os.path.join(mycwd,"Images")
    return img_path

def get_os_name():
    """Returns the os string for the SUT
    """
    if "MAC" in str(Env.getOS()):
        return "osx"
    else:
        print ("I don't know how to handle platform '%s'", Env.getOS())

   
