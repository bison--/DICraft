#!/usr/bin/env python

import sys
from PyQt4 import QtCore, QtGui
from gui.convertGui import *


class signalHandler(object):
	def __init__(self, ui):
		self._ui = ui
		QtCore.QObject.connect(self._ui.cmdDcm, QtCore.SIGNAL("clicked()"), self.cmdDcm_clicked)
		QtCore.QObject.connect(self._ui.cmdTmp, QtCore.SIGNAL("clicked()"), self.cmdTmp_clicked)
		QtCore.QObject.connect(self._ui.cmdStart, QtCore.SIGNAL("clicked()"), self.cmdStart_clicked)
		#print dir(self._ui.cmdStart)
		
	def cmdDcm_clicked(self):
		#http://zetcode.com/gui/pyqt4/german/dialogs/
		#res = str(QFileDialog.getExistingDirectory(self, 'Choose Save Directory', settings.save_dir))
		# local_folder_path = QFileDialog.getExistingDirectory(self.manager_widget, QString("Select Download Folder"), QString(self.last_dl_location), QFileDialog.ShowDirsOnly|QFileDialog.HideNameFilterDetails|QFileDialog.ReadOnly)
		#print dir(self._ui.txtDcm)
		#print self._ui.txtDcm.text()
		dirName = str(QtGui.QFileDialog.getExistingDirectory(None, "Select Directory with DCM files", self._ui.txtDcm.text()))
		self._ui.txtDcm.setText(dirName)
		
	def cmdTmp_clicked(self):
		dirName = str(QtGui.QFileDialog.getExistingDirectory(None, "Select Directory for temporary converted files", self._ui.txtTmp.text()))
		self._ui.txtTmp.setText(dirName)
		
		
	def runScript(self, parList):
		print "COMMANDS:", parList
		from subprocess import Popen, PIPE
		import time
		proc = Popen(parList, stdout=PIPE, stderr=PIPE)
		retcode = None
		
		while not retcode:
			retcode = proc.poll()
			if retcode is not None: # Process finished.
				#running_procs.remove(proc)
				break
			else: # No process is done, wait a bit and check again.
				time.sleep(0.1)
				continue
		 	tmp = proc.stdout.read()
		 	if tmp != "" and tmp.contains("\n"):
		 		print tmp
		 		
		print proc.stdout.read()
		
		# Here, `proc` has finished with return code `retcode`
		if retcode != 0:
			"""Error handling."""
			print "ERROR"
			return False
		else:
			return True
		#handle_results(proc.stdout)
		
	def cmdStart_clicked(self):
		#http://helloacm.com/execute-external-programs-the-python-ways/
		self._ui.cmdStart.setDisabled(True)
		#python convert.py multiImageTest/
		self.runScript(['python', 'convert.py', self._ui.txtDcm.text(), self._ui.txtTmp.text()])
		#python dcm2save.py tmp/ savefile=roflcopter.sav
		self.runScript(['python', 'dcm2save.py', self._ui.txtTmp.text(), "savefile=" + self._ui.txtProject.text() + ".sav"])
		self._ui.cmdStart.setDisabled(False)
		
app = QtGui.QApplication(sys.argv)
MainWindow = QtGui.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

sh = signalHandler(ui)

MainWindow.show()
sys.exit(app.exec_())
