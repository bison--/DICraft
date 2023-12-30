import engine
import multiTimer

class blockWork(object):

	def __init__(self, model):
		self.mt = multiTimer.multiTimer()
		self.model = model

	def _get_neighbor_blocks_r(self, block, neighbors):
		""" Finds the surrounding blocks of given block.
			WARNING: crashes after too many recursive calls!

		Parameters
		----------
		block : tuple of len 3
			The (x, y, z) position of the block.
		neighbors : tuple
			combined list of neighbors

		"""
		my_neighbors = neighbors
		my_neighbors.append(block)
		x, y, z = block
		for dx, dy, dz in engine.FACES:
			key = (x + dx, y + dy, z + dz)
			if key in self.model.world and not key in my_neighbors:
				my_neighbors + self._get_neighbor_blocks(key, my_neighbors)
				
		return my_neighbors
		
	def remove_block_isle_r(self, start_block):
		""" Removing a bunch of blocks that belongs to each other

		Parameters
		----------
		start_block : tuple of len 3
			The (x, y, z) position of the start block to remove.
		"""

		block_collection = []
		if start_block:
			x, y, z = start_block
			block_collection + self._get_neighbor_blocks(start_block, block_collection)
		
		print("removing blocks:", len(block_collection))
		for b in block_collection:
			self.remove_block(b)

	def getVolumes(self):
		""" return a list of dictionarys with connected blocks which build a volume
		"""
		volumeList = []
		
		blocksTotal = len(self.model.world)
		blocksCurrent = 0
		
		for block in self.model.world:
			blocksCurrent += 1
			isScanned = False
			for volume in volumeList:
				if block in volume:
					isScanned = True
					break
					
			if not isScanned:
				print(blocksCurrent, "/", blocksTotal)
				#print "found new volume:", block
				volumeList.append(self.getConnectedBlocks(block))
				#print "volume size:", volumeList[len(volumeList)-1]
				
		for volume in volumeList:
			print("size:", len(volume))

		print("found", len(volumeList), "connected volumes")

		return volumeList

	def getConnectedBlocks(self, startBlock):
		""" returns a dictionary with ALL connected blocks, a volume
		"""
		blockCollection = {}
		if startBlock:
			blockCollection = {startBlock:0}
			blocksToCheck = [startBlock, ]

			blockCountCurrent = 0
			self.mt.start("getConnectedBlocks")
			while blocksToCheck:
				x, y, z = blocksToCheck.pop()
				for dx, dy, dz in engine.FACES:
					blockCountCurrent += 1
					key = (x + dx, y + dy, z + dz)
					#kI = self.model.world.index(key)
					if key in self.model.world and not key in blockCollection:
						blockCollection[key] = 0
						blocksToCheck.append(key)
				
				if self.mt.duration("getConnectedBlocks") >= 10:
					self.mt.start("getConnectedBlocks")
					print("still alive, found", len(blockCollection), "voxel so far", "(", blockCountCurrent / 10,
						  "/s)")
					blockCountCurrent = 0
						
		return blockCollection
		
	def getConnectedBlocksDirection(self, startBlock, cX=False, cY=False, cZ=False):
		blockCollection = set()
		if startBlock:
			#blockCollection = set(startBlock)
			blockCollection = {startBlock:0,}
			blocksToCheck = [startBlock, ]
			
			blockCountCurrent = 0
			self.mt.start("getConnectedBlocksDirection")
			while blocksToCheck:
				x, y, z = blocksToCheck.pop()
								
				for dx, dy, dz in engine.FACES:
					blockCountCurrent += 1
					key = (x + dx, y + dy, z + dz)
					doThisOne = False
					
					if cX and dx != 0:
						doThisOne = True
					elif cY and dy != 0:
						doThisOne = True
					elif cZ and dz != 0:
						doThisOne = True
					
					if doThisOne and key in self.model.world and not key in blockCollection:
						#blockCollection.add(key)
						blockCollection[key] = 0
						blocksToCheck.append(key)
				
				if self.mt.duration("getConnectedBlocks") >= 10:
					self.mt.start("getConnectedBlocks")
					print("still alive, found", len(blockCollection), "voxel so far", "(", blockCountCurrent / 10,
						  "/s)")
					blockCountCurrent = 0

		return blockCollection
		
	def removeSmallVolumes(self, volumeList, smallest = 10000):
		""" collects ALL volumes and removes if the size is smaller than the given size
		"""
		volCounter = 0
		for volume in volumeList:
			volCounter += 1
			if len(volume) < smallest:
				print("removing volume:", volCounter, "/", len(volumeList), "(", len(volume), "blocks)")
				rmCounter = 0
				rmCounterTotal = 0
				for key in volume.keys():
					self.model.remove_block(key)
					rmCounter += 1
					if rmCounter >= 100:
						rmCounterTotal += rmCounter
						rmCounter = 0
						print(rmCounterTotal, "/", len(volume))

	def removeBlockIsle(self, startBlock):
		""" removes ALL blocks connected to the given block!
		"""
		if startBlock:
			blockCollection = self.getConnectedBlocks(startBlock)
			print("removing blocks:", len(blockCollection))
			rmCounter = 0
			rmCounterTotal = 0
			for b in blockCollection.keys():
				rmCounter += 1
				self.model.remove_block(b)
				if rmCounter >= 100:
					rmCounterTotal += rmCounter
					rmCounter = 0
					print(rmCounterTotal, "/", len(blockCollection))

			print(rmCounterTotal, "/", len(blockCollection))
			print("removing completed")

	def fillHoles(self, smallest=10000):
		spaceList = self.getHoles()
		print("found", len(spaceList), "holes")

		for hole in spaceList:
			if len(hole) < smallest:
				print("filling hole", len(hole))
				for space in hole:
					self.model.add_block(space)

		print("fillHoles completed")

	def getWorldBoundaries(self, addSpace=True):
		axRange = range(3)
		boundaries = [[None, None], [None, None], [None, None]]
				
		# get min and max from every axis
		for block in self.model.world:
			for axis in axRange:
				#print "block[axis]", block[axis]
				if boundaries[axis][0] is None or block[axis] < boundaries[axis][0]:
					boundaries[axis][0] = block[axis]
					
				if boundaries[axis][1] is None or block[axis] > boundaries[axis][1]:
					boundaries[axis][1] = block[axis]
		
		# add more space to make shure the outer space surrounded the whole construct		
		if addSpace:
			for axis in axRange:
				boundaries[axis][0] -= 1
				boundaries[axis][1] += 1
			
		return boundaries
	
	def isInWorldBoundaries(self, block, boundaries):	
		isInBound = True
		if block[0] < boundaries[0][0] or block[0] > boundaries[0][1]:
			isInBound = False
		elif block[1] < boundaries[1][0] or block[1] > boundaries[1][1]:
			isInBound = False
		elif block[2] < boundaries[2][0] or block[2] > boundaries[2][1]:
			isInBound = False
	
		#if isInBound:
			#print "block, boundaries", block, boundaries
		return isInBound
		
	def getHoles(self):
		boundaries = self.getWorldBoundaries()
		#boundaries = {"x":[None, None], "y":[None, None], "z":[None, None]}
		#boundariesX = [None, None]
		#boundariesY = [None, None]
		#boundariesZ = [None, None]
		
		blockDict = {}
		if self.model.shown:
			blockDict = self.model.shown
		else:
			blockDict = self.model.world
		
		checkedBlocks = {}
		spaceList = []
		spaceToCheck = []
		for block in blockDict:
			checkedBlocks[block] = 0
			x, y, z = block
			for dx, dy, dz in engine.FACES:
				key = (x + dx, y + dy, z + dz)
				
				if not key in self.model.world and not key in spaceToCheck and not key in checkedBlocks and self.isInWorldBoundaries(key, boundaries):
					print("spaceToCheck.append(key)", key)
					spaceToCheck.append(key)
			
			while spaceToCheck:
				space = spaceToCheck.pop()
				checkedBlocks[space] = 0
				if not space in self.model.world and not space in spaceToCheck and self.isInWorldBoundaries(space, boundaries):
					spaceList.append(self.getConnectedSpace(space, boundaries))
				
		return spaceList
		
	def getConnectedSpace(self, startSpace, boundaries=None):
		if not boundaries:
			boundaries = self.getWorldBoundaries()
		
		if startSpace:
			blockCollection = {startSpace:0}
			blocksToCheck = [startSpace, ]

			blockCountCurrent = 0
			self.mt.start("getConnectedBlocks")
			while blocksToCheck:
				x, y, z = blocksToCheck.pop()
				for dx, dy, dz in engine.FACES:
					blockCountCurrent += 1
					key = (x + dx, y + dy, z + dz)
					#kI = self.model.world.index(key)
					
					if not key in self.model.world and not key in blockCollection and self.isInWorldBoundaries(key, boundaries):
						blockCollection[key] = 0
						blocksToCheck.append(key)
				
				if self.mt.duration("getConnectedBlocks") >= 10:
					self.mt.start("getConnectedBlocks")
					print("still alive, found", len(blockCollection), "voxel so far", "(", blockCountCurrent / 10,
						  "/s)")
					blockCountCurrent = 0

		print("found space volume:", len(blockCollection))
		return blockCollection
