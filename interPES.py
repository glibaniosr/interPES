#!/usr/bin/python3

# This script takes two .xyz files from two different eletronic states and generate structures
# for a PES calculation in ORCA.

### USAGE --> genPES.py params_file.txt
# OBS: The params_file.txt should be in a directory named params inside current working directory 

# Imports
from contextlib import contextmanager
import re
import glob
import os
import ioMOD
import sys

### Functions ###
# Context manager for changing the current working directory ###
@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

# Generate new coordinate
def newcoord(n,const,pi):
    coord = n*const+pi
    return coord

### External input, get parameters ###
paramsFile = sys.argv[1]
paramsDir = "params"
with cd(paramsDir):
    params = ioMOD.getparams(paramsFile)

### Files and directories ###
state1File  = params[0] 
state2File  = params[1] 
base1File   = params[2]
base2File   = params[3]
dir1        = params[4]
dir2        = params[5]
h1File      = params[6]
h2File      = params[7]
botFile     = params[8]
allxyzFile  = params[9]
#### Global variables ###
nAtoms      = params[10]
nPoints     = params[11]
nProcs      = params[12]

### Internal variables ###
allCoord1   = []
allCoord2   = []
allInp1     = []
allInp2     = []
constx      = []
consty      = []
constz      = []
sp = "     "

# Create .inp files and write the title
allInp1 = ioMOD.createinps([nPoints,base1File,dir1])
allInp2 = ioMOD.createinps([nPoints,base2File,dir2])

# Get the lines from the headers
with cd(paramsDir):
    with open(h1File) as header:
        header1 = header.read()
    with open(h2File) as header:
        header2 = header.read()
# Write the headers on all files
for inpFile in allInp1:
    ioMOD.write([inpFile, header1, dir1])
for inpFile in allInp2:
    ioMOD.write([inpFile, header2, dir2])

# Get all the coordinates
with cd(paramsDir):
    allCoord1 = ioMOD.extcoord(state1File)
    allCoord2 = ioMOD.extcoord(state2File)

# Constants of the distances to interpolate the points for each atom n
n = 0
while n < nAtoms:
    constx.append((allCoord2[n][1]-allCoord1[n][1])/(nPoints-1))
    consty.append((allCoord2[n][2]-allCoord1[n][2])/(nPoints-1))
    constz.append((allCoord2[n][3]-allCoord1[n][3])/(nPoints-1))
    n = n+1

# Get the distance differences for coordinates interpolation
np = 0
while np < nPoints:
    newCoord = []
    if np == 0:
        newCoord = allCoord1
    elif np == nPoints-1:
        newCoord = allCoord2
    # Generate new coordinates for file n outside the two minimuns
    # New coordinates
    else:
        n = 0
        while n < nAtoms:
            coordX = newcoord(np,constx[n],allCoord1[n][1])
            coordY = newcoord(np,consty[n],allCoord1[n][2])
            coordZ = newcoord(np,constz[n],allCoord1[n][3])
            newCoord.append([allCoord1[n][0], coordX, coordY, coordZ])
            n += 1
            # Write the new coordinates in the .inp files
    with cd(dir1): # Files 1
        with open(allInp1[np], 'a') as output:
            output.write('\n')
            for lines in newCoord:
                output.write("{0:3s} {1:14f} {2:14f} {3:14f}".format(lines[0],lines[1],lines[2],lines[3]))
                output.write('\n')
                # Write the bottom of the file
            output.write('*\n') # Later add the option to write contents of the file
    with cd(dir2): # Files 2
        with open(allInp2[np], 'a') as output:
            output.write('\n')
            for lines in newCoord:
                output.write("{0:3s} {1:14f} {2:14f} {3:14f}".format(lines[0],lines[1],lines[2],lines[3]))
                output.write('\n')
                # Write the bottom of the file
            output.write('*\n') # Later add the option to write contents of the file
    np = np + 1

# Create the script to run all inputs
for idx, file in enumerate([base1File, base2File]):
    rodaNAME = "runall-" + file + ".sh"
    allInps = [allInp1, allInp2]
    allDir = [dir1, dir2]
    with cd(allDir[idx]):
        with open(rodaNAME, 'w') as rodaFile:
            for file in allInps[idx]:
                fileName,ext = os.path.splitext(file)
                line = "nohup orca_run -i "+file+" -o " +fileName+".out -p "+str(nProcs)+"\n"
                rodaFile.writelines(line)