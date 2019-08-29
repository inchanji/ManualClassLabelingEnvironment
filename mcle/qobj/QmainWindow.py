from __future__ import absolute_import
import ntpath
import numpy as np
import os
from PIL import ImageQt, Image
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from PyQt5.QtPrintSupport import *
from qobj.qmainViewers import * 
from src.config import configLayout
from src.action import createActions
from src.handleLabel import loadClassLabel
from src.image import loadImage, BndryLabelValue

def getIcon(path):
	app_icon = QIcon()
	app_icon.addFile(path + '16x16.png',   QSize(16,16))
	app_icon.addFile(path + '24x24.png',   QSize(24,24))
	app_icon.addFile(path + '32x32.png',   QSize(32,32))
	app_icon.addFile(path + '48x48.png',   QSize(48,48))
	app_icon.addFile(path + '256x256.png', QSize(256,256))

	return app_icon


class QMainWindow(QWidget):
	QInputClassLabel = pyqtSignal(int)
	QLoadClassLabels = pyqtSignal(str)

	def __init__(self):
		super(QMainWindow, self).__init__()

		self.initialize()

		# main layout 			
		self.imgviewer			= PhotoViewer(self)
		self.segviewer 			= SegViewer(self)

		self.configLayout()
		self.createActions()
		self.loadClassLabel()

		self.setGeometry(0, 0, 1200, 600)
		self.setMinimumSize(1000, 600)
		self.setMaximumSize(2000, 1500)
		self.setWindowTitle('Manual Class Labeling Environment')
		
		self.imgviewer.emitMouseOnPhoto.connect(self.updateImageInfo)
		self.imgviewer.emitClassLabelPos.connect(self.setClassLabelPos)
		self.imgviewer.emitClassLabelIdx.connect(self.setClassLabelIdx)

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

	def resetImage(self):
		if self.qImage0 is not None:
			self.imgviewer.resetImage()
			self.resetSegImage()

	def setClassLabelLineWidth(self, val = None):
		self.imgviewer.setClassLabelLineWidth(val)

	def setSegBndryThickness(self, val = None):
		self.segviewer.setSegBndryThickness(val)		

	def setSegBoundary(self):
		if self.imgviewer.askQuestion('Are you sure to proceed ?'):
			labelpos = self.imgviewer.ClassLabelPixPos
			self.imgviewer.setSegBndry(self.segviewer.setSegBndry(labelpos))

	def delOneMarkPoint(self):
		self.imgviewer.delOneMarkPoint()

	def fillInMarkPoint(self):
		self.imgviewer.fillInMarkPoint()


	def saveImage(self):
		self.segviewer.saveSegMap(self.savePath.text())

	def updateImageInfo(self, pos = None):
		if pos is not None:
			txt  = '[Image name] {:s}'.format(ntpath.basename(self.imagePath.text())) + '\n'
			txt += '[Image size] {:4d}×{:4d}\n'.format(self.imgWidth, self.imgHeight)
			txt += '[Mouse posistion] ({:4d}, {:4d})'.format(pos.x(), pos.y()) + '\n'
			self.viewInfo.setText(txt) 


	def selectClassLbl(self, idx = None):
		self.QInputClassLabel.emit(idx)


	def setClassLabelIdx(self, idx = None):
		if idx is not None:
			self.classLabelIdx = idx

	def setClassLabelPos(self, pos = None):
		if (pos is not None) and (self.classLabelIdx is not None):
			self.segviewer.setClassLabel(pos, self.classLabelIdx)
		else:
			print('either pos or classLabelIdx is None')

	def resetSegImage(self):
		qsegmap = QPixmap(self.imgWidth, self.imgHeight)
		qsegmap.fill(Qt.black)
		self.segviewer.setPhoto(qsegmap)
		print('resetSegImage')		


	def loadFileSystem(self):
		#self.fileview.setRootPath(self.fsPath.text())
		fileviewdir = QDir(self.fsPath.text())
		root = self.fileview.setRootPath(fileviewdir.path())
		self.treeView.setRootIndex(root)
		#self.fileview.setFilter(QDir.NoDotAndDotDot | QDir.Files)

	def loadFileSystemItem(self, index):
		path = self.sender().model().filePath(index)
		self.imagePath.setText(path)
		self.loadImage()
		#print('loadFileSystemItem:', path) 


	def setClassLabelQList(self, qmodelidx):
		#print(qmodelidx.row())
		self.classLabelIdx = qmodelidx.row()
		self.QLEselectLbl.setValue(self.classLabelIdx)
		self.QLEselectLbl.valueChanged.connect(self.selectClassLbl)		
		self.QInputClassLabel.emit(self.QLEselectLbl.value())	


	def increaseClassLabelIdx(self):
		if self.classLabelIdx is None:
			self.classLabelIdx = 0
		elif self.classLabelIdx < self.NClassLabel - 1:
			self.classLabelIdx += 1

		self.QLEselectLbl.setValue(self.classLabelIdx)
		self.QLEselectLbl.valueChanged.connect(self.selectClassLbl)		
		self.QInputClassLabel.emit(self.QLEselectLbl.value())	

	def decreaseClassLabelIdx(self):
		if self.classLabelIdx is None:
			self.classLabelIdx = 0
		elif self.classLabelIdx > 0:
			self.classLabelIdx -= 1

		self.QLEselectLbl.setValue(self.classLabelIdx)
		self.QLEselectLbl.valueChanged.connect(self.selectClassLbl)		
		self.QInputClassLabel.emit(self.QLEselectLbl.value())


	def loadRetrieveClassLable(self, path):
		fn = lambda x: self.Nclasslbl-1 if x == BndryLabelValue else x
		print('loadRetrieveClassLable:', path)
		segload 	= np.array(Image.open(path))
		nrow, ncol 	= np.shape(segload)
		labels 		= []
		pos 		= []
		for i in range(nrow):
			for j in range(ncol):
				val = segload[i,j]
				if  val != 0:
					labels.append(fn(val))
					pos.append([i,j])
					self.imgviewer.ClassLabelPixPos[fn(val)].append([i,j])

		self.imgviewer.loadSegClassLabel(labels, pos)
		self.segviewer.loadSegClassLabel(labels, pos)

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



def initialize(self):
	self.Nchannel 			= 3
	self.readytoMark 		= False
	self.qImage0 			= None
	self.PWD 				= os.getcwd()
	self.imagePath0 		= self.PWD + '/image/rock-austin.jpg'
	self.classLabelPath0 	= self.PWD + '/CLASSLABEL'
	self.featureBase 		= '*** Class Segmentation Maker (by Inchan Ji)***\n' +  '[No.] [Class label] [RGB 0-255]\n'
	self.Nclasslbl 			= None
	self.classlbl 			= ''
	self.extfilters 		= iter(('*.jpeg','*.jpg','*.png','*.bmp'))
