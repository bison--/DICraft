# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'convert.ui'
#
# Created: Tue Jan 28 20:59:25 2014
#      by: PyQt4 UI code generator 4.9.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(265, 270)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setMaximumSize(QtCore.QSize(16777215, 270))
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.gridLayout = QtGui.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.txtDcm = QtGui.QLineEdit(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(100)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.txtDcm.sizePolicy().hasHeightForWidth())
        self.txtDcm.setSizePolicy(sizePolicy)
        self.txtDcm.setObjectName(_fromUtf8("txtDcm"))
        self.horizontalLayout_2.addWidget(self.txtDcm)
        self.cmdDcm = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmdDcm.sizePolicy().hasHeightForWidth())
        self.cmdDcm.setSizePolicy(sizePolicy)
        self.cmdDcm.setMinimumSize(QtCore.QSize(31, 27))
        self.cmdDcm.setMaximumSize(QtCore.QSize(31, 27))
        self.cmdDcm.setObjectName(_fromUtf8("cmdDcm"))
        self.horizontalLayout_2.addWidget(self.cmdDcm)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.txtTmp = QtGui.QLineEdit(self.centralwidget)
        self.txtTmp.setObjectName(_fromUtf8("txtTmp"))
        self.horizontalLayout_3.addWidget(self.txtTmp)
        self.cmdTmp = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmdTmp.sizePolicy().hasHeightForWidth())
        self.cmdTmp.setSizePolicy(sizePolicy)
        self.cmdTmp.setMinimumSize(QtCore.QSize(31, 27))
        self.cmdTmp.setMaximumSize(QtCore.QSize(31, 27))
        self.cmdTmp.setObjectName(_fromUtf8("cmdTmp"))
        self.horizontalLayout_3.addWidget(self.cmdTmp)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.gridLayout.addLayout(self.verticalLayout, 0, 0, 1, 1)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_2.addWidget(self.label_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.txtProject = QtGui.QLineEdit(self.centralwidget)
        self.txtProject.setObjectName(_fromUtf8("txtProject"))
        self.horizontalLayout.addWidget(self.txtProject)
        self.label_4 = QtGui.QLabel(self.centralwidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout.addWidget(self.label_4)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.gridLayout.addLayout(self.verticalLayout_2, 1, 0, 1, 1)
        self.cmdStart = QtGui.QPushButton(self.centralwidget)
        self.cmdStart.setObjectName(_fromUtf8("cmdStart"))
        self.gridLayout.addWidget(self.cmdStart, 2, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 265, 25))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Convert", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("MainWindow", "Folder with DICOM files:", None, QtGui.QApplication.UnicodeUTF8))
        self.txtDcm.setText(QtGui.QApplication.translate("MainWindow", "multiImageTest/", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdDcm.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("MainWindow", "TEMP folder:", None, QtGui.QApplication.UnicodeUTF8))
        self.txtTmp.setText(QtGui.QApplication.translate("MainWindow", "tmp/", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdTmp.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("MainWindow", "Project name:", None, QtGui.QApplication.UnicodeUTF8))
        self.txtProject.setText(QtGui.QApplication.translate("MainWindow", "testImage", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("MainWindow", ".sav", None, QtGui.QApplication.UnicodeUTF8))
        self.cmdStart.setText(QtGui.QApplication.translate("MainWindow", "START", None, QtGui.QApplication.UnicodeUTF8))


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    MainWindow = QtGui.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

