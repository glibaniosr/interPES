#!/usr/bin/python3

from contextlib import contextmanager
import os

# Globals
CWD = os.getcwd()

### Context manager for changing the current working directory ###
@contextmanager
def cd(newdir):
    prevdir = os.getcwd()
    os.chdir(os.path.expanduser(newdir))
    try:
        yield
    finally:
        os.chdir(prevdir)

### Function to extract parameters from params file ###
def getparams(paramsFile):
    with open(paramsFile, 'r') as inp:
        for line in inp:
            data = line.split()
            if not line.startswith("#"):
                if line.startswith("state1_xyz"):
                    state1File = data[2]
                elif line.startswith("state2_xyz"):
                    state2File = data[2]
                elif line.startswith("basename1"):
                    base1File = data[2]
                elif line.startswith("basename2"):
                    base2File = data[2]
                elif line.startswith("dir_name1"):
                    dir1 = data[2]
                elif line.startswith("dir_name2"):
                    dir2 = data[2]
                elif line.startswith("head_file1"):
                    h1File = data[2]
                elif line.startswith("head_file2"):
                    h2File = data[2]
                elif line.startswith("bot_file"):
                    botFile = data[2]
                elif line.startswith("allxyz_file"):
                    allxyzFile = data[2]
                elif line.startswith("nAtoms"):
                    nAtoms = int(data[2])
                elif line.startswith("nPoints"):
                    nPoints = int(data[2])
                elif line.startswith("nProcs"):
                    nProcs = int(data[2])

    params = [state1File, state2File, base1File, base2File, dir1, dir2, 
    h1File, h2File, botFile, allxyzFile, nAtoms, nPoints, nProcs]

    return params

def createinps(data):
    nPoints = data[0]
    baseName = data[1]
    DIR = data[2]
    allInp = []
    n = 1
    if not os.path.exists(DIR):
        os.makedirs(DIR)
    while n <= nPoints:
        number = str(n)
        number = number.rjust(3,'0')
        writeFile = baseName + "." + number + ".inp"
        allInp.append(writeFile)
        with cd(DIR):
            with open(writeFile, 'w') as output:
                title = "# ORCA PES calculation step "+ number+ "\n"
                output.write(title)
        n += 1

    return allInp

### Function to create the inputs and write the headers ### 
def write(dataFile):   
    wFile = str(dataFile[0])
    inpLines = str(dataFile[1])
    DIR = str(dataFile[2])
    # Enter DIR and write to file
    with cd(DIR):
        with open(wFile,'a') as output:
            output.write(inpLines)

    return    

### Extract coordinates from file
def extcoord(inFile):
    allCoord = []
    with open(inFile,'r') as file:
        lines = file.readlines()
        nAtoms = int(lines[0])
        del lines[0]
        del lines[0]
        for line in lines:
            line = line.split()
            allCoord.append([str(line[0]), float(line[1]), float(line[2]), float(line[3])])
    return allCoord