# set the default sidebar font for windows to Segoe UI 12.
import sys
import os

import shutil


infile = os.path.join(os.getenv("PROGRAMFILES"),"Participatory Culture Foundation","Miro", "etc", "gtk-2.0", "gtkrc")
fontfile = os.path.join(os.getcwd(),"gtkrc_with_font")
shutil.copy(fontfile, infile)
