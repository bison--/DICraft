#!/usr/bin/env python

import sys, os
from PyQt4 import QtCore, QtGui
from gui.convertGui import *


class signalHandler(object):
	def __init__(self, ui):
		self.tmpPath = "tmp/"
	
		self._ui = ui
		QtCore.QObject.connect(self._ui.cmdDcm, QtCore.SIGNAL("clicked()"), self.cmdDcm_clicked)
		#QtCore.QObject.connect(self._ui.cmdTmp, QtCore.SIGNAL("clicked()"), self.cmdTmp_clicked)
		QtCore.QObject.connect(self._ui.cmdStartConvert, QtCore.SIGNAL("clicked()"), self.cmdStartConvert_clicked)
		QtCore.QObject.connect(self._ui.cmdStartToSave, QtCore.SIGNAL("clicked()"), self.cmdStartToSave_clicked)
		QtCore.QObject.connect(self._ui.cmdStartEditor, QtCore.SIGNAL("clicked()"), self.cmdStartEditor_clicked)
		#QtCore.QObject.connect(self._ui.txtDcm, QtCore.SIGNAL("textChanged(QString)"), Label, SLOT("setText(QString)"))
		QtCore.QObject.connect(self._ui.txtDcm, QtCore.SIGNAL("textChanged(QString)"), self.txt_changed)
		#QtCore.QObject.connect(self._ui.txtTmp, QtCore.SIGNAL("textChanged(QString)"), self.txt_changed)
		QtCore.QObject.connect(self._ui.txtProject, QtCore.SIGNAL("textChanged(QString)"), self.txt_changed)
		#print dir(self._ui.cmdStart)
		
		QtCore.QObject.connect(self._ui.nutMinGray, QtCore.SIGNAL("valueChanged(int)"), self.nutMinGray_changed)
		QtCore.QObject.connect(self._ui.sldMinGray, QtCore.SIGNAL("valueChanged(int)"), self.sldMinGray_changed)
		QtCore.QObject.connect(self._ui.nutMaxGray, QtCore.SIGNAL("valueChanged(int)"), self.nutMaxGray_changed)
		QtCore.QObject.connect(self._ui.sldMaxGray, QtCore.SIGNAL("valueChanged(int)"), self.sldMaxGray_changed)
		
		#spinbox set range: .setRange(0,100)
		
		self.reFreshProjects()
		self.checkInputErrors()
		
	def cmdDcm_clicked(self):
		#http://zetcode.com/gui/pyqt4/german/dialogs/
		#res = str(QFileDialog.getExistingDirectory(self, 'Choose Save Directory', settings.save_dir))
		# local_folder_path = QFileDialog.getExistingDirectory(self.manager_widget, QString("Select Download Folder"), QString(self.last_dl_location), QFileDialog.ShowDirsOnly|QFileDialog.HideNameFilterDetails|QFileDialog.ReadOnly)
		#print dir(self._ui.txtDcm)
		#print self._ui.txtDcm.text()
		dirName = str(QtGui.QFileDialog.getExistingDirectory(None, "Select Directory with DCM files", self._ui.txtDcm.text()))
		self._ui.txtDcm.setText(dirName)
		
	def runScript(self, parList):
		print("COMMANDS:", parList)
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

			tmp += proc.stdout.read(1)
			if tmp != "" and tmp.contains("\n"):
				print(tmp)
				tmp = ""

		print(proc.stdout.read())

		# Here, `proc` has finished with return code `retcode`
		if retcode != 0:
			"""Error handling."""
			print("ERROR")
			return False
		else:
			return True
		#handle_results(proc.stdout)
	
	def txt_changed(self, txt):
		self.checkInputErrors()
		
	def checkInputErrors(self):
		self._dirExist(self._ui.txtDcm)
		#self._dirExist(self._ui.txtTmp)
		self._fileExist(self._ui.txtProject)
	
	def nutMinGray_changed(self):
		self.minMaxVal_changed("nutMinGray")
	
	def sldMinGray_changed(self):
		self.minMaxVal_changed("sldMinGray")

	def nutMaxGray_changed(self):
		self.minMaxVal_changed("nutMaxGray")
	
	def sldMaxGray_changed(self):
		self.minMaxVal_changed("sldMaxGray")
		
	def minMaxVal_changed(self, name):
		if self._ui.sldMinGray.value() != self._ui.nutMinGray.value():
			if name == "nutMinGray":
				self._ui.sldMinGray.setValue(self._ui.nutMinGray.value())
			elif name == "sldMinGray":	
				self._ui.nutMinGray.setValue(self._ui.sldMinGray.value())
		elif self._ui.sldMaxGray.value() != self._ui.nutMaxGray.value():
			if name == "nutMaxGray":
				self._ui.sldMaxGray.setValue(self._ui.nutMaxGray.value())
			elif name == "sldMaxGray":	
				self._ui.nutMaxGray.setValue(self._ui.sldMaxGray.value())
	
	def _dirExist(self, lineEdit):
		if os.path.isdir(lineEdit.text()):
			lineEdit.setStyleSheet("QLineEdit {background-color: white;}")
		else:
			lineEdit.setStyleSheet("QLineEdit {background-color: salmon;}")					
	
	def _fileExist(self, lineEdit):
		saveFilePath = "saves/" + lineEdit.text() + ".sav"
		if not os.path.isdir(saveFilePath) and not os.path.exists(saveFilePath):
			lineEdit.setStyleSheet("QLineEdit {background-color: white;}")
		else:
			lineEdit.setStyleSheet("QLineEdit {background-color: yellow;}")					
	
	def cmdStartConvert_clicked(self):
		#http://helloacm.com/execute-external-programs-the-python-ways/
		self._ui.cmdStartConvert.setDisabled(True)
		#python convert.py multiImageTest/
		self.runScript(['python', 'convert.py', self._ui.txtDcm.text(), self.tmpPath])
		#python dcm2save.py tmp/ savefile=roflcopter.sav
		#self.runScript(['python', 'dcm2save.py', self.tmpPath, "savefile=" + self._ui.txtProject.text() + ".sav"])
		self._ui.cmdStartConvert.setDisabled(False)
		
	def cmdStartToSave_clicked(self):
		self._ui.cmdStartToSave.setDisabled(True)
		self.runScript(['python', 'dcm2save.py',
			self.tmpPath,
			"savefile=" + self._ui.txtProject.text() + ".sav",
			"minVal=" + str(self._ui.nutMinGray.value()),
			"maxVal=" + str(self._ui.nutMaxGray.value())
			])
		self._ui.cmdStartToSave.setDisabled(False)
		self.reFreshProjects()
		
	def cmdStartEditor_clicked(self):
		self._ui.cmdStartEditor.setDisabled(True)
		#self._ui.chkRemoveVoluminas.isChecked()
		#nutRemoveVoluminas.value()
		params = ['python', 'DICraft.py', "savefile=" + str(self._ui.cmbProjects.currentText())]
		if self._ui.chkRemoveVoluminas.isChecked():
			params.append("rmVol=" + str(self._ui.nutRemoveVoluminas.value()))
		
		if self._ui.chkFillCavities.isChecked():
			params.append("fillCavities")
		
		self.runScript(params)
		self._ui.cmdStartEditor.setDisabled(False)
		
	def reFreshProjects(self):
		self._ui.cmbProjects.clear()
		dirList = os.listdir("saves/")
		dirList.sort()
		for fname in dirList:
			if fname.endswith(".sav"):
				self._ui.cmbProjects.addItem(fname, fname) # text, "index"
		
		index = self._ui.cmbProjects.findData(self._ui.txtProject.text() + ".sav")
		self._ui.cmbProjects.setCurrentIndex(index)
		
app = QtGui.QApplication(sys.argv)
MainWindow = QtGui.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)

sh = signalHandler(ui)

MainWindow.show()
sys.exit(app.exec_())
