#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on 02.04.2020 19:21 CET

@author: zocker_160
"""

import os
import sys
from io import BytesIO

from lib import main as slicer
from lib.SST.src.lib.SST import SST
from lib.SST.src.lib.TGA import TGA

version = "0.4"
magic_number_compressed = b'PK01' # this is the magic number for all compressed files
tga_output = False
confirm = True

print("### SST Slicer for Empire Earth made by zocker_160")
print("### version %s" % version)
print("###")
print("### if you have any issue, pls feel free to report it:")
print("### https://github.com/EE-modders/SST-image_slicer/issues")
print("###")
print("###----------------------------------------------\n")

def show_help():    
    print("""USAGE: SSTslicer [options] <inputfile1> <inputfile2> ... <inputfileN>
important: if you want to convert multiple TGAs you can also just drag and drop them all at once onto the executable
possible options:
-h, --help, -v  show this help / version information
--tga           save all splits as tga as well
""")
    if confirm: input("press Enter to close........")
    sys.exit()

def show_exit():
    input("\npress Enter to close.......\n")
    sys.exit()

if len(sys.argv) <= 1:
    show_help()

parameter_list = list()

for i, arg in enumerate(sys.argv):
    if arg == "-h" or arg == "--help" or arg == "-v":
        confirm = False
        show_help()
    if arg == "--tga":
        tga_output = True
        parameter_list.append(i)

# remove commandline parameters
parameter_list.sort(reverse=True)
for param in parameter_list:
    sys.argv.pop(param)

try:
    filename = sys.argv[1]
except IndexError:
    print("ERROR: no file(s) specified!")
    show_exit()

try:
    with open(filename, 'rb') as infile:
        print("analysing %s......" % filename)
        if infile.read(4) == magic_number_compressed:
            print("\nyou need to decompress the file first!\n")
            show_exit()
except EnvironmentError:
    print("ERROR: File \"%s\" not found!" % filename)
    show_exit()



if filename.split('.')[-1] == "sst":
    num_infiles = len(sys.argv[1:])    

    if num_infiles == 1:
        print("got single SST file as input - splitting....")
        xTiles = int(input("input number of tiles on x-axis: "))
        yTiles = int(input("input number of tiles on y-axis: "))

        SST = SST()
        SST.read_from_file(filename)

        if (SST.header["tiles"] > 1 or SST.header["resolutions"] > 1):
            raise TypeError("This SST file has more than one tile and/or resolution!")

        slicer.slice(BytesIO(SST.TGAbody), filename.split('.')[-2], col=xTiles, row=yTiles, save=True)
    else:
        filenames = sys.argv[1:]
        newfilename = filenames[0].split('.')[-2].split('_')[-3] + "-joined.tga"

        print("\ngot %d SST files as input:  (watch out for the right order!!)\n" % num_infiles)

        for i in range(num_infiles):
            print("%d: %s" % (i+1, filenames[i]))
        print()
        response = input("is that correct? (y/n) ")
        if response != "y": show_exit()

        files = list()

        for file in filenames:
            tmpSST = SST()
            tmpSST.read_from_file(file)

            files.append( (file, BytesIO(tmpSST.TGAbody)) )
        
        image = slicer.join(slicer.get_tiles(files))
        image.save(newfilename)

        print("written output to file:\n%s" % newfilename)
        print("done!")
        show_exit()

elif filename.split('.')[-1] == "tga":
    num_infiles = len(sys.argv[1:])
    prefix = filename.split('.')[-2]

    if num_infiles == 1:
        print("got one TGA file as input - splitting....")
        xTiles = int(input("input number of tiles on x-axis: "))
        yTiles = int(input("input number of tiles on y-axis: "))

        tiles = slicer.slice(filename, prefix, col=xTiles, row=yTiles, save=tga_output)
        SSTtiles = list()

        for part in tiles:
            x, y = part.image.size
            newfilename = part.generate_filename(prefix=prefix, format='sst', path=False)
            
            tmpSST = SST(1, 1, x_res=x, y_res=y, TGAbody=part.get_bytes())
            print(newfilename)
            tmpSST.write_to_file(newfilename, add_extention=False)        
        
        print("done!")
        show_exit()
    else:
        print("INFO: function to join multiple TGAs is not implemented")
        show_exit()
else:
    print("ERROR: unsupported file extention: %s")
    print("only SST and TGA files are supported.")
    show_exit()