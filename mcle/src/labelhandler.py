from __future__ import absolute_import
import os
import numpy as np 
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from src.image import IntToRGB, rgbColorSchemeLabel, BndryLabelName, RGBAtoInt

def loadClassLabel(self):
	print('Load Class Labels: ', self.classLabelPath.text())

	if not os.path.isfile(self.classLabelPath.text()):
		print('cannot load class labels. no such file.')
		return

	classLabel0  		= np.array([line.split('\n')[0] for line in open(self.classLabelPath.text())])
	txtUpdate 			= self.featureBase
	inputClassLabels 	= ''

	classLabel 			= []

	for clbl in classLabel0:
		if clbl.split()[0] == 'LABEL':
			classLabel.append(clbl.split()[1])
	classLabel.append(BndryLabelName)


	Nclasslbl = len(classLabel)
	self.classSegViewer.setNumClassLabel(Nclasslbl)

	for i, inline in enumerate(classLabel):
		rgba = IntToRGB(rgbColorSchemeLabel(i, Nclasslbl))
	
		txtUpdate +=  '[{:3d}] [{:s}] [{:d},{:d},{:d}]\n'.format(i, inline, rgba[0], rgba[1], rgba[2])
		self.QListClassLabel.addItem('[{:3d}] [{:s}]'.format(i, inline))
		self.QListClassLabel.item(i).setBackground(QColor(rgba[0], rgba[1], rgba[2]))
		if (rgba[0] < 50) and (rgba[1] < 50) and (rgba[2] < 50):
			self.QListClassLabel.item(i).setForeground(QColor(255,255,255))

		if i < len(classLabel)-1:
			inputClassLabels += inline + ',' + str(rgba[0]) + ',' +  str(rgba[1]) + ',' +  str(rgba[2]) + '\t'
		else:
			inputClassLabels += inline + ',' + str(rgba[0]) + ',' +  str(rgba[1]) + ',' +  str(rgba[2]) 

	txtUpdate += '\n'
	txtUpdate += 'Ready to mark class labels :)))\n'
	txtUpdate += '-' * 50

	self.classLabelInfo.setText(txtUpdate)
	self.classLabelInfo.adjustSize()		
	self.readytoMark = True

	self.QLoadClassLabels.emit(inputClassLabels)		
	self.classLabelIdxSelected 		= None
	self.classLabelQPosSelected 	= None
	self.listClassLabel 			= classLabel.copy()
	
	self.Nclasslbl 					= Nclasslbl
	self.clsObjHandler.NClassLabel 	= Nclasslbl

	self.QLEselectLbl.setMaximum(self.Nclasslbl-1)
	self.QListClassLabel.clicked.connect(self.setClassLabelQList)

