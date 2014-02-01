#!/usr/bin/python

import sys, os
import numpy
import dicom
import pnmHeader
import saveModule
import multiTimer


minVal = 132 #12850
maxVal = 136  #13000 #13366
materialSwitch = 15

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
sourceFiles = []
if len(sys.argv) > 1:
	sourceFolder = sys.argv[1]


if heightMap:
	sourceFiles.append(sys.argv[1])
else:
	sourceFilesTmp = os.listdir(sourceFolder)
	sourceFilesTmp.sort(key=getInt)
	#sourceFiles = sorted(sourceFiles, key=lambda x: int(x.split('.')[3]))

	for i in range(len(sourceFilesTmp)):
		if not sourceFilesTmp[i].lower().endswith(".md") and fileNameHasNumber(sourceFilesTmp[i]):
			sourceFiles.append(os.path.join(sourceFolder, sourceFilesTmp[i]))


#tiffiles.sort(key=getint)
#finalStr = ""
#for x in xrange(10):
#	for y in xrange(100):
#		finalStr += "[{x}, {z}, {y}]=>SAND\n".format(x=x, y=y, z=-2)


class statistics(object):
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
		print "duration:", self.mt.duration("runtime")
		print "minValue:", self.minValue
		print "maxValue:", self.maxValue
		print "accepted values:", self.totalAcceptedValues, "/", self.totalValues

STATS = statistics()

def getUncompressed():
	finalStr = ""

	countX = 0
	countY = 0
	countZ = 0
	for z in sourceFiles:
		print z
		ds = dicom.read_file(z)

		countX = 0
		for x in ds.pixel_array:

			countY = 0
			for y in x:
				if y >= minVal and y <= maxVal:
					material = 0
					for i in xrange(materialMatrixL):
						if y > minVal + materialSwitch * i:
							material = i

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
	for z in sourceFiles:
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
	for z in sourceFiles:
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
	for z in sourceFiles:
		z = 'tmp/3DSlice57.dcm.pgm'
		if countVoxel >= 100000:
			break
		print z
		#z = sourceFiles[1]
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
	endian = '>'
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
	for z in sourceFiles:
		#if countVoxel >= 200000:
		#	break
		print z
		#z = sourceFiles[1]
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
					#print countX, index, len(pnm["pixels"])
					break
					
				pixVal = pnm["pixels"][index]
				#print pixVal
				if pixVal >= minVal and pixVal <= maxVal:
					STATS.addVal(pixVal, True)
					material = (pixVal - minVal) * materialSwitch
					
					if material > materialMatrixL:
						#print "over value:", pixVal, "/", material
						material = materialMatrixL
					elif material < materialSwitch:
						material = pixVal - minVal
					#for i in xrange(materialMatrixL):
					#	if pixVal >= minVal + materialSwitch * i:
					#		material = i
					
					countVoxel += 1
					
					if heightMap:
						for zI in range((pixVal - minVal)):
							finalStr += "[{y}, {z}, {x}]:{mat}\n".format(x=x, y=y, z=zI, mat=material)
					else:
						finalStr += "[{y}, {z}, {x}]:{mat}\n".format(x=x, y=y, z=countZ, mat=material)

					#print "added:", x,y,z,':', pixVal
				else:
					STATS.addVal(pixVal, False)
					#print "lost:", x,y,z,':', pixVal
					#finalStr += str(y) + ","
				countY += 1
			countX += 1
		countZ += 1
		print "current voxel:", countVoxel
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
STATS.printStats()
