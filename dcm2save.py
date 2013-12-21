#!/usr/bin/python


import sys, os
import numpy
import pnmHeader
#[-8, -3, 21]=>STONE


def getint(name):
	#tmp/3DSlice100.dcm.pnm
	#basename = name.partition('.')
	#alpha, num = basename.split('_')
	dirt = name.replace("3DSlice", "").replace(".dcm.pnm", "")
	if dirt.isdigit():
		return int(dirt)
	else:
		return 0
	
sav = open("savegame.sav", "w")
dcmFilePath = "./multiImageTest"
dcmFiles = []
if len(sys.argv) > 1:
	dcmFilePath = sys.argv[1]
	dcmFilesTmp = os.listdir(dcmFilePath)
	dcmFilesTmp.sort(key=getint)
	#dcmFiles = sorted(dcmFiles, key=lambda x: int(x.split('.')[3]))

	for i in range(len(dcmFilesTmp)):
		if not dcmFilesTmp[i].lower().endswith(".md"):
			dcmFiles.append(os.path.join(dcmFilePath, dcmFilesTmp[i]))
else:
	dcmFiles.append(os.path.join(dcmFilePath, "CT_small.dcm"))


#tiffiles.sort(key=getint)
#finalStr = ""
#for x in xrange(10):
#	for y in xrange(100):
#		finalStr += "[{x}, {z}, {y}]=>SAND\n".format(x=x, y=y, z=-2)


minVal = 8 #12850
maxVal = 30 #13000 #13366
materialSwitch = 1

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

					finalStr += "[{y}, {z}, {x}]=>{mat}\n".format(x=countX, y=countY, z=countZ, mat=material)
					#finalStr += str(y) + ","
				countY += 1
			countX += 1
		countZ += 1
		#finalStr += "\n"
	return finalStr

def makelong(s): 
	n = 0 
	for c in s: 
		n *= 256 
		n += ord(c) 
	return n 

def makelongByTup(tup): 
	n = 0 
	for b in tup: 
		n *= 256 
		n += b 
	return n 

def getFromImage():
	#http://stackoverflow.com/questions/138250/read-the-rgb-value-of-a-given-pixel-in-python-programatically
	from PIL import Image
	
	finalStr = ""

	countX = 0
	countY = 0
	countZ = 0
	for z in dcmFiles:
		print z
		im = Image.open(z) #Can be many different formats.
		pix = im.load()
		print im.size #Get the width and hight of the image for iterating over
		width, height = im.size

		#print pix[x,y] #Get the RGBA Value of the a pixel of an image
		#pix[x,y] = value # Set the RGBA Value of the image (tuple)
		countX = 0
		for x in xrange(width):
			countY = 0
			for y in xrange(height):
				#http://docs.python.org/dev/library/stdtypes.html#int.from_bytes
				#argb = int.from_bytes(pix[x, y], byteorder='little', signed=False) # only python 3
				#d = int(s.encode('hex'), 16)
				print dir(pix)
				print pix[x, y]  # always 0, wtf?
				argb = makelongByTup(pix[x, y])
				print argb
				exit()
				if argb >= minVal and argb <= maxVal:
					material = "GRASS"
					for i in xrange(materialMatrixL):
						if argb > minVal + materialSwitch * i:
							material = materialMatrix[i]

					finalStr += "[{y}, {z}, {x}]=>{mat}\n".format(x=x, y=y, z=countZ, mat=material)
					#finalStr += str(y) + ","
				countY += 1
			countX += 1
		countZ += 1
		if countZ > 10:
			break
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



def readPgm( filename, endian='>' ):
	fd = open(filename,'rb')
	fileFormat, width, height, samples, maxval = pnmHeader.read_pnm_header( fd )
	pixels = numpy.fromfile( fd, dtype='u1' if maxval < 256 else endian+'u2' )
	#print fileFormat, width, height, samples, maxval, len(pixels), pixels
	
	#print dir(pixels)
	
	return {"fileFormat":fileFormat, "width":width, "height":height, "samples":samples, "maxval":maxval,
		"pixels":pixels.tolist()}
		#"pixels":pixels.reshape(height, width, samples)}  #TODO: learn NUMPY!
	
def getFromPgm():
	#http://paulbourke.net/dataformats/ppm/
	finalStr = ""

	countX = 0
	countY = 0
	countZ = 0
	countVoxel = 0
	for z in dcmFiles:
		z = 'tmp/3DSlice57.dcm.pgm'
		if countVoxel >= 100000:
			break
		print z
		#z = dcmFiles[1]
		pnm = readPnm(z)
		width = pnm["width"]
		height = pnm["height"]

		countX = 0
		for x in xrange(width):#pnm["pixels"]:
			countY = 0
			for y in xrange(height):#x:
				#print x,y
				#pixVal = pnm["pixels"][x][y]
				#pixVal = y
				index = (countX * width) + y
				if index >= len(pnm["pixels"]):
					print index, len(pnm["pixels"])
					break
					
				pixVal = pnm["pixels"][index]
				#print pixVal
				if pixVal >= minVal and pixVal <= maxVal:
					material = "GRASS"
					for i in xrange(materialMatrixL):
						if pixVal > minVal + materialSwitch * i:
							material = materialMatrix[i]
					
					countVoxel += 1
					finalStr += "[{y}, {z}, {x}]=>{mat}\n".format(x=x, y=y, z=countZ, mat=material)
				else:
					pass
					#print "lost:", x,y,z,':', pixVal
					#finalStr += str(y) + ","
				countY += 1
			countX += 1
		countZ += 1
		#if countZ > 10:
		#	break
		#finalStr += "\n"
		break
	return finalStr

def readPnm( filename ):
	fd = open(filename,'rb')
	fileFormat, width, height, samples, maxval = pnmHeader.read_pnm_header( fd )
	pixels = numpy.fromfile( fd, dtype='u1' if maxval < 256 else endian+'u2' )
	#print fileFormat, width, height, samples, maxval, len(pixels), pixels
	
	#print dir(pixels)
	
	return {"fileFormat":fileFormat, "width":width, "height":height, "samples":samples, "maxval":maxval,
		"pixels":pixels.tolist()}
		#"pixels":pixels.reshape(height, width, samples)}  #TODO: learn NUMPY!
	

def getFromPnm():
	#http://paulbourke.net/dataformats/ppm/
	finalStr = ""

	countX = 0
	countY = 0
	countZ = 0
	countVoxel = 0
	for z in dcmFiles:
		#if countVoxel >= 200000:
		#	break
		print z
		#z = dcmFiles[1]
		pnm = readPnm(z)
		width = pnm["width"]
		height = pnm["height"]

		countX = 0
		for x in xrange(width):#pnm["pixels"]:
			countY = 0
			for y in xrange(height):#x:
				#print x,y
				#pixVal = pnm["pixels"][x][y]
				#pixVal = y
				index = (countX * width) + y
				if index >= len(pnm["pixels"]):
					print countX, index, len(pnm["pixels"])
					break
					
				pixVal = pnm["pixels"][index]
				#print pixVal
				if pixVal >= minVal and pixVal <= maxVal:
					material = "GRASS"
					for i in xrange(materialMatrixL):
						if pixVal > minVal + materialSwitch * i:
							material = materialMatrix[i]
					
					countVoxel += 1
					finalStr += "[{y}, {z}, {x}]=>{mat}\n".format(x=x, y=y, z=countZ, mat=material)
					#print "added:", x,y,z,':', pixVal
				else:
					pass
					#print "lost:", x,y,z,':', pixVal
					#finalStr += str(y) + ","
				countY += 1
			countX += 1
		countZ += 1
		#if countZ > 10:
		#	break
		#finalStr += "\n"
		
	return finalStr
	
#fh = open('testImg', "w")
#fh.write(getCompressed())
#fh.close()
#exit()
#print finalStr
sav.write(getFromPnm())
sav.close()
