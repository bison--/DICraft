# DICraft

Convert DICOM files into voxel/pixelcloud and edit in Minecraft style.


# DISCLAIMER

This *"program"* is under **heavy** development and it is NOT guranteet,  
that these instructions always fit the actual behavior!


# Installation

Debian based:

    sudo apt-get install python-pyglet python-dicom

Others "maybe":

    sudo pip install pyglet python-dicom

In some distributions **python-dicom** is named **pydicom**  

If you want/have to convert DICOM files with **convert.py** that we can use them,  
you need **dcmj2pnm** what is part of the dcmtk

    sudo apt-get install dcmtk


# USE

At first, we have to convert some **DCM** files into an readable format.
This will convert **ALL** .dcm files under the given directory into the **tmp** directory.

    python convert.py multiImageTest/
    
With this command we create a *"voxel"* file our engine can work with.
This command will automatically overwrtite **"saves/quicksave.sav"**, with the command switch "savefile="  
you can name the destination file.

    python dcm2save.py tmp/ savefile=roflcopter.sav

Finally we can start the main program (if you named your file, you have to tell the program)

    python DICraft.py savefile=roflcopter.sav

From here you can save your work with F5 or export it for 3D-Printing with F6

# Controls

Exit: ESC  
Release mouse: F1

Save your work: F5  
Export to OpenScad: F6 

Movement: W A S D, UP(SPACE), DOWN(LEFT CTRL)  
Remove block: left mouse button  
Place block: right mouse button  
Select "material": number 1 to 0

Remove group iof blocks:  
focus a block, press **"DEL"** and all blocks that stick together are removed  
**WARNING**  
There is a recursion bug that can crash the program if there are TO MANY blocks!  
**USE WITH CARE** 



