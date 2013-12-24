import DICraft as main # we need the blocktypes from the main program
import json
import os
import sys
from time import gmtime, strftime

class saveModule(object):
	def __init__(self):
		# "tarnslate" the block texture tuples into readable words for saving
		#self.coordDictSave = { str(main.GRASS):'GRASS', str(main.SAND):'SAND', str(main.BRICK):'BRICK', str(main.STONE):'STONE' }	  
		# "tarnslate" the words back into tuples for loading
		#self.coordDictLoad = { 'GRASS':main.GRASS, 'SAND':main.SAND, 'BRICK':main.BRICK, 'STONE':main.STONE }
				
		self.saveFile = 'quicksave.sav'
		self.saveFolder =  "saves"
		if len(sys.argv) > 1:
			for arg in sys.argv:
				if arg.startswith("savefile="):
					self.saveFile = arg.replace("savefile=", "")
		
		self.printStuff("working with file: " + self.getSaveDest())
		
		# max voxels to load
		self.maxVoxels = 10000000
		
	def printStuff(self, txt):
		print(strftime("%d-%m-%Y %H:%M:%S|", gmtime()) + str(txt) ) 
	
	def getSaveDest(self):
		return os.path.join(self.saveFolder, self.saveFile)
	
	def hasSaveGame(self):
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
			lineCounterTotal += 1
					
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
			
			if lineCounter > 1000:
				lineCounter = 0
				self.printStuff(str(lineCounterTotal) + "/" + str(linesTotal))
				
				# just in case you dont want to exhaust memory!
			if lineCounterTotal >= self.maxVoxels:
				break
			
		self.printStuff("loaded " + str(lineCounterTotal) + " blocks")
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
		
	def exportOpenScad(self, model):
		"""
		openscad
		translate([x,y,z]) cube(0.2);
		"""
		
		self.printStuff('start export...')
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
		self.printStuff('export completed')
