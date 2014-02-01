import engine as main  # we need the blocktypes from the main program
import json
import os
import sys
from time import gmtime, strftime
import stlWriter
import blockWork

		
class saveModule(object):
	def __init__(self):		
		self.saveFile = 'quicksave.sav'
		self.saveFolder = "saves"
		if len(sys.argv) > 1:
			for arg in sys.argv:
				if arg.startswith("savefile="):
					self.saveFile = arg.replace("savefile=", "")
				elif arg.startswith("sf="):
					self.saveFile = arg.replace("sf=", "")
		
		self.printStuff("working with file: " + self.getSaveDest())
				
		# console output after X lines
		self.maxLineCounter = 10000
		
		# max voxels to load
		self.maxVoxels = 10000000
		
	def printStuff(self, txt):
		print(strftime("%d-%m-%Y %H:%M:%S|", gmtime()) + str(txt) ) 
	
	def getSaveDest(self):
		return os.path.join(self.saveFolder, self.saveFile)
	
	def hasSaveFile(self):
		if os.path.exists(self.getSaveDest()):
			return True
		else:
			return False
	
	def loadWorld(self, model):
		self.printStuff('start loading...') 
		fh = open(self.getSaveDest(), 'r')
		worldMod = fh.read()
		fh.close()
		
		worldMod = worldMod.split('\n')
		
		lineCounter = 0
		lineCounterTotal = 0
		linesTotal = len(worldMod)
		for blockLine in worldMod:
			lineCounter += 1
					
			# remove the last empty line
			if blockLine != '':
				coords, blockType = blockLine.split(':')
				# blockTiype is the index in MATERIALS
				blockType = int(blockType)
				
				#print main.MATERIALS
				#print blockType
				#print main.MATERIALS[blockType]
				# convert the json list into tuple; json ONLY get lists but we need tuples
				model.add_block( tuple(json.loads(coords)), main.MATERIALS[blockType], False )
			
			if lineCounter > self.maxLineCounter:
				lineCounterTotal += lineCounter
				lineCounter = 0
				self.printStuff(str(lineCounterTotal) + "/" + str(linesTotal))
				
				# just in case you dont want to exhaust memory!
			if lineCounterTotal >= self.maxVoxels:
				break
			
		self.printStuff("loaded " + str(lineCounterTotal + lineCounter) + " voxels")
		self.printStuff('loading completed')
		
	def saveWorld(self, model):
		self.printStuff('start saving...')
		fh = open(self.getSaveDest(), 'w')
		
		# build a string to save it in one action
		worldString = ''
		
		for block in model.world:
			# 1. convert the block coords into json
			# 2. get the RAW texture data with model.world[block] and find the index in main.MATERIALS.index(i)
			worldString += "{0}:{1}\n".format(json.dumps(block), main.MATERIALS.index(model.world[block]))

		fh.write(worldString)
		fh.close()
		self.printStuff('saving completed')

	def exportStl(self, model):
		self.printStuff('start export stl...')
		fh = open(self.getSaveDest() + '.stl', 'wb')
		#writer = Binary_STL_Writer(fp)
		writer = stlWriter.Binary_STL_Writer(fh)
		
		lineCounter = 0
		lineCounterTotal = 0
		linesTotal = len(model.shown)
		for block in model.shown:
			lineCounter += 1
			writer.add_faces(self.getCubeFaces(block[0],block[1],block[2]))

			if lineCounter > self.maxLineCounter:
				lineCounterTotal += lineCounter
				lineCounter = 0
				self.printStuff(str(lineCounterTotal) + "/" + str(linesTotal))

		writer.close()
		self.printStuff('export stl completed')
	
	def exportStlZstretch(self, model):
		self.printStuff('start export stl Z...')
		fh = open(self.getSaveDest() + '.stl', 'wb')
		#writer = Binary_STL_Writer(fp)
		writer = stlWriter.Binary_STL_Writer(fh)
		
		zCollectionMin = {}
		zCollectionMax = {}
		for block in model.shown:
			xy = (block[0], block[1])
			z = block[2]
			if not xy in zCollectionMin:
				zCollectionMin[xy] = z
			elif z < zCollectionMin[xy]:
				zCollectionMin[xy] = z
			
			if not xy in zCollectionMax:
				zCollectionMax[xy] = z
			elif z > zCollectionMax[xy]:
				zCollectionMax[xy] = z
			
		lineCounter = 0
		lineCounterTotal = 0
		linesTotal = len(model.shown)
		for blockXY in zCollectionMin:
			lineCounter += 1
			
			#print blockXY,":",zCollectionMin[blockXY], zCollectionMax[blockXY]
			writer.add_faces(self.getCubeFaces(blockXY[0],blockXY[1],zCollectionMin[blockXY], zCollectionMax[blockXY]-zCollectionMin[blockXY]))

			if lineCounter > self.maxLineCounter:
				lineCounterTotal += lineCounter
				lineCounter = 0
				self.printStuff(str(lineCounterTotal) + "/" + str(linesTotal))

		writer.close()
		self.printStuff('export stl completed')
		
	def exportStlZ(self, model):
		bw = blockWork.blockWork(model)
		self.printStuff('start export stl Z 2.x...')
		fh = open(self.getSaveDest() + '.stl', 'wb')
		writer = stlWriter.Binary_STL_Writer(fh)
		
		#collectedBlocks = set()
		collectedBlocks = {}
		zTubes =  {}
		for visBlock in model.shown:
			if not visBlock in collectedBlocks:
				x = None
				y = None
				z = None
				minZ = None
				maxZ = None
			
				for block in bw.getConnectedBlocksDirection(visBlock, cZ=True):
					x, y, z = block
					if maxZ is None or z > maxZ:
						maxZ = z
					
					if minZ is None or z < minZ:
						minZ = z
					#collectedBlocks.add(block)
					collectedBlocks[block] = 0
				
				zTubes[(x, y, z)] = (minZ, maxZ)
		
		for tube in zTubes:
			x, y, z = tube
			#print tube, zTubes[tube][0], zTubes[tube][1]
			if zTubes[tube][0] == zTubes[tube][1]:
				writer.add_faces(self.getCubeFaces(x, y, zTubes[tube][0]))
			else:
				# we need the difference between the coords!
				writer.add_faces(self.getCubeFaces(x, y, zTubes[tube][0], zTubes[tube][1]-zTubes[tube][0]))
				
		writer.close()
		self.printStuff('export stl completed')
		
	def getCubeFaces(self, x=0, y=0, z=0, zTop=0):
		# cube size
		s = 1.0
		# cube corner points
		#p1 = (0+x, 0+y, 0+z)
		#p2 = (0+x, 0+y, s+z+zTop)
		#p3 = (0+x, s+y, 0+z)
		#p4 = (0+x, s+y, s+z+zTop)
		#p5 = (s+x, 0+y, 0+z)
		#p6 = (s+x, 0+y, s+z+zTop)
		#p7 = (s+x, s+y, 0+z)
		#p8 = (s+x, s+y, s+z+zTop)
		#x, -z, y

		# rotate X
		# by: derf
		ar = [x, -z, y]
		p1 = (0+ar[0], 0+ar[1], 0+ar[2])
		p2 = (0+ar[0], 0+ar[1], s+ar[2])
		p3 = (0+ar[0], s+ar[1]-zTop, 0+ar[2])
		p4 = (0+ar[0], s+ar[1]-zTop, s+ar[2])
		p5 = (s+ar[0], 0+ar[1], 0+ar[2])
		p6 = (s+ar[0], 0+ar[1], s+ar[2])
		p7 = (s+ar[0], s+ar[1]-zTop, 0+ar[2])
		p8 = (s+ar[0], s+ar[1]-zTop, s+ar[2])

		# define the 6 cube faces
		# faces just lists of 3 or 4 vertices
		return [
			[p1, p5, p7, p3],
			[p1, p5, p6, p2],
			[p5, p7, p8, p6],
			[p7, p8, p4, p3],
			[p1, p3, p4, p2],
			[p2, p6, p8, p4],
		]

	def exportOpenScad(self, model):
		"""
		openscad
		translate([x,y,z]) cube(0.2);
		"""
		
		self.printStuff('start scad export...')
		fh = open(self.getSaveDest() + ".scad", 'w')
		
		# build a string to save it in one action
		worldString = ''
		
		cubeCounter = 0
		for block in model.world:
			#render() { cubes }
			
			cubeCounter += 1
			
			if cubeCounter == 1:
				worldString += "render() {\n"
			
			worldString += "translate([{0},{1},{2}]) cube(1);\n".format(block[0], block[1], block[2])
			
			if cubeCounter >= 100:
				worldString += "};\n"
				cubeCounter = 0
				
		if not worldString.endswith("};\n"):
			worldString += "};\n"
			
		fh.write(worldString)
		fh.close()
		self.printStuff('export scad completed')
