import DICraft
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
		for dx, dy, dz in FACES:
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
		
		print "removing blocks:", len(block_collection)
		for b in block_collection:
			self.remove_block(b)

	def getVolumes(self):
		volumeList = []
		
		blocksTotal = len(self.model.world)
		blocksCurrent = 0
		
		for block in self.model.world:
			blocksCurrent += 1
			isScanned = False
			for volume in volumeList:
				if block in volume:
					isScanned = True
					
			if not isScanned:
				print blocksCurrent, "/", blocksTotal
				#print "found new volume:", block
				volumeList.append(self.getConnectedBlocks(block))
				#print "volume size:", volumeList[len(volumeList)-1]
				
		for volume in volumeList:
			print "size:", len(volume)
			
		print "found", len(volumeList), "connected volumes"
			
		return volumeList

	def getConnectedBlocks(self, startBlock):
		blockCollection = []
		if startBlock:
			blockCollection = [startBlock, ]
			blocksToCheck = [startBlock, ]

			blockCountCurrent = 0
			self.mt.start("getConnectedBlocks")
			while blocksToCheck:
				x, y, z = blocksToCheck.pop()
				for dx, dy, dz in DICraft.FACES:
					blockCountCurrent += 1
					key = (x + dx, y + dy, z + dz)
					if key in self.model.world and not key in blockCollection:
						blockCollection.append(key)
						blocksToCheck.append(key)
				
				if self.mt.duration("getConnectedBlocks") >= 10:
					self.mt.start("getConnectedBlocks")
					print "still alive, found", len(blockCollection), "voxel so far", "(", blockCountCurrent / 10 ,"/s)"
					blockCountCurrent = 0
						
		return blockCollection
		
	def removeBlockIsle(self, startBlock):
		if startBlock:
			blockCollection = self.getConnectedBlocks(startBlock)
			print "removing blocks:", len(blockCollection)
			rmCounter = 0
			rmCounterTotal = 0
			for b in blockCollection:
				rmCounter += 1
				self.model.remove_block(b)
				if rmCounter >= 100:
					rmCounterTotal += rmCounter
					rmCounter = 0
					print rmCounterTotal, "/", len(blockCollection)
					
			print rmCounterTotal, "/", len(blockCollection)
			print "removing completed"
