# DICraft

Convert DICOM files into voxel/pixelcloud, edit Minecraft style and 3D-print them.

This project tries to fill the gap between X-ray imaging (slices, single images, ultrasound images) and 3D-printing.  
For medical and scientific use (you will find application cases).

Visit [projekt page](http://bison--.github.io/DICraft/)

# DISCLAIMER

This *"program"* is under **heavy** development and it is NOT guaranteed
that these instructions always fit the actual behavior!


# Installation

Create a venv and install the requirements:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

If you want/have to convert DICOM files with **convert.py** that we can use them,  
you need **dcmj2pnm** what is part of the dcmtk
```bash
    sudo apt-get install dcmtk
```

# USE

At first, we have to convert some **DCM** files into an readable format.  
This will convert **ALL** .dcm files under the given directory into the **tmp** directory.

    python convert.py multiImageTest/ tmp/
    
With this command we create a *"voxel"* file our engine can work with.  
This command will automatically overwrite **"saves/quicksave.sav"** or with the command switch "savefile="  
you can name the destination file.

    python dcm2save.py tmp/ savefile=roflcopter.sav

Finally we can start the main program (if you named your file, you have to tell the program)

    python DICraft.py savefile=roflcopter.sav

From here you can save your work with F5 or export it for 3D printing with F6.

### example

Placed my MRT scans in **tmp/my/** and want to save the result in **tmp/**  

```bash
python convert.py tmp/my/ tmp/
python dcm2save.py tmp/ savefile=bison_brain.sav minVal=10 maxVal=255 materialSwitch=10
python DICraft.py savefile=bison_brain.sav
```


## Configuration

In **dcm2save.py** are 3 special configuration variables:  

    minVal = 130
    maxVal = 134
    materialSwitch = 15

**minVal** and **maxVal** are the raw gray values from the image, every value in between would be displayed later.  
You **HAVE** to play with those values to get an accurate result (later there will be a GUI for that....).  

**materialSwitch** is in which intervals another texture is picked.  
You may have to play with it too.  
The maximum value is 99.

All 3 have command line switches too.

```bash
python dcm2save.py tmp/ savefile=bison_brain.sav minVal=10 maxVal=255 materialSwitch=10
```

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

# LEGACY

old stuff/for reference only

## OLD installation

Debian based:

    sudo apt-get install python-pyglet python-dicom python-qt4

Others "maybe":

    sudo pip install pyglet python-dicom python-qt4

In some distributions **python-dicom** is named **pydicom**  
The conversion parts should work without GUI, so you will need Qt4 **ONLY** when strating the GUI-Tools.  

If you want/have to convert DICOM files with **convert.py** that we can use them,  
you need **dcmj2pnm** what is part of the dcmtk

    sudo apt-get install dcmtk
