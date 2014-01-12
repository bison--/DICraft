import math
import random
import time
import sys

##from collections import deque
##from pyglet import image
#from pyglet.gl import *
##from pyglet.graphics import TextureGroup
import pyglet
from pyglet.window import key
from engine import *

import blockWork
import saveModule
import multiTimer

sys.setrecursionlimit(64000)

# distance for interaction with cubes
EDIT_DISTANCE = 42


class Window(pyglet.window.Window):

	def __init__(self, *args, **kwargs):
		super(Window, self).__init__(*args, **kwargs)

		# Whether or not the window exclusively captures the mouse.
		self.exclusive = False

		# When flying gravity has no effect and speed is increased.
		self.flying = True

		# First element is -1 when moving forward, 1 when moving back, and 0
		# otherwise. The second element is -1 when moving left, 1 when moving
		# right, and 0 otherwise.
		self.strafe = [0, 0]

		# Current (x, y, z) position in the world, specified with floats.
		self.position = (-2, -2, 1)

		# First element is rotation of the player in the x-z plane (ground
		# plane) measured from the z-axis down. The second is the rotation
		# angle from the ground plane up.
		self.rotation = (100, 0)

		# Which sector the player is currently in.
		self.sector = None

		# The crosshairs at the center of the screen.
		self.reticle = None

		# Velocity in the y (upward) direction.
		self.dy = 0

		# A list of blocks the player can place. Hit num keys to cycle.
		self.inventory = []
		for i in range(0, len(MATERIALS), 10):
			#print "inventory:",i, MATERIALS[i]
			self.inventory.append(MATERIALS[i])

		# The current block the user can place. Hit num keys to cycle.
		self.block = self.inventory[0]

		# Convenience list of num keys.
		self.num_keys = [
			key._1, key._2, key._3, key._4, key._5,
			key._6, key._7, key._8, key._9, key._0]

		# the block that is currently focused
		self.focusedBlock = None

		# Instance of the model that handles the world.
		self.model = Model()
		
		# Instance of world modificator "blockwork"
		self.blockWork = blockWork.blockWork(self.model)

		self.labelDict = {}

		# The label that is displayed in the top left of the canvas.
		self.labelDict['worldInfo'] = pyglet.text.Label('', font_name='Arial', font_size=16,
			x=10, y=self.height - 10, anchor_x='left', anchor_y='top',
			color=(0, 0, 0, 255))

		# fix label while rendering the world
		self.labelDict['loabel'] = pyglet.text.Label("!RENDERING WORLD, STAY TUNED!", font_name='Arial', font_size=16,
			x=self.width / 2, y=self.height / 2 , anchor_x='center', anchor_y='top',
			color=(0, 0, 0, 255))
			
		# notifications from engine
		self.labelDict['notify'] = pyglet.text.Label("", font_name='Arial', font_size=16,
			x=self.width / 2, y=self.height / 2 , anchor_x='center', anchor_y='top',
			color=(0, 0, 0, 255))
		
		# focues block label
		self.labelDict['focusedBlock'] = pyglet.text.Label("", font_name='Arial', font_size=12,
			x=5, y=25, anchor_x='left', anchor_y='top',
			color=(0, 0, 0, 255))

		# This call schedules the `update()` method to be called 60 times a
		# second. This is the main game event loop.
		pyglet.clock.schedule_interval(self.update, 1.0 / 60)
		
		# interaction speed during mouse down events
		self.mouseInteractionSpeed = 0.35
		
		# start in window mode!
		self.fullScreen = False
		
		# a master timer for all the timers!
		self.mt = multiTimer.multiTimer()
		
		# collect and remove "small" volumes
		#self.blockWork.removeSmallVolumes(self.blockWork.getVolumes(), 10000)
		
		# add timer and bool for the initial loading text while rendereing the world
		# for the first time
		self.renderWorld = True
		self.mt.start("renderWorld")

	def set_exclusive_mouse(self, exclusive):
		""" If `exclusive` is True, the game will capture the mouse, if False
		the game will ignore the mouse.

		"""
		super(Window, self).set_exclusive_mouse(exclusive)
		self.exclusive = exclusive

	def get_sight_vector(self):
		""" Returns the current line of sight vector indicating the direction
		the player is looking.

		"""
		x, y = self.rotation
		m = math.cos(math.radians(y))
		dy = math.sin(math.radians(y))
		dx = math.cos(math.radians(x - 90)) * m
		dz = math.sin(math.radians(x - 90)) * m
		return (dx, dy, dz)

	def get_motion_vector(self):
		""" Returns the current motion vector indicating the velocity of the
		player.

		Returns
		-------
		vector : tuple of len 3
			Tuple containing the velocity in x, y, and z respectively.

		"""
		if any(self.strafe):
			x, y = self.rotation
			strafe = math.degrees(math.atan2(*self.strafe))
			if self.flying:
				m = math.cos(math.radians(y))
				dy = math.sin(math.radians(y))
				if self.strafe[1]:
					dy = 0.0
					m = 1
				if self.strafe[0] > 0:
					dy *= -1
				dx = math.cos(math.radians(x + strafe)) * m
				dz = math.sin(math.radians(x + strafe)) * m
			else:
				dy = 0.0
				dx = math.cos(math.radians(x + strafe))
				dz = math.sin(math.radians(x + strafe))
		else:
			dy = 0.0
			dx = 0.0
			dz = 0.0
		return (dx, dy, dz)

	def update(self, dt):
		""" This method is scheduled to be called repeatedly by the pyglet
		clock.

		Parameters
		----------
		dt : float
			The change in time since the last call.

		"""
		self.model.process_queue()
		sector = sectorize(self.position)
		if sector != self.sector:
			self.model.change_sectors(self.sector, sector)
			if self.sector is None:
				self.model.process_entire_queue()
			self.sector = sector
		m = 8
		dt = min(dt, 0.2)
		for _ in xrange(m):
			self._update(dt / m)

	def _update(self, dt):
		""" Private implementation of the `update()` method. This is where most
		of the motion logic lives, along with gravity and collision detection.

		Parameters
		----------
		dt : float
			The change in time since the last call.

		"""
		# walking
		speed = 15 if self.flying else 5
		d = dt * speed
		dx, dy, dz = self.get_motion_vector()
		dx, dy, dz = dx * d, dy * d, dz * d
		# gravity
		if not self.flying:
			# g force, should be = jump_speed * 0.5 / max_jump_height
			self.dy -= dt * 0.044
			self.dy = max(self.dy, -0.5)  # terminal velocity
			dy += self.dy
		elif self.dy != 0.0:
			dy += self.dy / speed
				
		# collisions
		x, y, z = self.position
		#x, y, z = self.collide((x + dx, y + dy, z + dz), 2)
		# disable collision
		#self.position = (x, y, z)
		self.position = (x + dx, y + dy, z + dz)
		
		# during mouse down events, do some interaction
		if self.mt.duration("mouse.LEFT") > self.mouseInteractionSpeed:
			vector = self.get_sight_vector()
			block, previous = self.model.hit_test(self.position, vector, EDIT_DISTANCE)
			if block:
				texture = self.model.world[block]
				self.model.remove_block(block)
			self.mt.start("mouse.LEFT")
		elif self.mt.duration("mouse.RIGHT") > self.mouseInteractionSpeed:
			vector = self.get_sight_vector()
			block, previous = self.model.hit_test(self.position, vector, EDIT_DISTANCE)
			if previous:
				self.model.add_block(previous, self.block)
			self.mt.start("mouse.RIGHT")

	def collide(self, position, height):
		""" Checks to see if the player at the given `position` and `height`
		is colliding with any blocks in the world.

		Parameters
		----------
		position : tuple of len 3
			The (x, y, z) position to check for collisions at.
		height : int or float
			The height of the player.

		Returns
		-------
		position : tuple of len 3
			The new position of the player taking into account collisions.

		"""	  
		pad = 0.25
		p = list(position)
		np = normalize(position)
		for face in FACES:  # check all surrounding blocks
			for i in xrange(3):  # check each dimension independently
				if not face[i]:
					continue
				d = (p[i] - np[i]) * face[i]
				if d < pad:
					continue
				for dy in xrange(height):  # check each height
					op = list(np)
					op[1] -= dy
					op[i] += face[i]
					op = tuple(op)
					if op not in self.model.world:
						continue
					p[i] -= (d - pad) * face[i]
					if face == (0, -1, 0) or face == (0, 1, 0):
						self.dy = 0
					break
		return tuple(p)

	def on_mouse_press(self, x, y, button, modifiers):
		""" Called when a mouse button is pressed. See pyglet docs for button
		amd modifier mappings.

		Parameters
		----------
		x, y : int
			The coordinates of the mouse click. Always center of the screen if
			the mouse is captured.
		button : int
			Number representing mouse button that was clicked. 1 = left button,
			4 = right button.
		modifiers : int
			Number representing any modifying keys that were pressed when the
			mouse button was clicked.

		"""
		if self.exclusive:
			vector = self.get_sight_vector()
			block, previous = self.model.hit_test(self.position, vector, EDIT_DISTANCE)
			if button == pyglet.window.mouse.LEFT:
				self.mt.start("mouse.LEFT")
				if block:
					texture = self.model.world[block]
					self.model.remove_block(block)
			else:
				self.mt.start("mouse.RIGHT")
				if previous:
					self.model.add_block(previous, self.block)
				else:
					emptySpace = self.model.get_empty_space(self.position, vector)
					if emptySpace:
						self.model.add_block(emptySpace, self.block)
		else:
			self.set_exclusive_mouse(True)

	def on_mouse_release(self, x, y, button, modifiers):
		""" Called when a mouse button is released.
		"""
		# stop the "interaction" timers
		if button == pyglet.window.mouse.LEFT:
			self.mt.stop("mouse.LEFT")
		elif button == pyglet.window.mouse.RIGHT:
			self.mt.stop("mouse.RIGHT")
			
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		""" Called when the player moves the mouse AND a mouse button is pressed.
		
		Parameters
		----------
		x, y : int
			The coordinates of the mouse click. Always center of the screen if
			the mouse is captured.
		dx, dy : float
			The movement of the mouse.
		button : int
			Number representing mouse button that was clicked. 1 = left button,
			4 = right button.
		modifiers : int
			Number representing any modifying keys that were pressed when the
			mouse button was clicked.
		"""
		# allow movement while mouse button is down
		self.on_mouse_motion(x, y, dx, dy)
		# simulate a "dead" center for non-trackball users
		if dx > 1.0 or dy > 1.0:
			# when moved, use the mouse like a brush
			self.on_mouse_press(x, y, buttons, modifiers)
		
	def on_mouse_motion(self, x, y, dx, dy):
		""" Called when the player moves the mouse.

		Parameters
		----------
		x, y : int
			The coordinates of the mouse click. Always center of the screen if
			the mouse is captured.
		dx, dy : float
			The movement of the mouse.

		"""
		if self.exclusive:
			m = 0.15
			x, y = self.rotation
			x, y = x + dx * m, y + dy * m
			y = max(-90, min(90, y))
			self.rotation = (x, y)

	def on_key_press(self, symbol, modifiers):
		""" Called when the player presses a key. See pyglet docs for key
		mappings.

		Parameters
		----------
		symbol : int
			Number representing the key that was pressed.
		modifiers : int
			Number representing any modifying keys that were pressed.

		"""
		if symbol == key.W:
			self.strafe[0] -= 1
		elif symbol == key.S:
			self.strafe[0] += 1
		elif symbol == key.A:
			self.strafe[1] -= 1
		elif symbol == key.D:
			self.strafe[1] += 1
		elif symbol == key.SPACE:
			#if self.dy == 0:
			self.dy = 1.0  # jump speed
		elif symbol == key.LCTRL:
			#if self.dy == 0:
			self.dy = -1.0
		elif symbol == key.R:
			# reset position in case of getting "lost"
			self.position = (-2, -2, 1)
			self.rotation = (100, 0)
		elif symbol == key.DELETE:
			vector = self.get_sight_vector()
			block = self.model.hit_test(self.position, vector, EDIT_DISTANCE)[0]
			self.blockWork.removeBlockIsle(block)
		elif symbol == key.F5:
			self.model.saveModule.saveWorld(self.model)
		elif symbol == key.F6:
			#self.model.saveModule.exportOpenScad(self.model)
			self.model.saveModule.exportStlZ(self.model)
		elif symbol == key.ESCAPE:
			exit()
		elif symbol == key.F1:
			self.set_exclusive_mouse(False)
		elif symbol == key.TAB:
			self.flying = not self.flying
		elif symbol in self.num_keys:
			index = (symbol - self.num_keys[0]) % len(self.inventory)
			print index
			self.block = self.inventory[index]

	def on_key_release(self, symbol, modifiers):
		""" Called when the player releases a key. See pyglet docs for key
		mappings.

		Parameters
		----------
		symbol : int
			Number representing the key that was pressed.
		modifiers : int
			Number representing any modifying keys that were pressed.

		"""
		if symbol == key.W:
			self.strafe[0] += 1
		elif symbol == key.S:
			self.strafe[0] -= 1
		elif symbol == key.A:
			self.strafe[1] += 1
		elif symbol == key.D:
			self.strafe[1] -= 1
		elif symbol == key.SPACE:
			self.dy = 0.0 
		elif symbol == key.LCTRL:
			self.dy = 0.0
		elif symbol == key.F:  # only on release, prevent alltime switch
			self.fullScreen = not self.fullScreen
			self.set_fullscreen(fullscreen = self.fullScreen)
			self.set_exclusive_mouse(False)
			self.set_exclusive_mouse(True)
			
	def on_resize(self, width, height):
		""" Called when the window is resized to a new `width` and `height`.

		"""
		# label
		self.labelDict["worldInfo"].y = height - 10
		self.labelDict["focusedBlock"].y = 20
		
		# reticle
		if self.reticle:
			self.reticle.delete()
		
		x, y = self.width / 2, self.height / 2
		n = 10
		self.reticle = pyglet.graphics.vertex_list(4,
			('v2i', (x - n, y, x + n, y, x, y - n, x, y + n))
		)

	def set_2d(self):
		""" Configure OpenGL to draw in 2d.

		"""
		width, height = self.get_size()
		glDisable(GL_DEPTH_TEST)
		glViewport(0, 0, width, height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		glOrtho(0, width, 0, height, -1, 1)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()

	def set_3d(self):
		""" Configure OpenGL to draw in 3d.

		"""
		width, height = self.get_size()
		glEnable(GL_DEPTH_TEST)
		glViewport(0, 0, width, height)
		glMatrixMode(GL_PROJECTION)
		glLoadIdentity()
		#gluPerspective(45.0f,(GLfloat)width/(GLfloat)height,near distance,far distance);
		#gluPerspective(65.0, width / float(height), 0.1, 60.0)
		gluPerspective(65.0, width / float(height), 0.1, 6000.0)
		glMatrixMode(GL_MODELVIEW)
		glLoadIdentity()
		
		#glDepthMask(GL_FALSE)
		#drawSkybox()
		#glDepthMask(GL_TRUE)
		
		x, y = self.rotation
		#http://wiki.delphigl.com/index.php/glRotate
		#procedure glRotatef(angle: TGLfloat; x: TGLfloat; y: TGLfloat; z: TGLfloat); 
		glRotatef(x, 0, 1, 0)
		glRotatef(-y, math.cos(math.radians(x)), 0, math.sin(math.radians(x)))
		x, y, z = self.position
		glTranslatef(-x, -y, -z)

	def on_draw(self):
		""" Called by pyglet to draw the canvas.

		"""
		self.clear()
		self.set_3d()
		glColor3d(1, 1, 1)
		self.model.batch.draw()
		self.draw_focused_block()
		self.set_2d()
		self.draw_label()
		self.draw_reticle()

	def draw_focused_block(self):
		""" Draw black edges around the block that is currently under the
		crosshairs.

		"""
		vector = self.get_sight_vector()
		self.focusedBlock = self.model.hit_test(self.position, vector, EDIT_DISTANCE)[0]
		if self.focusedBlock:
			x, y, z = self.focusedBlock
			vertex_data = cube_vertices(x, y, z, CUBE_SIZE + 0.01)
			glColor3d(255, 255, 21)
			# white focus
			pyglet.graphics.draw(24, GL_QUADS, ('v3f/static', vertex_data))
			# borderlines
			glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
			glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
			

	def draw_label(self):
		""" Draw the label in the top left of the screen.

		"""
		x, y, z = self.position
		self.labelDict['worldInfo'].text = '%02d (%.2f, %.2f, %.2f) %d / %d' % (
			pyglet.clock.get_fps(), x, y, z,
			len(self.model._shown), len(self.model.world))
		self.labelDict['worldInfo'].draw()
		
		if self.renderWorld:
			self.labelDict['loabel'].draw()
			if self.mt.duration("renderWorld") >= 1.5:
				self.mt.stop("renderWorld")
				self.renderWorld = False
		
		#TODO: draw some notifications from self.model! 
		if self.model.notification:
			self.labelDict['notify'].text = self.model.notification
			self.labelDict['notify'].draw()
		
		if self.focusedBlock:
			self.labelDict['focusedBlock'].text = "x:{},y:{},z:{}".format(self.focusedBlock[0], self.focusedBlock[1], self.focusedBlock[2])
			self.labelDict['focusedBlock'].draw()
			

	def draw_reticle(self):
		""" Draw the crosshairs in the center of the screen.

		"""
		glColor3d(0, 0, 0)
		self.reticle.draw(GL_LINES)



def log(txt):
	print(time.strftime("%d-%m-%Y %H:%M:%S|", time.gmtime()) + str(txt) ) 


def setup():
	""" Basic OpenGL configuration.

	"""
	glClearColor(0.5, 0.69, 1.0, 1)
	glEnable(GL_CULL_FACE)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
	glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)


def main():
	window = Window(width=800, height=600, caption='DICraft', resizable=True)
	#window = Window(fullscreen=True, caption='DICraft')
	#window.set_exclusive_mouse(True)
	setup()
	pyglet.app.run()


if __name__ == '__main__':
	main()
