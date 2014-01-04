import time

class multiTimer(object):
	def __init__(self):
		self.timers = {}
	
	def start(self, tName):
		if tName in self.timers:
			self.timers[tName].reset()
		else:
			self.timers[tName] = timerObj(tName)
	
	def stop(self, tName):
		if tName in self.timers:
			return self.timers[tName].stop()
		else:
			print("TIMER '" + tName + "' WAS NOT STARTET!")
			return 0.0
	
	def duration(self, tName):
		if tName in self.timers:
			return self.timers[tName].getDuration()
		else:
			return 0.0
	
class timerObj(object):
	def __init__(self, name):
		self.name = name
		self.startTime = time.time()
		self.stopTime = 0.0
	
	def isRunning(self):
		return self.stopTime == 0.0
	
	def getDuration(self):
		if self.stopTime == 0.0:
			return time.time() - self.startTime
		else:
			return self.stopTime - self.startTime
	
	def reset(self):
		self.startTime = time.time()
		self.stopTime = 0.0
	
	def stop(self):
		self.stopTime = time.time()
		return self.getDuration()
	
