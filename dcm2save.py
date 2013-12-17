#!/usr/bin/python


import sys, os
#print 'Hello World'
#[-8, -3, 21]=>STONE


	
sav = open("savegame.sav", "w")
dcmFilePath = "./multiImageTest"
dcmFiles = []
if len(sys.argv) > 1:
	dcmFilePath = sys.argv[1]
	dcmFilesTmp = os.listdir(dcmFilePath)
	dcmFilesTmp.sort()
	#dcmFiles = sorted(dcmFiles, key=lambda x: int(x.split('.')[3]))

	for i in range(len(dcmFilesTmp)):
		if dcmFilesTmp[i].lower().endswith(".dcm"):
			dcmFiles.append(os.path.join(dcmFilePath, dcmFilesTmp[i]))
else:
	dcmFiles.append(os.path.join(dcmFilePath, "CT_small.dcm"))

#finalStr = ""
#for x in xrange(10):
#	for y in xrange(100):
#		finalStr += "[{x}, {z}, {y}]=>SAND\n".format(x=x, y=y, z=-2)


minVal = 400
maxVal = 1500
materialSwitch = 250

import dicom


materialMatrix = ["GRASS", "SAND", "BRICK", "STONE"]
materialMatrixL = len(materialMatrix)

def getUncompressed():
	finalStr = ""

	countX = 0
	countY = 0
	countZ = 0
	for z in dcmFiles:
		print z
		ds = dicom.read_file(z)

		countX = 0
		for x in ds.pixel_array:

			countY = 0
			for y in x:
				if y >= minVal and y <= maxVal:
					material = "GRASS"
					for i in xrange(materialMatrixL):
						if y > minVal + materialSwitch * i:
							material = materialMatrix[i]

					finalStr += "[{y}, {z}, {x}]=>{mat}\n".format(x=countX, y=countY, z=countZ-2, mat=material)
					#finalStr += str(y) + ","
				countY += 1
			countX += 1
		countZ += 1
		#finalStr += "\n"
	return finalStr

def getCompressed():
	finalStr = ""

	countX = 0
	countY = 0
	countZ = 0
	for z in dcmFiles:
		print z
		ds = dicom.read_file(z)
		pixel_bytes = ds.PixelData
		#print pixel_bytes
		#print ds.items()[0]
		print ds.__dict__
		return pixel_bytes
		countX = 0
		for x in ds.pixel_array:

			countY = 0
			for y in x:
				if y >= minVal and y <= maxVal:
					material = "GRASS"
					for i in xrange(materialMatrixL):
						if y > minVal + materialSwitch * i:
							material = materialMatrix[i]

					finalStr += "[{y}, {z}, {x}]=>{mat}\n".format(x=countX, y=countY, z=countZ-2, mat=material)
					#finalStr += str(y) + ","
				countY += 1
			countX += 1
		countZ += 1
		#finalStr += "\n"
	return finalStr

#fh = open('testImg', "w")
#fh.write(getCompressed())
#fh.close()
#exit()
#print finalStr
sav.write(getUncompressed())
sav.close()
