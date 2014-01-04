import DICraft

class blockwork(object):

	def __init__(self, model):
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
			if key in self.world and not key in my_neighbors:
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

	def removeBlockIsle(self, startBlock):
		if startBlock:
			blockCollection = []
			blocksToCheck = [startBlock, ]
			
			while blocksToCheck:
				x, y, z = blocksToCheck.pop()
				for dx, dy, dz in DICraft.FACES:
					key = (x + dx, y + dy, z + dz)
					if not key in blockCollection and key in self.model.world:
						blockCollection.append(key)
						blocksToCheck.append(key)
						#print "found",key,blocksToCheck,blockCollection
				
			print "removing blocks:", len(blockCollection)
			rmCounter = 0
			for b in blockCollection:
				rmCounter += 1
				self.model.remove_block(b)
				if rmCounter >= 100:
					rmCounter = 0
					print rmCounter, "/", len(blockCollection)
			print "removing completed"
