from __future__ import absolute_import
import ntpath
import numpy as np
import os
from PIL import ImageQt, Image
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from qobj.qImgViewer import * 
from qobj.qClassSegViewer import *
from qobj.qObjectSegViewer import *
from src.config import configLayout
from src.action import createActions
from src.labelhandler import loadClassLabel
from src.image import loadImage, BndryLabelValue
from src.clsobjhandler import *

def getIcon(path):
	app_icon = QIcon()
	app_icon.addFile(os.path.join(path, '16x16.png'),   QSize(16,16))
	app_icon.addFile(os.path.join(path, '24x24.png'),   QSize(24,24))
	app_icon.addFile(os.path.join(path, '32x32.png'),   QSize(32,32))
	app_icon.addFile(os.path.join(path, '48x48.png'),   QSize(48,48))
	app_icon.addFile(os.path.join(path, '256x256.png'), QSize(256,256))
	return app_icon

class QMainWindow(QWidget):
	QInputClassLabel = pyqtSignal(int)
	QLoadClassLabels = pyqtSignal(str)

	def __init__(self):
		super(QMainWindow, self).__init__()

		self.initialize()

		# main layout 			
		self.imgviewer			= PhotoViewer(self)
		self.classSegViewer 	= ClassSegViewer(self)
		self.objectSegViewer 	= ObjectSegViewer(self)

		self.configLayout()
		self.createActions()
		self.loadClassLabel()

		self.setGeometry(100, 100, 1048, 640)
		self.setMinimumSize(1000, 600)
		self.setMaximumSize(2000, 1500)
		self.setWindowTitle('Manual Class Labeling Environment')
		
		self.imgviewer.emitMouseOnPhoto.connect(self.updateImageInfo)
		self.imgviewer.emitClassLabelPos.connect(self.setClassLabelPos)
		self.imgviewer.emitClassLabelIdx.connect(self.setClassLabelIdx)
		self.clsObjHandler.emitClassObjectIdx.connect(self.getClassObjectIdx)
		self.clsObjHandler.emitClassObjectPos.connect(self.getClassObjectPos)
		self.clsObjHandler.emitFillClassObject.connect(self.updateClassObject)
		self.clsObjHandler.emitKillClassObject.connect(self.removeClassObjectPos)

	def initialize(self):
		initialize(self)

	def configLayout(self):
		configLayout(self)

	def createActions(self):
		createActions(self)

	def loadClassLabel(self):
		loadClassLabel(self)

	def loadImage(self):
		loadImage(self)

	def switchInspectionMode(self):
		self.imgviewer.switchInspectionMode()

	def switchMarkPointMode(self):
		self.imgviewer.switchMarkPointMode()

	def switchFillPixelMode(self):
		self.imgviewer.switchFillPixelMode()

	def drawLinebtwMarkPoint(self):
		self.imgviewer.drawLinebtwMarkPoint()

	def resetImage(self):
		if self.qImage0 is not None:
			self.imgviewer.resetImage()
			self.resetSegImages()
			self.clsObjHandler.reset()

	def setClassLabelLineWidth(self, val = None):
		self.imgviewer.setClassLabelLineWidth(val)

	def setSegBndryThickness(self, val = None):
		self.classSegViewer.setSegBndryThickness(val)		

	def setSegBoundary(self):
		if self.imgviewer.askQuestion('Are you sure to proceed ?'):
			self.setClassLabelQList(self.NClassLabel - 1)
			idx 	 = self.classLabelIdxSelected
			labelpos = self.clsObjHandler.getClassLabelPixPos(self.NClassLabel)
			bndrypos = self.classSegViewer.setSegBndry(labelpos)
			self.imgviewer.setSegBndry(bndrypos)
			self.setClassLabelQList(idx)

	def delOneMarkPoint(self):
		self.imgviewer.delOneMarkPoint()

	def fillInMarkPoint(self):
		self.imgviewer.fillInMarkPoint()

	def saveClsSegImage(self):
		self.classSegViewer.saveSegMap(self.saveClsSegPath.text())

	def saveObjSegImage(self):
		self.objectSegViewer.saveSegMap(self.saveObjSegPath.text())

	def updateImageInfo(self, pos = None):
		if pos is not None:
			txt  = '[Image name] {:s}'.format(ntpath.basename(self.imagePath.text())) + '\n'
			txt += '[Image size] {:4d}×{:4d}\n'.format(self.imgWidth, self.imgHeight)
			txt += '[Mouse posistion] ({:4d}, {:4d})'.format(pos.x(), pos.y()) + '\n'
			self.viewInfo.setText(txt) 

	def selectClassLbl(self, idx = None):
		self.QInputClassLabel.emit(idx)

	def selectObjClsLbl(self, idx = None):
		self.clsObjHandler.clsObjIdxSelected = idx

	def setClassLabelIdx(self, idx = None):
		if idx is not None:
			self.classLabelIdxSelected = idx

	def setClassLabelPos(self, pos = None):
		if (pos is not None) and (self.classLabelIdxSelected is not None):
			self.classSegViewer.setClassLabel(pos, self.classLabelIdxSelected)
			self.classLabelQPosSelected = pos.copy()
		else:
			print('either pos or classLabelIdx is None')

		if (pos is not None) and (self.clsObjHandler.clsObjIdxSelected is not None):
			if self.classLabelIdxSelected < self.Nclasslbl-1:
				self.objectSegViewer.fillClassObject(self.clsObjHandler.clsObjIdxSelected, pos)
			else:
				self.objectSegViewer.setSegBndry(pos)

	def resetSegImages(self):
		qsegmap = QPixmap(self.imgWidth, self.imgHeight)
		qsegmap.fill(Qt.black)
		self.classSegViewer.setPhoto(qsegmap)
		self.objectSegViewer.setPhoto(qsegmap)
		print('reset Seg Images')		

	def loadFileSystem(self):
		fileviewdir = QDir(self.fsPath.text())
		root = self.fileSysview.setRootPath(fileviewdir.path())
		self.fileSysTreeView.setRootIndex(root)

	def loadFileSystemItem(self, index):
		path = self.sender().model().filePath(index)
		self.imagePath.setText(path)
		self.loadImage()
		#print('loadFileSystemItem:', path) 

	def setClassLabelQList(self, qmodelidx):
		#print(qmodelidx.row())
		if type(qmodelidx) == int:
			self.classLabelIdxSelected = qmodelidx
		else:
			self.classLabelIdxSelected = qmodelidx.row()
		self.QLEselectLbl.setValue(self.classLabelIdxSelected)
		self.QLEselectLbl.valueChanged.connect(self.selectClassLbl)		
		self.QInputClassLabel.emit(self.QLEselectLbl.value())	


	def increaseClassLabelIdx(self):
		if self.classLabelIdxSelected is None:
			self.classLabelIdxSelected = 0
		elif self.classLabelIdxSelected < self.NClassLabel - 1:
			self.classLabelIdxSelected += 1

		self.QLEselectLbl.setValue(self.classLabelIdxSelected)
		self.QLEselectLbl.valueChanged.connect(self.selectClassLbl)		
		self.QInputClassLabel.emit(self.QLEselectLbl.value())	

	def decreaseClassLabelIdx(self):
		if self.classLabelIdxSelected is None:
			self.classLabelIdxSelected = 0
		elif self.classLabelIdxSelected > 0:
			self.classLabelIdxSelected -= 1

		self.QLEselectLbl.setValue(self.classLabelIdxSelected)
		self.QLEselectLbl.valueChanged.connect(self.selectClassLbl)		
		self.QInputClassLabel.emit(self.QLEselectLbl.value())


	def Cancel(self):
		self.close()

	def closeEvent(self, event):
		msgbox 	= QMessageBox()
		msgbox.setIcon(QMessageBox.Question)
		reply 	= msgbox.question(self, "",
									"Are you sure to close window ?", 
									QMessageBox.No | QMessageBox.Yes , QMessageBox.No)
		if reply == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()

	def addObjClass(self, name = None):
		validLabel = True
		if name == None: # Filled Area with Class Label
			try: 
				labelstr 	= self.listClassLabel[self.classLabelIdxSelected] + '_' + str(self.clsObjHandler.NclsObj)
				if self.classLabelIdxSelected == 0:  # ignore background when adding item to class object list
					validLabel = False
			except:
				validLabel 	= False
		else:
			labelstr = name
			
		if not(validLabel): return

		qpos 	 = self.classLabelQPosSelected
		self.clsObjHandler.addClsObj(self.classLabelIdxSelected, labelstr, qpos)

	def addBndryClass(self, name = None):
		print('addBndryClass')
		qpos 	 = self.classLabelQPosSelected
		self.clsObjHandler.addClsObj(self.classLabelIdxSelected, name, qpos)

	def getClassObjectIdx(self, idx = None):
		self.objectSegViewer.clsObjIdx = idx

	def getClassObjectPos(self, pos = None):
		self.objectSegViewer.clsObjPos = pos

	def updateClassObject(self, enable = None):
		if enable:
			idx = self.objectSegViewer.clsObjIdx
			pos = self.objectSegViewer.clsObjPos
			self.objectSegViewer.fillClassObject(idx, pos)

	def removeClassObjectPos(self, qpos = None):
		if qpos != None:
			self.imgviewer.removeClassLabel(qpos)
			self.classSegViewer.removeClassLabel(qpos)
			self.objectSegViewer.removeClassLabel(qpos)
			#self.objectSegViewer.fillClassObject(idx, pos)

def initialize(self):
	self.Nchannel 			= 3
	self.readytoMark 		= False
	self.qImage0 			= None
	self.PWD 				= os.getcwd()
	self.imagePath0 		= os.path.join(self.PWD, 'image', 'rock-austin.jpg')
	self.classLabelPath0 	= os.path.join(self.PWD , 'CLASSLABEL')
	self.featureBase 		= '*** Class Segmentation Maker (by Inchan Ji)***\n' +  '[No.] [Class label] [RGB 0-255]\n'
	self.Nclasslbl 			= None
	self.classlbl 			= ''
	self.extfilters 		= iter(('*.jpeg','*.jpg','*.png','*.bmp'))

