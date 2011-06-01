# set the default sidebar font for windows to Segoe UI 13.
import sys
import fileinput
import shutil

def set_fonts():
    searchExp = "tahoma 11"
    replaceExp = "Segoe UI 12"
    infile = "C:\Program Files\Participatory Culture Foundation\Miro\etc\gtk-2.0\gtkrc"
    tmpfile = "C:\Program Files\Participatory Culture Foundation\Miro\etc\gtk-2.0\gtkrc.mod"
    fin = open(infile)
    fout = open(tmpfile,"wt")
    fback = "C:\Program Files\Participatory Culture Foundation\Miro\etc\gtk-2.0\gtkrc.bak"
    for line in fin:
        fout.write( line.replace(searchExp, replaceExp) )
    fin.close()
    fout.close()
    shutil.move(infile,fback)
    shutil.move(tmpfile,infile)

set_fonts()
