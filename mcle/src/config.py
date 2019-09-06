from __future__ import absolute_import
from PyQt5.QtWidgets import *
from PyQt5.QtCore import * 
from PyQt5.QtGui import *
from src.clsobjhandler import *
import os

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
	HBlayoutSaveSegImage 	= setLayoutSaveSegImage(self)
	HBlayoutSaveObjImage 	= setLayoutSaveObjImage(self)

	# 'Image Info' widget
	HBlayoutImageInfo 		= setLayoutImageInfo(self)

	# Object / Class List
	VBlayoutObjectClassControl = setLayoutObjectClassView(self)

	# File System Widget
	#VBlayoutFileView 		= setLayoutFileView(self)
	VBlayoutFileView 		= setLayoutFileViewNew(self)

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
	VBlayoutLSS.addLayout(HBlayoutOpenImage, 1)
	VBlayoutLSS.addLayout(HBlayoutSaveSegImage,1)
	VBlayoutLSS.addLayout(HBlayoutSaveObjImage,1)
	VBlayoutLSS.addLayout(HBlayoutImageInfo,  7)


	# HBlayoutMain
	HBlayoutMain.addLayout(VBlayoutLSS,     4)
	HBlayoutMain.addLayout(VBlayoutViewInfo,4)

	# Main View widget layout
	LayoutMainView.addLayout(HBlayoutViewMain, 8)
	LayoutMainView.addLayout(HBlayoutMain,     2)

	HLayoutMain.addLayout(LayoutMainView,   8)
	HLayoutMain.addLayout(VBlayoutObjectClassControl, 2)
	HLayoutMain.addLayout(VBlayoutFileView, 2)




	LayoutMain.addLayout(HBlayoutEdits, 1) 		# Edit buttons
	LayoutMain.addLayout(HLayoutMain,   9)		# layout below buttons

	self.SBObjClsLabeler.setValue(1)




def setLayoutEdit(self):
	HBlayoutEdits = QHBoxLayout() 
	HBlayoutEdits.setAlignment(Qt.AlignLeft)

	self.BtnInspect = QPushButton()
	self.BtnInspect.setCheckable(True)
	self.BtnInspect.setIcon(QIcon(os.path.join(self.PWD,'res','magnifying_glass.png')))
	self.BtnInspect.setText('I')
	self.BtnInspect.setMinimumWidth(ICON_MIN_WIDTH)
	self.BtnInspect.setMinimumHeight(ICON_MIN_HEIGHT)
	self.BtnInspect.clicked.connect(self.switchInspectionMode)
	self.BtnInspect.setToolTip('Image/pixel Inspection')

	self.BtnMarkPoint = QPushButton()
	self.BtnMarkPoint.setCheckable(True)
	self.BtnMarkPoint.setIcon(QIcon(os.path.join(self.PWD,'res','pin.png')))
	self.BtnMarkPoint.setText('M')
	self.BtnMarkPoint.setMinimumWidth(ICON_MIN_WIDTH)
	self.BtnMarkPoint.setMinimumHeight(ICON_MIN_HEIGHT)
	self.BtnMarkPoint.clicked.connect(self.switchMarkPointMode)
	self.BtnMarkPoint.setToolTip('Pixel Marker of Class Label')

	BtnReset = QPushButton()
	BtnReset.setIcon(QIcon(os.path.join('res','reset.png')))
	BtnReset.setText(u"\u2318" + "R")
	BtnReset.setMinimumWidth(ICON_MIN_WIDTH)
	BtnReset.setMinimumHeight(ICON_MIN_HEIGHT)	
	BtnReset.clicked.connect(self.resetImage)
	BtnReset.setToolTip('Reset All')

	BtnGoBack = QPushButton()
	BtnGoBack.setIcon(QIcon(os.path.join(self.PWD,'res','left_arrow.png')))
	BtnGoBack.setText(u"\u232B")
	BtnGoBack.setMinimumWidth(ICON_MIN_WIDTH)
	BtnGoBack.setMinimumHeight(ICON_MIN_HEIGHT)	
	BtnGoBack.clicked.connect(self.delOneMarkPoint)
	BtnGoBack.setToolTip('Go One Step Back (Pixel Marker)')

	self.BtnFillLabelOnePixel = QPushButton()
	self.BtnFillLabelOnePixel.setCheckable(True)
	self.BtnFillLabelOnePixel.setIcon(QIcon(os.path.join(self.PWD,'res','dropper.png')))
	self.BtnFillLabelOnePixel.setText("P")
	self.BtnFillLabelOnePixel.setMinimumWidth(ICON_MIN_WIDTH)
	self.BtnFillLabelOnePixel.setMinimumHeight(ICON_MIN_HEIGHT)	
	self.BtnFillLabelOnePixel.clicked.connect(self.switchFillPixelMode)
	self.BtnFillLabelOnePixel.setToolTip('Fill Class Label in One Pixel')


	BtnDrawLineBtwPoints = QPushButton()
	BtnDrawLineBtwPoints.setIcon(QIcon(os.path.join(self.PWD,'res','line.png')))
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
	BtnFillInsidePoints.setIcon(QIcon(os.path.join(self.PWD,'res','fill.png')))
	BtnFillInsidePoints.setText('F')
	BtnFillInsidePoints.setMinimumWidth(ICON_MIN_WIDTH)
	BtnFillInsidePoints.setMinimumHeight(ICON_MIN_HEIGHT)	
	BtnFillInsidePoints.clicked.connect(self.fillInMarkPoint)
	BtnFillInsidePoints.setToolTip('Finish Marking Points and Fill Class Labels inside Boundary')

	BtnDrawBoundary = QPushButton()
	BtnDrawBoundary.setIcon(QIcon(os.path.join(self.PWD,'res','bndry.png')))
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
	BtnZoomIn.setIcon(QIcon(os.path.join(self.PWD,'res','zoomin.png')))
	BtnZoomIn.setText(u"\u2318" + "+")
	BtnZoomIn.setMinimumWidth(ICON_MIN_WIDTH)
	BtnZoomIn.setMinimumHeight(ICON_MIN_HEIGHT)	
	BtnZoomIn.clicked.connect(self.imgviewer.zoomIn)
	BtnZoomIn.setToolTip('Zoom-in Image')

	BtnZoomOut = QPushButton()
	BtnZoomOut.setIcon(QIcon(os.path.join(self.PWD,'res','zoomout.png')))
	BtnZoomOut.setText(u"\u2318" + "-")
	BtnZoomOut.setMinimumWidth(ICON_MIN_WIDTH)
	BtnZoomOut.setMinimumHeight(ICON_MIN_HEIGHT)	
	BtnZoomOut.clicked.connect(self.imgviewer.zoomOut)
	BtnZoomOut.setToolTip('Zoom-out Image')

	BtnFitIn = QPushButton()
	BtnFitIn.setIcon(QIcon(os.path.join(self.PWD,'res','fitin.png')))
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

	HBlayoutEdits.addWidget(self.BtnInspect)
	HBlayoutEdits.addWidget(self.BtnMarkPoint)
	HBlayoutEdits.addWidget(BtnReset)
	HBlayoutEdits.addWidget(BtnGoBack)
	HBlayoutEdits.addWidget(self.BtnFillLabelOnePixel)
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
	QLabelImgView = QLabel()
	QLabelImgView.setAlignment(Qt.AlignBottom)
	QLabelImgView.setText('Image Viewer')	

	QLabelClassSegView = QLabel()
	QLabelClassSegView.setAlignment(Qt.AlignBottom)
	QLabelClassSegView.setText('Class Viewer')	

	QLabelObjSegView = QLabel()
	QLabelObjSegView.setAlignment(Qt.AlignBottom)
	QLabelObjSegView.setText('Object Viewer')	


	VBlayoutView1 = QVBoxLayout() 
	VBlayoutView1.addWidget(QLabelImgView, 0.1)
	VBlayoutView1.addWidget(self.imgviewer,  19)	

	VBlayoutView2 = QVBoxLayout() 
	VBlayoutView2.addWidget(QLabelClassSegView, 1)
	VBlayoutView2.addWidget(self.classSegViewer,  19)
	VBlayoutView2.addWidget(QLabelObjSegView, 1)
	VBlayoutView2.addWidget(self.objectSegViewer, 19)	


	HBlayoutView = QHBoxLayout() 
	HBlayoutView.setAlignment(Qt.AlignTop)
	HBlayoutView.addLayout(VBlayoutView1, 7)
	HBlayoutView.addLayout(VBlayoutView2, 3)	
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
	QLselectLbl.setAlignment(Qt.AlignCenter)
	QLselectLbl.setScaledContents(True)
	QLselectLbl.setText('Select/Enter Class Label (' + u'\u2193'  + ': - ,' + u'\u2191' + ':  +)')		

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


def setLayoutSaveSegImage(self):
	HBlayoutSave = QHBoxLayout()
	btnSave = QPushButton("Save Class Seg." + u" \u2318" + "S")
	btnSave.setMinimumWidth(BTN_MIN_WIDTH)
	btnSave.setMaximumWidth(BTN_MAX_WIDTH)
	btnSave.clicked.connect(self.saveClsSegImage)	

	self.saveClsSegPath = QLineEdit(self)
	self.saveClsSegPath.setText('')
	self.saveClsSegPath.returnPressed.connect(self.saveClsSegImage)

	HBlayoutSave.setAlignment(Qt.AlignCenter)
	HBlayoutSave.addWidget(btnSave)
	HBlayoutSave.addWidget(self.saveClsSegPath)	
	return HBlayoutSave


def setLayoutSaveObjImage(self):
	HBlayoutSave = QHBoxLayout()
	btnSave = QPushButton("Save Obj. Seg." + u" \u2318" + "S")
	btnSave.setMinimumWidth(BTN_MIN_WIDTH)
	btnSave.setMaximumWidth(BTN_MAX_WIDTH)
	btnSave.clicked.connect(self.saveObjSegImage)	

	self.saveObjSegPath = QLineEdit(self)
	self.saveObjSegPath.setText('')
	self.saveObjSegPath.returnPressed.connect(self.saveObjSegImage)

	HBlayoutSave.setAlignment(Qt.AlignCenter)
	HBlayoutSave.addWidget(btnSave)
	HBlayoutSave.addWidget(self.saveObjSegPath)	
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



def setLayoutFileViewNew(self):
	VBlayoutFileView = QVBoxLayout()
	VBlayoutFileView.setAlignment(Qt.AlignTop)

	# Label & Path
	HVlayoutFSInfo = QVBoxLayout()
	fsInfo = QLabel()
	fsInfo.setAlignment(Qt.AlignLeft)
	fsInfo.setText('Image Files')
	fsInfo.setScaledContents(True)

	self.fsPath = QLineEdit(self)
	self.fsPath.setText(os.path.join(self.PWD,'image'))
	self.fsPath.returnPressed.connect(self.loadFileSystem)		
	HVlayoutFSInfo.addWidget(fsInfo)
	HVlayoutFSInfo.addWidget(self.fsPath)

	# File System 
	self.fileSysTreeView = QTreeView()
	#self.fileSysTreeView.setSortingEnabled(True)
	self.fileSysview = QFileSystemModel(self.fileSysTreeView)
	self.fileSysview.setFilter(QDir.NoDotAndDotDot | QDir.Files)
	self.fileSysview.setNameFilters(self.extfilters)
	self.fileSysview.setNameFilterDisables(False)
	self.fileSysview.setRootPath(os.path.join(self.PWD,'image'))
	self.fileSysview.setReadOnly(True)

	self.fileSysTreeView.setModel(self.fileSysview)
	self.fileSysTreeView.doubleClicked.connect(self.loadFileSystemItem)

	fileviewdir = QDir(os.path.join(self.PWD,'image'))
	root = self.fileSysview.setRootPath(fileviewdir.path())
	#files = fileviewdir.entryList()
	self.fileSysTreeView.setRootIndex(root)

	HBlayoutLabelSelect = QHBoxLayout()
	VBlayoutLabelSelect = QVBoxLayout()

	QLabelSelect = QLabel()
	QLabelSelect.setAlignment(Qt.AlignBottom)
	QLabelSelect.setAlignment(Qt.AlignRight)
	QLabelSelect.setText('Select Class Label')


	self.QListClassLabel = QListWidget()

	VBlayoutLabelSelect.addWidget(QLabelSelect, 0.1)
	VBlayoutLabelSelect.addWidget(self.QListClassLabel,9)

	HBlayoutLabelSelect.addWidget(QLabel(), 1)
	HBlayoutLabelSelect.addLayout(VBlayoutLabelSelect, 9)


	VBlayoutFileView.addLayout(HVlayoutFSInfo, 0.1)
	VBlayoutFileView.addWidget(self.fileSysTreeView, 6)
	VBlayoutFileView.addLayout(HBlayoutLabelSelect,3)
	return	VBlayoutFileView


def setLayoutObjectClassView(self):
	QLabelObjClsHandler = QLabel()
	QLabelObjClsHandler.setAlignment(Qt.AlignBottom)
	QLabelObjClsHandler.setAlignment(Qt.AlignCenter)
	QLabelObjClsHandler.setText('Object / Class')

	self.SBObjClsLabeler = QSpinBox()
	self.SBObjClsLabeler.setMinimum(0)
	self.SBObjClsLabeler.setMaximum(255)
	self.SBObjClsLabeler.valueChanged.connect(self.selectObjClsLbl)

	QLabelKillObjCls = QLabel()
	QLabelKillObjCls.setAlignment(Qt.AlignCenter)
	QLabelKillObjCls.setText('Press \'K\' to remove Object')

	HBlayout = QHBoxLayout()
	HBlayout.setAlignment(Qt.AlignLeft)
	HBlayout.addWidget(QLabelObjClsHandler)
	HBlayout.addWidget(self.SBObjClsLabeler)


	self.clsObjHandler = clsObjTreeHandler(self)

	VBlayoutObjClsHandler	 	= QVBoxLayout()
	VBlayoutObjClsHandler.addLayout(HBlayout, 0.5)
	#VBlayoutObjClsHandler.addWidget(self.QTreeObjectClassHandler, 9.5)
	VBlayoutObjClsHandler.addWidget(self.clsObjHandler, 9.5)
	VBlayoutObjClsHandler.addWidget(QLabelKillObjCls, 0.1)

	return VBlayoutObjClsHandler



