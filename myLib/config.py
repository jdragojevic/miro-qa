#config.py

import os
import time
import subprocess
import pickle
import shutil
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
    dir_list = []
    proj_dir = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro")
    os_image_dir = get_img_path()
    #Add the os-specific image directory to the sikuli search path if it is not in there already   
    if os_image_dir not in list(getImagePath()):
        addImagePath(os_image_dir)
    #Add the sub-dir under Images to the sikuli search path if they are not there already
    app_image_dir = os.path.join(proj_dir,"Images")
    print app_image_dir
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

def start_ff_on_linux():
    subprocess.Popen(r'firefox', cwd='/usr/bin/')

def get_support_dir():
    if get_os_name() == "win":
        ver = Env.getOSVersion()
        wv = ver.split('.')[0]
        if int(wv) < 6:
            support_dir = os.path.join(os.getenv("HOME"),"Application Support","Participatory Culture Foundation","Miro","Support")
        else:
            support_dir = os.path.join(os.getenv("USERPROFILE"),"AppData","Roaming","Participatory Culture Foundation","Miro","Support")
    elif get_os_name() == "lin":
            support_dir = os.path.join(os.getenv("HOME"),".miro")
    elif get_os_name() == "osx":
            support_dir = os.path.join(os.getenv("HOME"),"Library","Application Support","Miro")

    else:
        print "no clue"
    return support_dir

def get_video_dir():
    if get_os_name() == "win":
        ver = Env.getOSVersion()
        wv = ver.split('.')[0]
        if int(wv) < 6:
            video_dir = os.path.join(os.getenv("HOME"),"My Documents","My Videos","Miro")
        else:
            video_dir = os.path.join(os.getenv("USERPROFILE"),"Videos","Miro")
    elif get_os_name() == "lin":
            video_dir = os.path.join(os.getenv("HOME"),"Videos","Miro")
    elif get_os_name() == "osx":
            video_dir = os.path.join(os.getenv("HOME"),"Movies","Miro")

    else:
        print "no clue"
    return video_dir



def delete_database_and_prefs():
        """Delete the miro support dir and preferences.

        On Windows, delete the entire Support dir. On OSX delete Support dir + preferences plist.
        On linux, delete Support dir, + unset gconf settings.
        """
        
        miro_support_dir = get_support_dir()
        if os.path.exists(miro_support_dir):
            shutil.rmtree(miro_support_dir)
        else:
            print "***Warning: didn't find support dir***"
        #completely ditch preferences on linux
        if get_os_name() == "lin":
            unset_cmd = ["gconftool-2", "--recursive-unset", "/apps/miro"]
            p = subprocess.Popen(unset_cmd).communicate()
        #completely ditch preferences on osx
        if get_os_name() == "osx":
            plist_file = os.path.join(os.getenv("HOME"),"Library","Preferences","org.participatoryculture.Miro.plist")
            if os.path.exists(plist_file):
                os.remove(plist_file)



def delete_miro_video_storage_dir():
        """Delete the Miro video storage directory.

        """
    
        #Delete Miro default video storage
        miro_video_dir = get_video_dir()
        if os.path.exists(miro_video_dir):
            shutil.rmtree(miro_video_dir)
        else:
            print "***Warning: didn't find videos dir***"



def get_val_from_mirodb(dbtable,dbfield):
    stmt = 'from db_mod import MiroDatabase; MiroDatabase().get_value("%s","%s")' % (dbtable,dbfield)    
    db_cmd = ['python','-c',stmt]
    p = subprocess.Popen(db_cmd).communicate()
    infile = os.path.join(os.getenv("PCF_TEST_HOME"),"Miro","dbval.pkl")
    pkl_file = open(infile, 'rb')
    dbvalue = pickle.load(pkl_file)
    pkl_file.close()
    if os.path.exists(infile):
        os.remove(infile)
    return dbvalue
    

def set_mirodb_value(dbtable,dbfield,dbval):
    stmt = 'from db_mod import MiroDatabase; MiroDatabase().set_value("%s","%s","%s")' % (dbtable,dbfield,dbval)
    db_cmd = ['python','-c',stmt]
    p = subprocess.Popen(db_cmd).communicate()
   
    
    


    
    
