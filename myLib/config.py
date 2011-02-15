#config.py

import os
import time
from sikuli.Sikuli import *


testlitmus = False


def get_img_path():
    """Set up the path to the os specific image directory and for setBundlePath().

    """
    img_path = os.path.join(os.getenv("SIKULI_TEST_HOME"),"Images_"+get_os_name())
    return img_path


def miro_images():
    """Set up the path to the generic miro images.


    """
    img_path = os.path.join(os.getenv("SIKULI_TEST_HOME"),"Images")
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

   
