from __future__ import absolute_import
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import *

BTN_MIN_WIDTH 		= 100
BTN_MAX_WIDTH 		= 200
ICON_MIN_WIDTH 		= 30
ICON_MIN_HEIGHT 	= 30

def configLayout(self):
	# Feature layout

	# Edit widget	
	HBlayoutEdits 			= setLayoutEdit(self)

	# View widget
	HBlayoutView 			= setLayoutView(self)

	# Load Class label layout
	HBlayoutLoadClassLbl 	= setLayoutLoadClassLabel(self)

	# Select Class label layout
	HBlayoutSelectClassLabel = setLayoutSelectClassLabel(self)
	
	# Class Label Info layout
	QScrollClassLblInfo 	= setLayoutQScrollClassLblInfo(self)

	# 'Open image' button
	HBlayoutOpenImage 		= setLayoutOpenImage(self)

	# 'Save image' button
	HBlayoutSaveImage 		= setLayoutSaveImage(self)

	# 'Image Info' widget
	HBlayoutImageInfo 		= setLayoutImageInfo(self)

	# File System Widget
	#VBlayoutFileView 		= setLayoutFileView(self)
	VBlayoutFileView = setLayoutFileViewLabelView(self)

	# Arrange all layout classes # 
	# Main layout
	LayoutMain 				= QVBoxLayout(self) # with "self", it becomes MAIN layout
	LayoutMain.setAlignment(Qt.AlignTop)


	# layout for buttons here!
	HLayoutMain     = QHBoxLayout() 
	HLayoutMain.setAlignment(Qt.AlignLeft)

	#
	LayoutMainView = QVBoxLayout()   
	LayoutMainView.setAlignment(Qt.AlignLeft)

	# (View + Info) widgets 
	HBlayoutViewMain = QHBoxLayout() 
	HBlayoutViewMain.setAlignment(Qt.AlignCenter)


	# ViewInfo widget layout
	VBlayoutViewInfo = QVBoxLayout() 
	VBlayoutViewInfo.setAlignment(Qt.AlignTop)
	VBlayoutViewInfo.addLayout(HBlayoutLoadClassLbl)
	VBlayoutViewInfo.addLayout(HBlayoutSelectClassLabel)
	VBlayoutViewInfo.addWidget(QScrollClassLblInfo)


	HBlayoutViewMain.addLayout(HBlayoutView) 
	
	# Load/Save images widget layout

	HBlayoutMain = QHBoxLayout()
	HBlayoutMain.setAlignment(Qt.AlignCenter)

	# VBox including Load + Save + Status
	VBlayoutLSS = QVBoxLayout()
	VBlayoutLSS.setAlignment(Qt.AlignLeft)
	VBlayoutLSS.addLayout(HBlayoutOpenImage)
	VBlayoutLSS.addLayout(HBlayoutSaveImage)
	VBlayoutLSS.addLayout(HBlayoutImageInfo)


	# HBlayoutMain
	HBlayoutMain.addLayout(VBlayoutLSS)
	HBlayoutMain.addLayout(VBlayoutViewInfo)

	# Main View widget layout
	LayoutMainView.addLayout(HBlayoutViewMain, 8)
	LayoutMainView.addLayout(HBlayoutMain,     2)

	HLayoutMain.addLayout(LayoutMainView,  8)
	HLayoutMain.addLayout(VBlayoutFileView,2)


	LayoutMain.addLayout(HBlayoutEdits)
	LayoutMain.addLayout(HLayoutMain)




def setLayoutEdit(self):
	HBlayoutEdits = QHBoxLayout() 
	HBlayoutEdits.setAlignment(Qt.AlignLeft)

	BtnInspect = QPushButton()
	BtnInspect.setIcon(QIcon(self.PWD+'/res/magnifying_glass.png'))
	BtnInspect.setText('I')
	BtnInspect.setMinimumWidth(ICON_MIN_WIDTH)
	BtnInspect.setMinimumHeight(ICON_MIN_HEIGHT)
	BtnInspect.clicked.connect(self.switchInspectionMode)
	BtnInspect.setToolTip('Image/pixel Inspection')

	BtnMarkPoint = QPushButton()
	BtnMarkPoint.setIcon(QIcon(self.PWD+'/res/pin.png'))
	BtnMarkPoint.setText('M')
	BtnMarkPoint.setMinimumWidth(ICON_MIN_WIDTH)
	BtnMarkPoint.setMinimumHeight(ICON_MIN_HEIGHT)
	BtnMarkPoint.clicked.connect(self.switchMarkPointMode)
	BtnMarkPoint.setToolTip('Pixel Marker of Class Label')

	BtnReset = QPushButton()
	BtnReset.setIcon(QIcon('res/reset.png'))
	BtnReset.setText(u"\u2318" + "R")
	BtnReset.setMinimumWidth(ICON_MIN_WIDTH)
	BtnReset.setMinimumHeight(ICON_MIN_HEIGHT)	
	BtnReset.clicked.connect(self.resetImage)
	BtnReset.setToolTip('Reset All')

	BtnGoBack = QPushButton()
	BtnGoBack.setIcon(QIcon(self.PWD+'/res/left_arrow.png'))
	BtnGoBack.setText(u"\u232B")
	BtnGoBack.setMinimumWidth(ICON_MIN_WIDTH)
	BtnGoBack.setMinimumHeight(ICON_MIN_HEIGHT)	
	BtnGoBack.clicked.connect(self.delOneMarkPoint)
	BtnGoBack.setToolTip('Go One Step Back (Pixel Marker)')

	BtnFillLabelOnePixel = QPushButton()
	BtnFillLabelOnePixel.setIcon(QIcon(self.PWD+'/res/dropper.png'))
	BtnFillLabelOnePixel.setText("P")
	BtnFillLabelOnePixel.setMinimumWidth(ICON_MIN_WIDTH)
	BtnFillLabelOnePixel.setMinimumHeight(ICON_MIN_HEIGHT)	
	BtnFillLabelOnePixel.clicked.connect(self.switchFillPixelMode)
	BtnFillLabelOnePixel.setToolTip('Fill Class Label in One Pixel')


	BtnDrawLineBtwPoints = QPushButton()
	BtnDrawLineBtwPoints.setIcon(QIcon(self.PWD+'/res/line.png'))
	BtnDrawLineBtwPoints.setText('L')
	BtnDrawLineBtwPoints.setMinimumWidth(ICON_MIN_WIDTH)
	BtnDrawLineBtwPoints.setMinimumHeight(ICON_MIN_HEIGHT)	
	#BtnDrawLineBtwPoints.clicked.connect(self.drawLinebtwMarkPoint)
	BtnDrawLineBtwPoints.setToolTip('Finish Marking Points and Draw Lines of Class Labels between Marked Points')

	SBScaleLineWidth = QSpinBox()
	SBScaleLineWidth.setMinimum(1)
	SBScaleLineWidth.valueChanged.connect(self.setClassLabelLineWidth)
	SBScaleLineWidth.setToolTip('Set line width')
	#SBScaleLineWidth.setContentsMargins(-10,0,0,0)
	#print('contentsMargins(): ',SBScaleLineWidth.getContentsMargins())

	BtnFillInsidePoints = QPushButton()
	BtnFillInsidePoints.setIcon(QIcon(self.PWD+'/res/fill.png'))
	BtnFillInsidePoints.setText('F')
	BtnFillInsidePoints.setMinimumWidth(ICON_MIN_WIDTH)
	BtnFillInsidePoints.setMinimumHeight(ICON_MIN_HEIGHT)	
	BtnFillInsidePoints.clicked.connect(self.fillInMarkPoint)
	BtnFillInsidePoints.setToolTip('Finish Marking Points and Fill Class Labels inside Boundary')

	BtnDrawBoundary = QPushButton()
	BtnDrawBoundary.setIcon(QIcon(self.PWD+'/res/bndry.png'))
	BtnDrawBoundary.setText('B')
	BtnDrawBoundary.setMinimumWidth(ICON_MIN_WIDTH)
	BtnDrawBoundary.setMinimumHeight(ICON_MIN_HEIGHT)	
	BtnDrawBoundary.clicked.connect(self.setSegBoundary)
	BtnDrawBoundary.setToolTip('Add Boundary (pixel value = 255) between Segmentation Patches')

	SBSegBndryThickness = QSpinBox()
	SBSegBndryThickness.setMinimum(1)
	SBSegBndryThickness.valueChanged.connect(self.setSegBndryThickness)
	SBSegBndryThickness.setToolTip('Set Segmentation Bndry Thickness')


	BtnZoomIn = QPushButton()
	BtnZoomIn.setIcon(QIcon(self.PWD+'/res/zoomin.png'))
	BtnZoomIn.setText(u"\u2318" + "+")
	BtnZoomIn.setMinimumWidth(ICON_MIN_WIDTH)
	BtnZoomIn.setMinimumHeight(ICON_MIN_HEIGHT)	
	BtnZoomIn.clicked.connect(self.imgviewer.zoomIn)
	BtnZoomIn.setToolTip('Zoom-in Image')

	BtnZoomOut = QPushButton()
	BtnZoomOut.setIcon(QIcon(self.PWD+'/res/zoomout.png'))
	BtnZoomOut.setText(u"\u2318" + "-")
	BtnZoomOut.setMinimumWidth(ICON_MIN_WIDTH)
	BtnZoomOut.setMinimumHeight(ICON_MIN_HEIGHT)	
	BtnZoomOut.clicked.connect(self.imgviewer.zoomOut)
	BtnZoomOut.setToolTip('Zoom-out Image')

	BtnFitIn = QPushButton()
	BtnFitIn.setIcon(QIcon(self.PWD+'/res/fitin.png'))
	BtnFitIn.setText(u"\u2318" + "0")
	BtnFitIn.setMinimumWidth(ICON_MIN_WIDTH)
	BtnFitIn.setMinimumHeight(ICON_MIN_HEIGHT)	
	BtnFitIn.clicked.connect(self.imgviewer.fitInView)
	BtnFitIn.setToolTip('Fit-in Image')


	QLMoveImageFrame = QPushButton()
	QLMoveImageFrame.setMinimumWidth(ICON_MIN_WIDTH)
	QLMoveImageFrame.setMinimumHeight(ICON_MIN_HEIGHT)
	QLMoveImageFrame.setText('Move Image Frame: '+ u'\u2190 \u2191 \u2193 \u2192')
	QLMoveImageFrame.setEnabled(False)

	HBlayoutEdits.addWidget(BtnInspect)
	HBlayoutEdits.addWidget(BtnMarkPoint)
	HBlayoutEdits.addWidget(BtnReset)
	HBlayoutEdits.addWidget(BtnGoBack)
	HBlayoutEdits.addWidget(BtnFillLabelOnePixel)
	HBlayoutEdits.addWidget(BtnDrawLineBtwPoints)
	HBlayoutEdits.addWidget(SBScaleLineWidth)
	HBlayoutEdits.addWidget(BtnFillInsidePoints)
	HBlayoutEdits.addWidget(BtnDrawBoundary)
	HBlayoutEdits.addWidget(SBSegBndryThickness)
	HBlayoutEdits.addWidget(BtnZoomIn)
	HBlayoutEdits.addWidget(BtnZoomOut)
	HBlayoutEdits.addWidget(BtnFitIn)
	
	HBlayoutEdits.addWidget(QLMoveImageFrame)

	return HBlayoutEdits


def setLayoutView(self):

	HBlayoutView = QHBoxLayout() 
	HBlayoutView.setAlignment(Qt.AlignTop)
	HBlayoutView.addWidget(self.imgviewer, 7)
	HBlayoutView.addWidget(self.segviewer, 3)
	return HBlayoutView



def setLayoutLoadClassLabel(self):
	HBlayoutLoadClassLbl = QHBoxLayout()

	loadClassLbl = QPushButton("Load Class Label "+ u"\u2318" + "L")
	loadClassLbl.setMinimumWidth(BTN_MIN_WIDTH)
	loadClassLbl.clicked.connect(self.loadClassLabel)

	self.classLabelPath = QLineEdit(self)
	self.classLabelPath.setText(self.classLabelPath0)
	self.classLabelPath.returnPressed.connect(self.loadClassLabel)
	
	HBlayoutLoadClassLbl.setAlignment(Qt.AlignLeft)
	HBlayoutLoadClassLbl.addWidget(loadClassLbl, 4)
	HBlayoutLoadClassLbl.addWidget(self.classLabelPath,6)
	return HBlayoutLoadClassLbl



def setLayoutSelectClassLabel(self):
	HBlayoutSelectClassLabel = QHBoxLayout()
	HBlayoutSelectClassLabel.setAlignment(Qt.AlignCenter)
	
	QLselectLbl = QLabel()
	QLselectLbl.setAlignment(Qt.AlignLeft)
	QLselectLbl.setScaledContents(True)
	QLselectLbl.setText('Select/Enter Class Label (' + u'\u2193'  + ': < ,' + u'\u2191' + ':  >)')		

	self.QLEselectLbl = QSpinBox()
	self.QLEselectLbl.setToolTip('Change Class Label Index')	
	self.QLEselectLbl.valueChanged.connect(self.selectClassLbl)
	self.QLEselectLbl.setMinimum(0)
	self.QLEselectLbl.setMaximum(0)
	if self.Nclasslbl is not None:
		self.QLEselectLbl.setMaximum(self.Nclasslbl)


	HBlayoutSelectClassLabel.addWidget(QLselectLbl, 4)
	HBlayoutSelectClassLabel.addWidget(self.QLEselectLbl, 1)
	HBlayoutSelectClassLabel.addWidget(QWidget(), 5)
	return HBlayoutSelectClassLabel


def setLayoutQScrollClassLblInfo(self):
	QScrollClassLblInfo  = QScrollArea()
	self.classLabelInfo = QLabel()
	self.classLabelInfo.setAlignment(Qt.AlignLeft)
	self.classLabelInfo.setScaledContents(True)
	self.classLabelInfo.setText(self.featureBase)
	QScrollClassLblInfo.setWidget(self.classLabelInfo)

	return QScrollClassLblInfo



def setLayoutOpenImage(self):
	HBlayoutLoad = QHBoxLayout()

	btnLoad = QPushButton("Open Image " + u"\u2318" + "O")
	btnLoad.setMinimumWidth(BTN_MIN_WIDTH)
	btnLoad.setMaximumWidth(BTN_MAX_WIDTH)
	btnLoad.clicked.connect(self.loadImage)

	self.imagePath = QLineEdit(self)
	self.imagePath.setText(self.imagePath0)
	self.imagePath.returnPressed.connect(self.loadImage)

	HBlayoutLoad.setAlignment(Qt.AlignCenter)
	HBlayoutLoad.addWidget(btnLoad)
	HBlayoutLoad.addWidget(self.imagePath)
	return HBlayoutLoad


def setLayoutSaveImage(self):

	HBlayoutSave = QHBoxLayout()
	btnSave = QPushButton("Save Seg." + u"    \u2318" + "S")
	btnSave.setMinimumWidth(BTN_MIN_WIDTH)
	btnSave.setMaximumWidth(BTN_MAX_WIDTH)
	btnSave.clicked.connect(self.saveImage)	

	self.savePath = QLineEdit(self)
	self.savePath.setText('')
	self.savePath.returnPressed.connect(self.saveImage)

	HBlayoutSave.setAlignment(Qt.AlignCenter)
	HBlayoutSave.addWidget(btnSave)
	HBlayoutSave.addWidget(self.savePath)	
	return HBlayoutSave

def setLayoutImageInfo(self):
	VBlayoutStatus = QVBoxLayout()

	self.viewInfo = QLabel()
	self.viewInfo.setAlignment(Qt.AlignLeft)
	self.viewInfo.setScaledContents(True)
	self.viewInfo.setText('[Image Info]\n')		
	self.viewInfo.setMinimumHeight(100)
	
	VBlayoutStatus.setAlignment(Qt.AlignLeft)
	VBlayoutStatus.addWidget(self.viewInfo)
	return VBlayoutStatus



def setLayoutFileView(self):
	VBlayoutFileView = QVBoxLayout()
	VBlayoutFileView.setAlignment(Qt.AlignTop)

	# Label & Path

	HBlayoutFSInfo = QHBoxLayout()
	fsInfo = QLabel()
	fsInfo.setAlignment(Qt.AlignLeft)
	fsInfo.setText('Image Files')
	fsInfo.setScaledContents(True)

	self.fsPath = QLineEdit(self)
	self.fsPath.setText(self.PWD+'/image')
	self.fsPath.returnPressed.connect(self.loadFileSystem)		
	HBlayoutFSInfo.addWidget(fsInfo)
	HBlayoutFSInfo.addWidget(self.fsPath)

	# File System 
	self.treeView = QTreeView()
	#self.treeView.setSortingEnabled(True)
	self.fileview = QFileSystemModel(self.treeView)

	self.fileview.setFilter(QDir.NoDotAndDotDot | QDir.Files)
	self.fileview.setNameFilters(self.extfilters)
	self.fileview.setRootPath(self.PWD+'/image')
	self.fileview.setReadOnly(True)

	self.treeView.setModel(self.fileview)
	self.treeView.doubleClicked.connect(self.loadFileSystemItem)

	fileviewdir = QDir(self.PWD+'/image')
	root = self.fileview.setRootPath(fileviewdir.path())
	#files = fileviewdir.entryList()
	self.treeView.setRootIndex(root)

	VBlayoutFileView.addLayout(HBlayoutFSInfo)
	VBlayoutFileView.addWidget(self.treeView)

	return	VBlayoutFileView



def setLayoutFileViewLabelView(self):
	VBlayoutFileView = QVBoxLayout()
	VBlayoutFileView.setAlignment(Qt.AlignTop)

	# Label & Path

	HBlayoutFSInfo = QHBoxLayout()
	fsInfo = QLabel()
	fsInfo.setAlignment(Qt.AlignLeft)
	fsInfo.setText('Image Files')
	fsInfo.setScaledContents(True)

	self.fsPath = QLineEdit(self)
	self.fsPath.setText(self.PWD+'/image')
	self.fsPath.returnPressed.connect(self.loadFileSystem)		
	HBlayoutFSInfo.addWidget(fsInfo)
	HBlayoutFSInfo.addWidget(self.fsPath)

	# File System 
	self.treeView = QTreeView()
	#self.treeView.setSortingEnabled(True)
	self.fileview = QFileSystemModel(self.treeView)

	self.fileview.setFilter(QDir.NoDotAndDotDot | QDir.Files)
	self.fileview.setNameFilters(self.extfilters)
	self.fileview.setRootPath(self.PWD+'/image')
	self.fileview.setReadOnly(True)

	self.treeView.setModel(self.fileview)
	self.treeView.doubleClicked.connect(self.loadFileSystemItem)

	fileviewdir = QDir(self.PWD+'/image')
	root = self.fileview.setRootPath(fileviewdir.path())
	#files = fileviewdir.entryList()
	self.treeView.setRootIndex(root)



	HBlayoutLabelSelect = QHBoxLayout()
	VBlayoutLabelSelect = QVBoxLayout()

	QLabelSelect = QLabel()
	QLabelSelect.setAlignment(Qt.AlignBottom)
	QLabelSelect.setAlignment(Qt.AlignRight)
	QLabelSelect.setText('Select Class Label')


	self.QListClassLabel = QListWidget()

	VBlayoutLabelSelect.addWidget(QLabelSelect, 1)
	VBlayoutLabelSelect.addWidget(self.QListClassLabel,9)

	HBlayoutLabelSelect.addWidget(QLabel(), 1)
	HBlayoutLabelSelect.addLayout(VBlayoutLabelSelect, 9)


	VBlayoutFileView.addLayout(HBlayoutFSInfo, 1)
	VBlayoutFileView.addWidget(self.treeView, 6)
	VBlayoutFileView.addLayout(HBlayoutLabelSelect,2)
	

	return	VBlayoutFileView



