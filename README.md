# DICraft

Convert DICOM files into voxel/pixelcloud and edit in Minecraft style.


# DISCLAIMER

This *"program"* is under **heavy** development and it is NOT guranteet,  
that these instructions always fit the actual behavior!


# Installation

Debian based:

    sudo apt-get install python-pyglet python-dicom python-qt4

Others "maybe":

    sudo pip install pyglet python-dicom python-qt4

In some distributions **python-dicom** is named **pydicom**  
The conversion parts should work without GUI, so you will need QT4 **ONLY** when strating the GUI-Tools.  

If you want/have to convert DICOM files with **convert.py** that we can use them,  
you need **dcmj2pnm** what is part of the dcmtk

    sudo apt-get install dcmtk


# USE

At first, we have to convert some **DCM** files into an readable format.  
This will convert **ALL** .dcm files under the given directory into the **tmp** directory.

    python convert.py multiImageTest/ tmp/
    
With this command we create a *"voxel"* file our engine can work with.  
This command will automatically overwrtite **"saves/quicksave.sav"** or with the command switch "savefile="  
you can name the destination file.

    python dcm2save.py tmp/ savefile=roflcopter.sav

Finally we can start the main program (if you named your file, you have to tell the program)

    python DICraft.py savefile=roflcopter.sav

From here you can save your work with F5 or export it for 3D-Printing with F6

## Configuration

In **dcm2save.py** are 3 special configuraton variables:  

    minVal = 130
    maxVal = 134
    materialSwitch = 15

**minVal** and **maxVal** are the raw gray values from the image, every value in between would be displayed later.  
You **HAVE** to play with those values to get an accurate result (later there will be a GUI for that....).  

**materialSwitch** is in which intervals another Texture is picked.  
You may have to play with it too.  
The maximum value is 99.

# Controls

Exit: ESC  
Release mouse: F1

Save your work: F5  
Export to OpenScad: F6

Movement: W A S D, UP(SPACE), DOWN(LEFT CTRL)  
Remove block: left mouse button  
Place block: right mouse button  
Select "material": number 1 to 0  
Reset position (in case of getting "lost"): R

Remove group of blocks:  
focus a block, press **"DEL"** and all blocks that stick together are removed  
**WARNING**  
This may take "forever", be careful!
**USE WITH CARE** 



