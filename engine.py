import time
import multiTimer
import saveModule

from collections import deque
# TODO: remove/move this kind of stuff to rendering engine!
import pyglet
from pyglet import image
from pyglet.gl import *
from pyglet.graphics import TextureGroup

# default cube size is 0.5
# not changeable, yet
CUBE_SIZE = 0.5

# Size of sectors used to ease block loading.
SECTOR_SIZE = 150

def cube_vertices(x, y, z, n):
	""" Return the vertices of the cube at position x, y, z with size 2*n.

	"""
	return [
		x-n,y+n,z-n, x-n,y+n,z+n, x+n,y+n,z+n, x+n,y+n,z-n,  # top
		x-n,y-n,z-n, x+n,y-n,z-n, x+n,y-n,z+n, x-n,y-n,z+n,  # bottom
		x-n,y-n,z-n, x-n,y-n,z+n, x-n,y+n,z+n, x-n,y+n,z-n,  # left
		x+n,y-n,z+n, x+n,y-n,z-n, x+n,y+n,z-n, x+n,y+n,z+n,  # right
		x-n,y-n,z+n, x+n,y-n,z+n, x+n,y+n,z+n, x-n,y+n,z+n,  # front
		x+n,y-n,z-n, x-n,y-n,z-n, x-n,y+n,z-n, x+n,y+n,z-n,  # back
	]


def tex_coord(x, y, n=200):
	""" Return the bounding vertices of the texture square.
	
	Parameters:
	n : the NUMBER of texture elements on the X/WITH axis of the image
	"""
	m = 1.0 / n
	dx = x * m
	dy = y * m
	return dx, dy, dx + m, dy, dx + m, dy + m, dx, dy + m


def tex_coords(top, bottom, side):
	""" Return a list of the texture squares for the top, bottom and side.

	"""
	top = tex_coord(*top)
	bottom = tex_coord(*bottom)
	side = tex_coord(*side)
	result = []
	result.extend(top)
	result.extend(bottom)
	result.extend(side * 4)
	return result

def tex_coords_simple(xCoord):
	""" Return a list of the texture squares for the top, bottom and side.

	"""
	allSides = (xCoord, 0)
	
	top = tex_coord(*allSides)
	bottom = tex_coord(*allSides)
	side = tex_coord(*allSides)
	result = []
	result.extend(top)
	result.extend(bottom)
	result.extend(side * 4)
	return result

TEXTURE_PATH = 'texture.png'

#GRASS = tex_coords((1, 0), (0, 1), (0, 0))
#SAND = tex_coords((1, 1), (1, 1), (1, 1))
#BRICK = tex_coords((2, 0), (2, 0), (2, 0))
#STONE = tex_coords((2, 1), (2, 1), (2, 1))

MATERIALS = []
for i in xrange(100):
	MATERIALS.append(tex_coords_simple(i))


FACES = [
	( 0, 1, 0),
	( 0,-1, 0),
	(-1, 0, 0),
	( 1, 0, 0),
	( 0, 0, 1),
	( 0, 0,-1),
]


def normalize(position):
	""" Accepts `position` of arbitrary precision and returns the block
	containing that position.

	Parameters
	----------
	position : tuple of len 3

	Returns
	-------
	block_position : tuple of ints of len 3

	"""
	x, y, z = position
	x, y, z = (int(round(x)), int(round(y)), int(round(z)))
	return (x, y, z)


def sectorize(position):
	""" Returns a tuple representing the sector for the given `position`.

	Parameters
	----------
	position : tuple of len 3

	Returns
	-------
	sector : tuple of len 3

	"""
	x, y, z = normalize(position)
	x, y, z = x / SECTOR_SIZE, y / SECTOR_SIZE, z / SECTOR_SIZE
	return (x, 0, z)


class Model(object):

	def __init__(self):

		# A Batch is a collection of vertex lists for batched rendering.
		self.batch = pyglet.graphics.Batch()

		# A TextureGroup manages an OpenGL texture.
		self.group = TextureGroup(image.load(TEXTURE_PATH).get_texture())

		# A mapping from position to the texture of the block at that position.
		# This defines all the blocks that are currently in the world.
		self.world = {}

		# Same mapping as `world` but only contains blocks that are shown.
		self.shown = {}

		# Mapping from position to a pyglet `VertextList` for all shown blocks.
		self._shown = {}

		# Mapping from sector to a list of positions inside that sector.
		self.sectors = {}

		# Simple function queue implementation. The queue is populated with
		# _show_block() and _hide_block() calls
		self.queue = deque()
		
		# a module to save and load the world
		self.saveModule = saveModule.saveModule()
		
		# notifications to display
		self.notification = ""

		self._initialize()

	def _initialize(self):
		""" Initialize the world by placing all the blocks.

		"""
		
		if self.saveModule.hasSaveFile() == True:
			self.saveModule.loadWorld(self)
		else:
			print "no savefile, generating sample"
			
			for x in xrange(len(MATERIALS)):
				self.add_block((x, 0, 0), MATERIALS[x], immediate=False)
				
			for z in xrange(len(MATERIALS)):
				self.add_block((0, z, 1), MATERIALS[z], immediate=False)
				
			for y in xrange(len(MATERIALS)):
				self.add_block((0, 2, y), MATERIALS[y], immediate=False)
		
	def hit_test(self, position, vector, max_distance=8):
		""" Line of sight search from current position. If a block is
		intersected it is returned, along with the block previously in the line
		of sight. If no block is found, return None, None.

		Parameters
		----------
		position : tuple of len 3
			The (x, y, z) position to check visibility from.
		vector : tuple of len 3
			The line of sight vector.
		max_distance : int
			How many blocks away to search for a hit.

		"""
		m = 8
		x, y, z = position
		dx, dy, dz = vector
		previous = None
		for _ in xrange(max_distance * m):
			key = normalize((x, y, z))
			if key != previous and key in self.world:
				return key, previous
			previous = key
			x, y, z = x + dx / m, y + dy / m, z + dz / m
		return None, None

	def get_empty_space(self, position, vector, max_distance=8):
		""" returns the position of empty space in range
		return none if there is no empty space
		
		Parameters
		----------
		position : tuple of len 3
			The (x, y, z) position to check visibility from.
		vector : tuple of len 3
			The line of sight vector.
		max_distance : int
			How many blocks away to search for a hit.
			
		"""
		m = 8
		x, y, z = position
		dx, dy, dz = vector
		previous = None
		
		rangeCounter = 0
		for _ in xrange(max_distance * m):
			rangeCounter += 1
			if rangeCounter == max_distance * m:
				key = normalize((x, y, z))
				if not key in self.world:
					return key
			x, y, z = x + dx / m, y + dy / m, z + dz / m
		return None
		

	def exposed(self, position):
		""" Returns False is given `position` is surrounded on all 6 sides by
		blocks, True otherwise.

		"""
		x, y, z = position
		for dx, dy, dz in FACES:
			if (x + dx, y + dy, z + dz) not in self.world:
				return True
		return False

	def add_block(self, position, texture, immediate=True):
		""" Add a block with the given `texture` and `position` to the world.

		Parameters
		----------
		position : tuple of len 3
			The (x, y, z) position of the block to add.
		texture : list of len 3
			The coordinates of the texture squares. Use `tex_coords()` to
			generate.
		immediate : bool
			Whether or not to draw the block immediately.

		"""
		if position in self.world:
			self.remove_block(position, immediate)
		self.world[position] = texture
		self.sectors.setdefault(sectorize(position), []).append(position)
		if immediate:
			if self.exposed(position):
				self.show_block(position)
			self.check_neighbors(position)

	def remove_block(self, position, immediate=True):
		""" Remove the block at the given `position`.

		Parameters
		----------
		position : tuple of len 3
			The (x, y, z) position of the block to remove.
		immediate : bool
			Whether or not to immediately remove block from canvas.

		"""
		del self.world[position]
		self.sectors[sectorize(position)].remove(position)
		if immediate:
			if position in self.shown:
				self.hide_block(position)
			self.check_neighbors(position)
		
	def check_neighbors(self, position):
		""" Check all blocks surrounding `position` and ensure their visual
		state is current. This means hiding blocks that are not exposed and
		ensuring that all exposed blocks are shown. Usually used after a block
		is added or removed.

		"""
		x, y, z = position
		for dx, dy, dz in FACES:
			key = (x + dx, y + dy, z + dz)
			if key not in self.world:
				continue
			if self.exposed(key):
				if key not in self.shown:
					self.show_block(key)
			else:
				if key in self.shown:
					self.hide_block(key)

	def show_block(self, position, immediate=True):
		""" Show the block at the given `position`. This method assumes the
		block has already been added with add_block()

		Parameters
		----------
		position : tuple of len 3
			The (x, y, z) position of the block to show.
		immediate : bool
			Whether or not to show the block immediately.

		"""
		texture = self.world[position]
		self.shown[position] = texture
		if immediate:
			self._show_block(position, MATERIALS[texture])
		else:
			self._enqueue(self._show_block, position, MATERIALS[texture])

	def _show_block(self, position, texture):
		""" Private implementation of the `show_block()` method.

		Parameters
		----------
		position : tuple of len 3
			The (x, y, z) position of the block to show.
		texture : list of len 3
			The coordinates of the texture squares. Use `tex_coords()` to
			generate.

		"""
		x, y, z = position
		vertex_data = cube_vertices(x, y, z, CUBE_SIZE)
		texture_data = list(texture)
		# create vertex list
		# FIXME Maybe `add_indexed()` should be used instead
		self._shown[position] = self.batch.add(24, GL_QUADS, self.group,
			('v3f/static', vertex_data),
			('t2f/static', texture_data))

	def hide_block(self, position, immediate=True):
		""" Hide the block at the given `position`. Hiding does not remove the
		block from the world.

		Parameters
		----------
		position : tuple of len 3
			The (x, y, z) position of the block to hide.
		immediate : bool
			Whether or not to immediately remove the block from the canvas.

		"""
		self.shown.pop(position)
		if immediate:
			self._hide_block(position)
		else:
			self._enqueue(self._hide_block, position)

	def _hide_block(self, position):
		""" Private implementation of the 'hide_block()` method.

		"""
		self._shown.pop(position).delete()

	def show_sector(self, sector):
		""" Ensure all blocks in the given sector that should be shown are
		drawn to the canvas.

		"""
		for position in self.sectors.get(sector, []):
			if position not in self.shown and self.exposed(position):
				self.show_block(position, False)

	def hide_sector(self, sector):
		""" Ensure all blocks in the given sector that should be hidden are
		removed from the canvas.

		"""
		for position in self.sectors.get(sector, []):
			if position in self.shown:
				self.hide_block(position, False)

	def change_sectors(self, before, after):
		""" Move from sector `before` to sector `after`. A sector is a
		contiguous x, y sub-region of world. Sectors are used to speed up
		world rendering.

		"""	
		before_set = set()
		after_set = set()
		pad = 4
		for dx in xrange(-pad, pad + 1):
			for dy in [0]:  # xrange(-pad, pad + 1):
				for dz in xrange(-pad, pad + 1):
					if dx ** 2 + dy ** 2 + dz ** 2 > (pad + 1) ** 2:
						continue
					if before:
						x, y, z = before
						before_set.add((x + dx, y + dy, z + dz))
					if after:
						x, y, z = after
						after_set.add((x + dx, y + dy, z + dz))
		show = after_set - before_set
		hide = before_set - after_set
		for sector in show:
			self.show_sector(sector)
		for sector in hide:
			self.hide_sector(sector)

	def _enqueue(self, func, *args):
		""" Add `func` to the internal queue.

		"""
		self.queue.append((func, args))

	def _dequeue(self):
		""" Pop the top function from the internal queue and call it.

		"""
		func, args = self.queue.popleft()
		func(*args)

	def process_queue(self):
		""" Process the entire queue while taking periodic breaks. This allows
		the game loop to run smoothly. The queue contains calls to
		_show_block() and _hide_block() so this method should be called if
		add_block() or remove_block() was called with immediate=False

		"""
		start = time.clock()
		while self.queue and time.clock() - start < 1 / 60.0:
			self._dequeue()

	def process_entire_queue(self):
		""" Process the entire queue with no breaks.

		"""
		while self.queue:
			self._dequeue()
