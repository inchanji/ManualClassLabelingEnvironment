from __future__ import absolute_import
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import *

def createActions(self):
	openShortcut 		= QShortcut(QKeySequence("Ctrl+o"), self)
	openShortcut.activated.connect(self.loadImage) 
	
	saveShortcut 		= QShortcut(QKeySequence("Ctrl+s"), self)
	saveShortcut.activated.connect(self.saveClsSegImage) 
	saveShortcut.activated.connect(self.saveObjSegImage) 

	zoominShortcut  	= QShortcut(QKeySequence("Ctrl+="), self)
	zoominShortcut.activated.connect(self.imgviewer.zoomIn) 

	zoomoutShortcut  	= QShortcut(QKeySequence("Ctrl+-"), self)
	zoomoutShortcut.activated.connect(self.imgviewer.zoomOut) 

	fitinShortcut  		= QShortcut(QKeySequence("Ctrl+0"), self)
	fitinShortcut.activated.connect(self.imgviewer.fitInView) 		

	cursorShortcut  	= QShortcut(QKeySequence("i"), self)
	cursorShortcut.activated.connect(self.switchInspectionMode) 	

	markPtShortcut  	= QShortcut(QKeySequence("m"), self)
	markPtShortcut.activated.connect(self.switchMarkPointMode) 

	fillMarkShortcut  	= QShortcut(QKeySequence("f"), self)
	fillMarkShortcut.activated.connect(self.fillInMarkPoint) 

	drawLineMarkShortcut  	= QShortcut(QKeySequence("l"), self)
	drawLineMarkShortcut.activated.connect(self.drawLinebtwMarkPoint) 

	fillLabelOnePixelShortcut  	= QShortcut(QKeySequence("p"), self)
	fillLabelOnePixelShortcut.activated.connect(self.switchFillPixelMode) 

	drawBoundaryShortcut  	= QShortcut(QKeySequence("b"), self)
	drawBoundaryShortcut.activated.connect(self.setSegBoundary) 	

	loadataSrhortcut  	= QShortcut(QKeySequence("Ctrl+l"), self)
	loadataSrhortcut.activated.connect(self.loadClassLabel)

	delattrShortcut  	= QShortcut(QKeySequence("Backspace"), self)
	delattrShortcut.activated.connect(self.imgviewer.delOneMarkPoint)

	resetShorcut 		= QShortcut(QKeySequence("Ctrl+r"), self)
	resetShorcut.activated.connect(self.resetImage)
	#resetShorcut.activated.connect(self.resetSegImage)

	decreaseClassLabelIdxShorcut	= QShortcut(QKeySequence("-"), self)
	decreaseClassLabelIdxShorcut.activated.connect(self.decreaseClassLabelIdx)

	increaseClassLabelIdxShorcut  = QShortcut(QKeySequence("="), self)
	increaseClassLabelIdxShorcut.activated.connect(self.increaseClassLabelIdx)

	closeShortcut  	= QShortcut(QKeySequence("Ctrl+w"), self)
	closeShortcut.activated.connect(self.Cancel)