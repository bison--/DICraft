#!/usr/bin/python

import sys
import os
from PIL import Image
from PIL import ImageOps
import numpy
import dicom
import pnmHeader
import saveModule
import multiTimer

minVal = 130  #12850
maxVal = 136  #13000 #13366
materialSwitch = 15
maxVoxels = -1

useCutArea = False
cutRectangle = (0, 0, 0, 0)

# max len of material index we can use
materialMatrixL = 99 #len(materialMatrix)

# heightMap
heightMap = False


def fileNameHasNumber(name):
	parts = name.split(".")
	part = parts[0]
	for i in reversed(range(len(part))):
		if part[i].isdigit():
			return True

	return False

def getInt(name):
	#TODO: make a USEFUL sort algorythm!
	#tmp/3DSlice100.dcm.pnm
	#basename = name.partition('.')
	#alpha, num = basename.split('_')
	parts = name.split(".")
	#dirt = parts[0].replace("3DSlice", "")
	part = parts[0]
	finalNumber = ""
	for i in reversed(range(len(part))):
		if part[i].isdigit():
			finalNumber = str(part[i]) + finalNumber
	
	#dirt = name.replace("3DSlice", "").replace(".dcm.pgm", "")
	if finalNumber.isdigit():
		return int(finalNumber)
	else:
		return 0


sm = saveModule.saveModule()
sav = open(sm.getSaveDest(), "w")

sourceFolder = "./tmp"
sourceFolder = "./tmp/Seq_9_EP2D_DIFF_3_5MM"
sourceFiles = []
if len(sys.argv) > 1:
	sourceFolder = sys.argv[1]

for arg in sys.argv:
	if arg.startswith("minVal="):
		minVal = int(arg.replace("minVal=", ""))
	elif arg.startswith("maxVal="):
		maxVal = int(arg.replace("maxVal=", ""))
	elif arg.startswith("materialSwitch="):
		materialSwitch = int(arg.replace("materialSwitch=", ""))
	elif arg.startswith("heightMap="):
		heightMap = bool(int(arg.replace("heightMap=", "")))
	elif arg.startswith("maxVoxels="):
		maxVoxels = int(arg.replace("maxVoxels=", ""))
	elif arg.startswith("cutRectangle="):
		useCutArea = True
		cutRectangleParts = arg.replace("cutRectangle=", "").split(",")
		cutRectangle = (int(cutRectangleParts[0]), int(cutRectangleParts[1]), int(cutRectangleParts[2]), int(cutRectangleParts[3]))

if heightMap:
	sourceFiles.append(sys.argv[1])
else:
	sourceFilesTmp = os.listdir(sourceFolder)
	sourceFilesTmp.sort(key=getInt)

	for i in range(len(sourceFilesTmp)):
		if not sourceFilesTmp[i].lower().endswith(".md") and fileNameHasNumber(sourceFilesTmp[i]):
			sourceFiles.append(os.path.join(sourceFolder, sourceFilesTmp[i]))


class Statistics:
	def __init__(self):
		self.mt = multiTimer.multiTimer()
		self.mt.start("runtime")
		self.minValue = -1
		self.maxValue = 0
		self.totalValues = 0
		self.totalAcceptedValues = 0
	
	def addVal(self, val, isAccepted=False):
		self.totalValues += 1
		if isAccepted:
			self.totalAcceptedValues += 1
		
		if val > self.maxValue:
			self.maxValue = val
		elif val < self.minValue or self.minValue == -1:
			self.minValue = val
			
	def printStats(self):
		self.mt.stop("runtime")
		print("duration:", self.mt.duration("runtime"))
		print("minValue:", self.minValue)
		print("maxValue:", self.maxValue)
		print("accepted values:", self.totalAcceptedValues, "/", self.totalValues)


STATS = Statistics()

def readPng(filename):
	img = Image.open(filename)
	# https://holypython.com/python-pil-tutorial/how-to-convert-an-image-to-black-white-in-python-pil
	img = img.convert("L")
	if useCutArea:
		#img = ImageOps.crop(img, cutRectangle)
		img = img.crop(cutRectangle)

	return {
		"width": img.size[0],
		"height": img.size[1],
		"pixels": list(img.getdata()),
		"pixelCount": img.size[0] * img.size[1]
	}

def getFromPng():
	#http://paulbourke.net/dataformats/ppm/
	rows = []
	finalStr = ""

	countX = 0
	countY = 0
	countZ = 0
	countVoxel = 0
	for z in sourceFiles:
		print(z)

		png = readPng(z)

		width = png["width"]
		height = png["height"]

		countX = 0
		for x in range(width):
			countY = 0
			for y in range(height):#x:
				#print x,y
				#pixVal = pnm["pixels"][x][y]
				#pixVal = y
				index = (countX * width) + y
				if index >= png["pixelCount"]:
					#print countX, index, len(pnm["pixels"])
					print("index out of range")
					break
					
				pixVal = png["pixels"][index]

				if pixVal >= minVal and pixVal <= maxVal:
					STATS.addVal(pixVal, True)
					material = (pixVal - minVal) * materialSwitch
					
					if material > materialMatrixL:
						material = materialMatrixL
					elif material < materialSwitch:
						material = pixVal - minVal

					countVoxel += 1
					
					if heightMap:
						for zI in range((pixVal - minVal)):
							#finalStr += "[{y}, {z}, {x}]:{mat}\n".format(x=x, y=y, z=zI, mat=material)
							rows.append("[{y}, {z}, {x}]:{mat}\n".format(x=x, y=y, z=zI, mat=material))
					else:
						#finalStr += "[{y}, {z}, {x}]:{mat}\n".format(x=x, y=y, z=countZ, mat=material)
						rows.append("[{y}, {z}, {x}]:{mat}\n".format(x=x, y=y, z=countZ, mat=material))
				else:
					STATS.addVal(pixVal, False)
				countY += 1
			countX += 1
		countZ += 1
		print("current voxel:", countVoxel)
		if maxVoxels != -1 and countVoxel >= maxVoxels:
			break
		
	return "".join(rows)
	

sav.write(getFromPng())
sav.close()
STATS.printStats()
