#config.py

import os
import time
import subprocess
from sikuli.Sikuli import *



testlitmus = True


def get_img_path():
    """Set up the path to the os specific image directory and for setBundlePath().

    """
    proj_dir = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro")
    img_dir = "Images_"+get_os_name()
    img_path = os.path.join(proj_dir,img_dir)
    return img_path

def set_image_dirs():
    """Set the Sikuli image path for the os specific image directory and the main Image dir.

    """
    os_specific_images = "Images_"+get_os_name()
    app_images = "Images"
    dir_list = []
    proj_dir = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro")

    os_image_dir = os.path.join(proj_dir,os_specific_images)
    app_image_dir = os.path.join(proj_dir,app_images)
    
    #Add the os-specific image directory to the sikuli search path if it is not in there already   
    if os_image_dir not in list(getImagePath()):
        addImagePath(os_image_dir)
    #Add the sub-dir under Images to the sikuli search path if they are not there already
    for x in os.listdir(app_image_dir):
        dirx = os.path.join(app_image_dir,x)
        if dirx not in list(getImagePath()):
            addImagePath(dirx)    
    

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

   
def start_miro_on_linux():
    mydir = os.getenv("MIRONIGHTLYDIR")
    subprocess.Popen(r'./run.sh', cwd=mydir)

    
    
    
