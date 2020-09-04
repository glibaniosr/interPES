# interPES
 Interpolate xyz coordinates from two structures to create a PES (ORCA support)

interPES is a script that take two different .xyz files and linearly interpolate the coordinates
from these files to create **n** interpolated structures usually used in Potential Energy Surface (PES)
calculations.

## Usage

To use interPES you need a directory named "params" in your current work folder containing a parameter
file as the example.

To run the script:

> python3 interPES.py params.txt

## Results

The script will create two different folders state1 and state2 with separate inputs for each generated coordinates based on two different electronic states (as example). If you do not need two different kind of input just create two different files with same contents (same headers). In the future I will give an option to have this or not.

Also in the current working directory it will be created a .xyz files with all the structures generated. The structures are separated by a ">", and therefore can also be used in ORCA as a single input with multiple .xyz structures.